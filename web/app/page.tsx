"use client";

import React, { useMemo, useState } from "react";
import { motion } from "framer-motion";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import {
  Brain,
  Database,
  Play,
  RefreshCw,
  CheckCircle2,
  XCircle,
  Sparkles,
  TerminalSquare,
} from "lucide-react";

const schemaText = `Database: streaming_platform

users
-----
user_id INTEGER PRIMARY KEY
first_name TEXT
last_name TEXT
email TEXT
country TEXT
signup_date TEXT
birth_year INTEGER

subscription_plans
------------------
plan_id INTEGER PRIMARY KEY
plan_name TEXT
monthly_price REAL
max_devices INTEGER
video_quality TEXT

subscriptions
-------------
subscription_id INTEGER PRIMARY KEY
user_id INTEGER
plan_id INTEGER
start_date TEXT
end_date TEXT
status TEXT

profiles
--------
profile_id INTEGER PRIMARY KEY
user_id INTEGER
profile_name TEXT
is_kids_profile INTEGER

genres
------
genre_id INTEGER PRIMARY KEY
genre_name TEXT

shows
-----
show_id INTEGER PRIMARY KEY
title TEXT
release_year INTEGER
country TEXT
content_type TEXT
age_rating TEXT

show_genres
-----------
show_id INTEGER
genre_id INTEGER
PRIMARY KEY (show_id, genre_id)

seasons
-------
season_id INTEGER PRIMARY KEY
show_id INTEGER
season_number INTEGER
release_year INTEGER

episodes
--------
episode_id INTEGER PRIMARY KEY
season_id INTEGER
episode_number INTEGER
title TEXT
duration_minutes INTEGER

watch_history
-------------
watch_id INTEGER PRIMARY KEY
profile_id INTEGER
episode_id INTEGER
watched_at TEXT
minutes_watched INTEGER
completed INTEGER

ratings
-------
rating_id INTEGER PRIMARY KEY
profile_id INTEGER
show_id INTEGER
rating INTEGER
rating_date TEXT

actors
------
actor_id INTEGER PRIMARY KEY
first_name TEXT
last_name TEXT
birth_year INTEGER
country TEXT

show_cast
---------
show_id INTEGER
actor_id INTEGER
role_name TEXT
PRIMARY KEY (show_id, actor_id)

payments
--------
payment_id INTEGER PRIMARY KEY
subscription_id INTEGER
payment_date TEXT
amount REAL
payment_method TEXT
payment_status TEXT`;


const starterPrompt = {
  id: "q1",
  difficulty: "Easy",
  naturalLanguage:
    "Find the title, release_year, and country of all shows released after 2020, ordered by release_year descending.",
  expectedSql:
    "SELECT title, release_year, country FROM shows WHERE release_year > 2020 ORDER BY release_year DESC;",
  explanation: "This checks basic SELECT, WHERE, and ORDER BY skills.",
};

const starterRows = [
  { title: "City Lights", release_year: 2024, country: "USA" },
  { title: "Shadow Point", release_year: 2023, country: "UK" },
  { title: "Golden Hour", release_year: 2021, country: "Canada" },
];

function normalizeSql(sql: string) {
  return sql
    .replace(/--.*$/gm, "")
    .replace(/\s+/g, " ")
    .replace(/\s*;\s*$/, "")
    .trim()
    .toLowerCase();
}

