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
create_database()

new_questions = [
{
    "prompt": "Name a food that people usually eat with their hands.",
    "guesses": [
        {"guess": "pizza", "score": 30},
        {"guess": "hamburger", "score": 25},
        {"guess": "sandwich", "score": 15},
        {"guess": "chicken wings", "score": 12},
        {"guess": "french fries", "score": 8},
    ]
},
{
    "prompt": "What's a type of dance move?",
    "guesses": [
        {"guess": "twirl", "score": 30},
        {"guess": "moonwalk", "score": 20},
        {"guess": "spin", "score": 15},
        {"guess": "dip", "score": 10},
        {"guess": "shuffle", "score": 5}
    ]
},
{
    "prompt": "Name a funny noise.",
    "guesses": [
        {"guess": "snicker", "score": 30},
        {"guess": "giggle", "score": 20},
        {"guess": "snort", "score": 15},
        {"guess": "chortle", "score": 10},
        {"guess": "whoopee", "score": 5}
    ]
},
{
    "prompt": "Name a silly thing to do with spaghetti.",
    "guesses": [
        {"guess": "slurp", "score": 30},
        {"guess": "twirl", "score": 20},
        {"guess": "noodle dance", "score": 15},
        {"guess": "spaghetti art", "score": 10},
        {"guess": "spaghetti hair", "score": 5}
    ]
}
]

# Insert the new questions into the database
for question in new_questions:
    insert_question(question["prompt"], question["guesses"])