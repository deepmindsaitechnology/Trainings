"""Backend functions for the Student Database Text2SQL conversational agent."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

import mysql.connector
import pandas as pd
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
SCHEMA_PATH = BASE_DIR / "db_schema.json"

# Strict block list: this application is only for reporting and QA.
_BLOCKED_SQL_WORDS = re.compile(
    r"\b(insert|update|delete|drop|alter|truncate|create|replace|grant|revoke|call|execute|load|outfile|dumpfile|into|lock|unlock|set|use)\b",
    flags=re.IGNORECASE,
)


def load_schema_metadata() -> dict[str, Any]:
    """Load table metadata used to ground the LLM in the real schema."""
    with SCHEMA_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_groq_client() -> Groq:
    """Create Groq SDK client using the key stored in .env."""
    api_key = os.getenv("GROQ_API_KEY", "").strip()

    if not api_key:
        raise ValueError(
            "Please add your Groq API key in the .env file as GROQ_API_KEY."
        )

    return Groq(api_key=api_key)


def get_db_connection():
    """Open a MySQL connection to source_db using .env values."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "source_db"),
    )


def _extract_json(text: str) -> dict[str, Any]:
    """Extract JSON even when the model accidentally wraps it in markdown."""
    clean_text = re.sub(
        r"```(?:json)?|```", "", text, flags=re.IGNORECASE
    ).strip()

    try:
        return json.loads(clean_text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", clean_text, flags=re.DOTALL)

        if not match:
            raise ValueError("LLM did not return valid JSON SQL output.")

        return json.loads(match.group(0))


def validate_read_only_sql(sql: str) -> str:
    """
    Allow exactly one read-only SELECT query.
    A default LIMIT 100 is added when the model does not provide a limit.
    """
    cleaned_sql = re.sub(
        r"```(?:sql)?|```", "", sql, flags=re.IGNORECASE
    ).strip().rstrip(";")

    if not cleaned_sql:
        raise ValueError("Generated SQL is empty.")

    if ";" in cleaned_sql:
        raise ValueError("Multiple SQL statements are not allowed.")

    if not re.match(r"^select\b", cleaned_sql, flags=re.IGNORECASE):
        raise ValueError("Only SELECT queries are allowed in this QA application.")

    if re.search(r"(--|/\*|\*/|#)", cleaned_sql):
        raise ValueError("SQL comments are not allowed.")

    if _BLOCKED_SQL_WORDS.search(cleaned_sql):
        raise ValueError(
            "Unsafe SQL keyword detected. Only read-only reporting is allowed."
        )

    if not re.search(r"\blimit\s+\d+\b", cleaned_sql, flags=re.IGNORECASE):
        cleaned_sql = f"{cleaned_sql}\nLIMIT 100"

    return cleaned_sql


def generate_sql(question: str, conversation_context: str = "") -> dict[str, str]:
    """Convert the user's natural language question into one MySQL SELECT query."""
    schema = load_schema_metadata()
    schema_text = json.dumps(schema, indent=2)
    model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    system_prompt = f"""
You are a precise Text-to-SQL assistant for a school database.
Create exactly one valid MySQL SELECT query from the user's question.

DATABASE SCHEMA METADATA:
{schema_text}

MANDATORY RULES:
1. Use only tables and columns defined in the schema metadata.
2. Generate SELECT statements only. Never generate INSERT, UPDATE, DELETE,
   DROP, ALTER, CREATE, TRUNCATE, SET, USE, procedures, or comments.
3. Never assume a relationship between teachers and students because no
   mapping table is available.
4. For marks joins, join:
   student_details.student_id = student_marks.student_id
5. Use backticks around the column `class` when needed:
   student_details.`class`
6. Use MySQL syntax.
7. For vague analytics questions, choose a sensible aggregation.
8. Return JSON only using this exact structure:
   {{"sql": "SELECT ...", "interpretation": "Brief description of what the SQL retrieves."}}
""".strip()

    user_prompt = f"""
Conversation context, only when useful:
{conversation_context or 'No previous context.'}

User question: {question}
""".strip()

    completion = get_groq_client().chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    output = _extract_json(completion.choices[0].message.content or "")
    safe_sql = validate_read_only_sql(str(output.get("sql", "")))
    interpretation = str(
        output.get("interpretation", "Generated SQL query.")
    )

    return {
        "sql": safe_sql,
        "interpretation": interpretation,
    }


def run_query(sql: str) -> pd.DataFrame:
    """Execute validated SQL and return the output as a DataFrame."""
    safe_sql = validate_read_only_sql(sql)

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(safe_sql)

        rows = cursor.fetchall()

        return pd.DataFrame(rows, columns=cursor.column_names)

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def generate_answer(question: str, sql: str, result_df: pd.DataFrame) -> str:
    """Convert SQL results into a natural-language response."""
    if result_df.empty:
        return "No matching records were found for your question."

    model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    result_preview = result_df.head(30).to_json(
        orient="records",
        date_format="iso",
    )

    prompt = f"""
You are answering a user's database question using already executed SQL results.
Answer only from the supplied result rows. Do not invent data.
Keep the response clear and compact.
Mention that displayed rows may be limited if relevant.

Question: {question}
SQL: {sql}
Rows returned: {len(result_df)}
Result preview: {result_preview}
""".strip()

    completion = get_groq_client().chat.completions.create(
        model=model,
        temperature=0.1,
        messages=[
            {
                "role": "system",
                "content": "You summarize database query results accurately.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return completion.choices[0].message.content or "Query executed successfully."


def ask_database(question: str, conversation_context: str = "") -> dict[str, Any]:
    """Complete Text2SQL pipeline: generate SQL, execute it, summarize results."""
    query_info = generate_sql(question, conversation_context)
    result_df = run_query(query_info["sql"])
    answer = generate_answer(question, query_info["sql"], result_df)

    return {
        "answer": answer,
        "sql": query_info["sql"],
        "interpretation": query_info["interpretation"],
        "data": result_df,
    }