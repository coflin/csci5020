#!/usr/bin/python3
import sqlite3

"""
Creates a questions.db database and adds questions to it. 

Format: 
{
    "prompt": "Question1",
    "guesses": [
        {"guess": "guess 1", "score": 62},
        {"guess": "guess 2", "score": 50},
        {"guess": "guess 3", "score": 12},
        {"guess": "guess 4", "score": 5},
        {"guess": "guess 5", "score": 4},
    ]
}

"""


def create_database(db_file):
    """Create the SQLite database and the necessary table."""
    conn = sqlite3.connect(db_file)
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

def insert_question(db_file, prompt, guesses):
    conn = sqlite3.connect(db_file)
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

def main():
    # Define the database file
    db_file = "questions.db"

    # Check if the database file exists, create it if not
    create_database(db_file)

    new_questions = [
        {
            "prompt": "Name something a movie hero will see in a haunted house.",
            "guesses": [
                {"guess": "ghosts", "score": 41},
                {"guess": "spiders", "score": 14},
                {"guess": "dead", "score": 13},
                {"guess": "skeletons", "score": 6},
                {"guess": "blood", "score": 5},
            ]
        },
        {
            "prompt": "Name a way an egg could be prepared that also describes your boss.",
            "guesses": [
                {"guess": "scrambled", "score": 39},
                {"guess": "fried", "score": 26},
                {"guess": "sunny-side up", "score": 14},
                {"guess": "runny", "score": 12},
                {"guess": "over easy", "score": 9},
            ]
        },
        {
            "prompt": "Name someone the dog complains about to the pet psychologist.",
            "guesses": [
                {"guess": "cat", "score": 35},
                {"guess": "owner", "score": 30},
                {"guess": "mailman", "score": 10},
                {"guess": "kids", "score": 7},
                {"guess": "vet", "score": 7},
            ]
        },
        {
            "prompt": "Name a reason you cover your mouth.",
            "guesses": [
                {"guess": "cough", "score": 69},
                {"guess": "sneeze", "score": 50},
                {"guess": "yawn", "score": 12},
                {"guess": "yellow teeth", "score": 5},
                {"guess": "shock", "score": 4},
            ]
        },
        {
            "prompt": "Name something you bought and then suffered buyer's remorse.",
            "guesses": [
                {"guess": "car", "score": 48},
                {"guess": "clothes", "score": 20},
                {"guess": "house", "score": 7},
                {"guess": "food", "score": 3},
                {"guess": "pet", "score": 1},
            ]
        }
    ]

    # Insert the new questions into the database
    for question in new_questions:
        insert_question(db_file, question["prompt"], question["guesses"])

if __name__ == "__main__":
    main()