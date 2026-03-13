import json
import sqlite3
from typing import Any
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from openai import OpenAI
from questions import QUESTIONS, get_question_by_id, get_random_question

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://realsqlprac.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db.sqlite")

SCHEMA_TEXT = """
Dataset: retail_orders

Tables:
1) customers(customer_id, first_name, last_name, state, signup_date)
2) products(product_id, product_name, category, price)
3) orders(order_id, customer_id, order_date, status, total_amount)
4) order_items(order_item_id, order_id, product_id, quantity, unit_price)

Relationships:
- orders.customer_id -> customers.customer_id
- order_items.order_id -> orders.order_id
- order_items.product_id -> products.product_id
""".strip()

QUESTION_BANK = [
    {
        "id": "q1",
        "difficulty": "Easy",
        "prompt": "Find the first_name, last_name, and state of all customers who live in California, ordered alphabetically by last_name.",
        "expected_sql": "SELECT first_name, last_name, state FROM customers WHERE state = 'CA' ORDER BY last_name ASC;"
    },
    {
        "id": "q2",
        "difficulty": "Medium",
        "prompt": "List each product category and the number of products in that category. Sort by the count descending.",
        "expected_sql": "SELECT category, COUNT(*) AS product_count FROM products GROUP BY category ORDER BY product_count DESC;"
    },
]

class QueryRequest(BaseModel):
    sql: str
    datasetId: str

class GeneratePromptRequest(BaseModel):
    datasetId: str

class CheckAnswerRequest(BaseModel):
    datasetId: str
    questionId: str
    sql: str
def generate_ai_feedback(question_prompt: str, expected_sql: str, student_sql: str, reason: str, missing_patterns: list[str]) -> str:
    try:
        missing_text = ", ".join(missing_patterns) if missing_patterns else "None"

        prompt = f"""
        You are helping a student practice SQL.

        Question:
        {question_prompt}

        Expected SQL:
        {expected_sql}

        Student SQL:
        {student_sql}

        Checker result:
        - reason: {reason}
        - missing patterns: {missing_text}

        Write a short explanation of what the student likely did wrong.
        Rules:
        - Be concise
        - Be specific
        - Do NOT give the full corrected SQL
        - Give a hint about what to fix
        - If the issue is alias/column naming only, say that clearly
        """

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a SQL tutor. Explain mistakes clearly and briefly without revealing the full solution."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"AI feedback unavailable: {str(e)}"
def normalize_sql_text(sql: str) -> str:
    return " ".join(sql.lower().split())

def sql_contains_required_patterns(sql: str, patterns: list[dict]) -> tuple[bool, list[str]]:
    normalized = normalize_sql_text(sql)
    missing = []

    for item in patterns:
        if not re.search(item["pattern"], normalized):
            missing.append(item["label"])

    return len(missing) == 0, missing

def normalize_rows_by_values(rows):
    return sorted([tuple(row.values()) for row in rows])

def get_conn():
    return sqlite3.connect(DB_PATH)

def rows_to_dicts(cursor, rows):
    columns = [desc[0] for desc in cursor.description] if cursor.description else []
    return [dict(zip(columns, row)) for row in rows]

def is_safe_select(sql: str) -> bool:
    normalized = sql.strip().lower()
    banned = ["insert", "update", "delete", "drop", "alter", "create", "attach", "pragma"]
    return normalized.startswith("select") and not any(word in normalized for word in banned)

def run_select(sql: str) -> list[dict[str, Any]]:
    if not is_safe_select(sql):
        raise HTTPException(status_code=400, detail="Only safe SELECT queries are allowed.")

    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        return rows_to_dicts(cur, rows)
    except sqlite3.Error as e:
        raise HTTPException(status_code=400, detail=f"SQL error: {str(e)}")
    finally:
        conn.close()
def normalize_rows(rows):
    return sorted([tuple(row.values()) for row in rows])
@app.get("/")
def root():
    return {"status": "ok"}
@app.get("/health")
def health():
    return {"ok": True}

@app.post("/api/query")
def query(req: QueryRequest):
    rows = run_select(req.sql)
    return {"rows": rows}

@app.post("/api/generate-prompt")
def generate_prompt(req: GeneratePromptRequest):
    question = get_random_question()

    if not question:
        raise HTTPException(status_code=404, detail="No questions available")

    return {
        "questionId": question["id"],
        "difficulty": question["difficulty"].title(),
        "naturalLanguage": question["prompt"],
        "expectedSql": question["expected_sql"],
        "explanation": question["explanation"],
        "concepts": question["concepts"],
    }

@app.post("/api/check-answer")
def check_answer(req: CheckAnswerRequest):
    question = get_question_by_id(req.questionId)

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    try:
        expected_rows = run_select(question["expected_sql"])
        student_rows = run_select(req.sql)
    except HTTPException as e:
        ai_feedback = generate_ai_feedback(
            question["prompt"],
            question["expected_sql"],
            req.sql,
            "sql_error",
            []
        )
        return {
            "correct": False,
            "feedback": e.detail,
            "aiFeedback": ai_feedback,
            "reason": "sql_error",
            "missingPatterns": [],
            "expectedPreview": [],
            "studentPreview": [],
        }

    structure_ok, missing = sql_contains_required_patterns(
        req.sql,
        question["required_patterns"]
    )

    if expected_rows == student_rows and structure_ok:
        return {
            "correct": True,
            "feedback": "Correct.",
            "aiFeedback": "",
            "reason": "correct",
            "missingPatterns": [],
            "expectedPreview": expected_rows[:10],
            "studentPreview": student_rows[:10],
        }

    if normalize_rows_by_values(expected_rows) == normalize_rows_by_values(student_rows) and structure_ok:
        ai_feedback = generate_ai_feedback(
            question["prompt"],
            question["expected_sql"],
            req.sql,
            "alias_mismatch",
            []
        )
        return {
            "correct": False,
            "feedback": "Your values are correct, but your column names or aliases differ from the expected output.",
            "aiFeedback": ai_feedback,
            "reason": "alias_mismatch",
            "missingPatterns": [],
            "expectedPreview": expected_rows[:10],
            "studentPreview": student_rows[:10],
        }

    if expected_rows == student_rows and not structure_ok:
        ai_feedback = generate_ai_feedback(
            question["prompt"],
            question["expected_sql"],
            req.sql,
            "lucky_result",
            missing
        )
        return {
            "correct": False,
            "feedback": "Your query returns the expected rows on this dataset, but it is missing required SQL structure for this question.",
            "aiFeedback": ai_feedback,
            "reason": "lucky_result",
            "missingPatterns": missing,
            "expectedPreview": expected_rows[:10],
            "studentPreview": student_rows[:10],
        }

    if not structure_ok:
        ai_feedback = generate_ai_feedback(
            question["prompt"],
            question["expected_sql"],
            req.sql,
            "missing_structure",
            missing
        )
        return {
            "correct": False,
            "feedback": "Your query is missing required SQL structure.",
            "aiFeedback": ai_feedback,
            "reason": "missing_structure",
            "missingPatterns": missing,
            "expectedPreview": expected_rows[:10],
            "studentPreview": student_rows[:10],
        }

    ai_feedback = generate_ai_feedback(
        question["prompt"],
        question["expected_sql"],
        req.sql,
        "wrong_result",
        []
    )
    return {
        "correct": False,
        "feedback": "Result does not match the expected output.",
        "aiFeedback": ai_feedback,
        "reason": "wrong_result",
        "missingPatterns": [],
        "expectedPreview": expected_rows[:10],
        "studentPreview": student_rows[:10],
    }