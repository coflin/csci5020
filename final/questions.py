#!/usr/bin/python3
import sqlite3
import os

DB_FILE = "questions.db"

def create_database():
    """Create the SQLite database and the necessary table."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create the questions table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prompt TEXT,
        guess1 TEXT,
        guess1_score INTEGER,
        guess2 TEXT,
        guess2_score INTEGER,
        guess3 TEXT,
        guess3_score INTEGER,
        guess4 TEXT,
        guess4_score INTEGER,
        guess5 TEXT,
        guess5_score INTEGER
    )
    """)

    conn.commit()
    conn.close()

def insert_question(prompt, guesses):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Generate the SQL query for inserting a new question
    columns = ["prompt"] + [f"guess{i}" for i in range(1, 6)] + [f"guess{i}_score" for i in range(1, 6)]
    values = [prompt] + [guess["guess"] for guess in guesses] + [guess["score"] for guess in guesses]
    placeholders = ",".join(["?"] * len(columns))

    query = f"""
    INSERT INTO questions ({", ".join(columns)})
    VALUES ({placeholders})
    """

    # Execute the query
    cursor.execute(query, values)
    conn.commit()
    conn.close()

# Check if the database file exists, create it if not
if not os.path.exists(DB_FILE):
    create_database()

new_questions = [
    {
        "prompt": "What is the best honeymoon destination?",
        "guesses": [
            {"guess": "maldives", "score": 30},
            {"guess": "paris", "score": 20},
            {"guess": "hawaii", "score": 10},
            {"guess": "bali", "score": 5},
            {"guess": "switzerland", "score": 2}
        ]
    },
    {
        "prompt": "Words that end with at",
        "guesses": [
            {"guess": "fat", "score": 30},
            {"guess": "mat", "score": 20},
            {"guess": "rat", "score": 10},
            {"guess": "hat", "score": 5},
            {"guess": "pat", "score": 2}
        ]
    }
]

# Insert the new questions into the database
for question in new_questions:
    insert_question(question["prompt"], question["guesses"])