function ResultTable({ rows }: { rows: Record<string, unknown>[] }) {
  if (!rows?.length) {
    return <div className="text-sm text-muted-foreground">No rows returned.</div>;
  }

  const columns = Object.keys(rows[0]);

  return (
    <div className="overflow-x-auto rounded-2xl border">
      <table className="w-full text-sm">
        <thead className="bg-muted/50">
          <tr>
            {columns.map((col) => (
              <th key={col} className="px-4 py-3 text-left font-medium">
                {col}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, idx) => (
            <tr key={idx} className="border-t">
              {columns.map((col) => (
                <td key={col} className="px-4 py-3 align-top">
                  {String(row[col])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default function SQLPracticeUI() {
  const [sql, setSql] = useState(
    "SELECT first_name, last_name, country FROM users ORDER BY last_name;"
  );
  const [practicePrompt, setPracticePrompt] = useState(starterPrompt);
  const [queryResult, setQueryResult] = useState<Record<string, unknown>[]>(starterRows);
  const [runStatus, setRunStatus] = useState<"idle" | "running" | "done" | "error">("idle");
  const [isCheckingAnswer, setIsCheckingAnswer] = useState(false);
  const [runMessage, setRunMessage] = useState("Run a SQL query against the selected dataset.");
  const [checkResult, setCheckResult] = useState<null | {
    correct: boolean;
    feedback: string;
    aiFeedback?: string;
    expectedPreview?: Record<string, unknown>[];
    studentPreview?: Record<string, unknown>[];
  }>(null);

  const API_BASE_URL =
    process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

  const sqlLooksCorrect = useMemo(() => {
    return normalizeSql(sql) === normalizeSql(practicePrompt.expectedSql);
  }, [sql, practicePrompt.expectedSql]);

  async function runQuery() {
    setRunStatus("running");
    setRunMessage("Executing query...");

    try {
      const res = await fetch(`${API_BASE_URL}/api/query`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          sql,
          datasetId: "streaming_platform",
          questionId: practicePrompt.id,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        const message =
          typeof data.detail === "string"
            ? data.detail
            : JSON.stringify(data.detail || data);
        throw new Error(message);
      }

      setQueryResult(data.rows);
      setRunStatus("done");
      setRunMessage("Query executed successfully.");
    } catch (err) {
      setRunStatus("error");
      setRunMessage(err instanceof Error ? err.message : "Unknown error");
      setQueryResult([]);
    }
  }

  async function generatePrompt() {
    try {
      const res = await fetch(`${API_BASE_URL}/api/generate-prompt`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          datasetId: "streaming_platform",
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        const message =
          typeof data.detail === "string"
            ? data.detail
            : JSON.stringify(data.detail || data);
        throw new Error(message);
      }

      setPracticePrompt({
        id: data.questionId,
        difficulty: data.difficulty,
        naturalLanguage: data.naturalLanguage,
        expectedSql: data.expectedSql,
        explanation: data.explanation,
      });

      setSql("");
      setCheckResult(null);
      setQueryResult([]);
      setRunStatus("idle");
      setRunMessage("New AI prompt generated.");
    } catch (err) {
      setRunMessage(err instanceof Error ? err.message : "Unknown error");
    }
  }

  async function checkAnswer() {
    if (isCheckingAnswer) return;

    setIsCheckingAnswer(true);
    setCheckResult(null);

    try {
      const res = await fetch(`${API_BASE_URL}/api/check-answer`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          datasetId: "streaming_platform",
          questionId: practicePrompt.id,
          sql,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        const message =
          typeof data.detail === "string"
            ? data.detail
            : JSON.stringify(data.detail || data);
        throw new Error(message);
      }

      setCheckResult({
        correct: data.correct,
        feedback: data.feedback,
        aiFeedback: data.aiFeedback,
        expectedPreview: data.expectedPreview,
        studentPreview: data.studentPreview,
      });
    } catch (err) {
      setCheckResult({
        correct: false,
        feedback: err instanceof Error ? err.message : "Unknown error",
        aiFeedback: "",
        expectedPreview: [],
        studentPreview: [],
      });
    } finally {
      setIsCheckingAnswer(false);
    }
  }

  return (
    <div className="min-h-screen bg-background p-6">
      <div className="mx-auto grid max-w-7xl gap-6 lg:grid-cols-[1.1fr_0.9fr]">
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
          <Card className="rounded-2xl shadow-sm">
            <CardHeader>
              <div className="flex items-center justify-between gap-3">
                <div style={{ color: "#000080" }}>
                  <CardTitle className="flex items-center gap-2 text-2xl">
                    <TerminalSquare className="h-6 w-6" />
                    SQL Prac
                  </CardTitle>
                  <CardDescription>
                    First query takes time to connect to DB ~20s, after it should be good
                  </CardDescription>
                </div>
                <Badge className="rounded-full px-3 py-1">Dataset locked</Badge>
              </div>
            </CardHeader>

            <CardContent className="space-y-4">
              <div className="grid gap-3 md:grid-cols-[1fr_auto_auto]">
                <Button onClick={runQuery} className="rounded-2xl" disabled={isCheckingAnswer}>
                  <Play className="mr-2 h-4 w-4" />
                  Run Query
                </Button>
                <Button
                  variant="outline"
                  onClick={checkAnswer}
                  className="rounded-2xl"
                  disabled={isCheckingAnswer}
                >
                  <CheckCircle2 className="mr-2 h-4 w-4" />
                  {isCheckingAnswer ? "Checking..." : "Check Answer"}
                </Button>
              </div>

              <div className="rounded-2xl border bg-muted/30 p-3 text-sm">
                <div
                  className="font-medium"
                  style={{ color: "#000080", fontSize: "1rem", fontWeight: "bold" }}
                >
                  Execution status
                </div>
                <div
                  style={{ color: "black", fontSize: "1rem" }}
                  className="mt-1 text-muted-foreground"
                >
                  {runStatus === "idle" ? "Idle." : runMessage}
                </div>
              </div>

              <Textarea
                value={sql}
                onChange={(e) => setSql(e.target.value)}
                placeholder="Write your SQL here..."
                className="min-h-[260px] rounded-2xl font-mono text-sm"
              />

              <Tabs defaultValue="results">
                <TabsList className="rounded-2xl">
                  <TabsTrigger value="results">Results</TabsTrigger>
                  <TabsTrigger value="schema">Schema</TabsTrigger>
                </TabsList>

                <TabsContent value="results" className="mt-4">
                  <ResultTable rows={queryResult} />
                </TabsContent>

                <TabsContent value="schema" className="mt-4">
                  <pre className="overflow-x-auto whitespace-pre-wrap rounded-2xl border bg-muted/30 p-4 text-sm">
                    {schemaText}
                  </pre>
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.06 }}
        >
          <div className="space-y-6">
            <Card className="rounded-2xl shadow-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Brain className="h-5 w-5" />
                  AI Practice Coach
                </CardTitle>
                <CardDescription>
                  A model trained or tuned on this dataset can generate realistic SQL exercises.
                </CardDescription>
              </CardHeader>

              <CardContent className="space-y-4">
                <div className="flex items-center gap-2">
                  <Badge variant="secondary">Question ID: {practicePrompt.id}</Badge>
                  <Badge variant="outline">{practicePrompt.difficulty}</Badge>
                </div>

                <div className="rounded-2xl border p-4">
                  <div
                    style={{ color: "#000080", fontSize: "1rem", fontWeight: "bold" }}
                    className="mb-2 flex items-center gap-2 font-medium"
                  >
                    <Sparkles className="h-4 w-4" />
                    Prompt for the user
                  </div>
                  <p
                    style={{ fontSize: "1.5rem", lineHeight: "1.25", color: "Black" }}
                    className="text-sm text-muted-foreground"
                  >
                    {practicePrompt.naturalLanguage}
                  </p>
                </div>

                <Button onClick={generatePrompt} variant="outline" className="w-full rounded-2xl">
                  <RefreshCw className="mr-2 h-4 w-4" />
                  Generate Prompt
                </Button>
              </CardContent>
            </Card>

            <Card className="rounded-2xl shadow-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Database className="h-5 w-5" />
                  Answer Feedback
                </CardTitle>
                <CardDescription>Immediate evaluation for practice mode.</CardDescription>
              </CardHeader>

              <CardContent>
                {checkResult ? (
                  <div
                    className={`rounded-2xl border p-4 ${
                      checkResult.correct ? "bg-green-50" : "bg-red-50"
                    }`}
                  >
                    <div className="mb-2 flex items-center gap-2 font-semibold">
                      {checkResult.correct ? (
                        <>
                          <CheckCircle2 className="h-5 w-5" /> Correct
                        </>
                      ) : (
                        <>
                          <XCircle className="h-5 w-5" /> Needs work
                        </>
                      )}
                    </div>
                    <p className="text-sm text-muted-foreground">{checkResult.feedback}</p>
                  </div>
                ) : (
                  <div className="rounded-2xl border p-4 text-sm text-muted-foreground">
                    Submit your SQL to get correctness feedback.
                  </div>
                )}
              </CardContent>

              <CardContent>
                {checkResult?.aiFeedback && (
                  <div className="mt-3 rounded-xl border bg-muted/30 p-3 text-sm">
                    <div className="font-medium mb-1">AI explanation</div>
                    <div className="text-muted-foreground">{checkResult.aiFeedback}</div>
                  </div>
                )}
              </CardContent>

              <CardContent>
                {isCheckingAnswer && !checkResult && (
                  <div className="rounded-2xl border p-4 text-sm text-muted-foreground">
                    Checking your query and generating AI feedback...
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </motion.div>
      </div>
    </div>
  );
}