import random

QUESTIONS = [
    {
    "id": "q1",
    "difficulty": "easy",
    "topic": "select_where_order",
    "prompt": "Find the first_name, last_name, and state of all customers who live in California, ordered alphabetically by last_name.",
    "expected_sql": """
SELECT first_name, last_name, state
FROM customers
WHERE state = 'CA'
ORDER BY last_name ASC;
""".strip(),
    "required_patterns": [
        {"label": "select from customers table", "pattern": r"from\s+customers"},
        {"label": "filter customers in California", "pattern": r"where\s+.*state\s*=\s*['\"]ca['\"]"},
        {"label": "order results by last_name", "pattern": r"order\s+by\s+.*last_name"}
    ],
    "concepts": ["SELECT", "WHERE", "ORDER BY"],
    "explanation": "Tests selecting columns, filtering rows using WHERE, and ordering results with ORDER BY."
},
    {
    "id": "q3",
    "difficulty": "medium",
    "topic": "joins_aggregation_filtering",
    "prompt": "List the total quantity of products ordered and total revenue generated per product category for orders with status 'completed'. Order the results by total revenue in descending order.",
    "expected_sql": """
SELECT
    p.category,
    SUM(oi.quantity) AS total_quantity,
    SUM(oi.quantity * oi.unit_price) AS total_revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
JOIN products p
    ON oi.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY p.category
ORDER BY total_revenue DESC;
""".strip(),
    "required_patterns": [
        {"label": "join orders to order_items", "pattern": r"join\s+order_items"},
        {"label": "join order_items to products", "pattern": r"join\s+products"},
        {"label": "filter for completed orders", "pattern": r"where\s+.*status\s*=\s*['\"]completed['\"]"},
        {"label": "group by category", "pattern": r"group\s+by\s+.*category"},
        {"label": "sum aggregated values", "pattern": r"sum\s*\("},
        {"label": "order by descending revenue", "pattern": r"order\s+by\s+.*desc"},
    ],
    "concepts": ["JOIN", "WHERE", "GROUP BY", "SUM", "ORDER BY"],
    "explanation": "Tests multi-table joins, filtering, aggregation, and ordering."
}
]
def get_question_by_id(question_id: str):
    return next((q for q in QUESTIONS if q["id"] == question_id), None)

def get_random_question(difficulty: str | None = None):
    pool = QUESTIONS
    if difficulty:
        pool = [q for q in QUESTIONS if q["difficulty"] == difficulty.lower()]
    return random.choice(pool) if pool else None