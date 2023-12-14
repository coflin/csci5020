import socket
import threading
import time
import sqlite3
from loguru import logger

logger.add("/var/log/family_feud_server.log")

# Use threading.Lock to synchronize access to shared resources
scores_lock = threading.Lock()


def handle_client(client_socket, clients, barrier):
    """
    Handles communication with a connected client.

    Args:
        client_socket (socket.socket): The socket object for the client.
        clients (list): List of connected clients.
        barrier (threading.Barrier): Synchronization barrier.

    Returns:
        None
    """
    try:
        # Send a welcome message
        client_socket.send(
            b"""\033[93m
__          __  _                            _        
\ \        / / | |                          | |       
 \ \  /\  / /__| | ___ ___  _ __ ___   ___  | |_ ___  
  \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \ 
   \  /\  /  __/ | (_| (_) | | | | | |  __/ | || (_) |
    \/  \/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/ 
                                                      
                                                      
  _____            _           _       ______              _ _       
 / ____|          | |         ( )     |  ____|            (_) |      
| (___  _ __   ___| |__   __ _|/ ___  | |__ __ _ _ __ ___  _| |_   _ 
 \___ \| '_ \ / _ \ '_ \ / _` | / __| |  __/ _` | '_ ` _ \| | | | | |
 ____) | | | |  __/ | | | (_| | \__ \ | | | (_| | | | | | | | | |_| |
|_____/|_| |_|\___|_| |_|\__,_| |___/ |_|  \__,_|_| |_| |_|_|_|\__, |
                                                                __/ |
                                                               |___/ 
 ______             _ 
|  ____|           | |
| |__ ___ _   _  __| |
|  __/ _ \ | | |/ _` |
| | |  __/ |_| | (_| |
|_|  \___|\__,_|\__,_|
                                    
\033[0m                          
 \n\033[92mAuthor: Sneha Irukuvajjula\033[0m   

\n\033[93m\033[1mGame Setup \033[0m\033[0m \n
Two players are part of the game. A survey was conducted with around 100 people,\n 
and the top 5 responses to various questions were collected.
                           
\n\033[93m\033[1mObjective \033[0m\033[0m \n
Players aim to guess the top 5 most popular answers to these survey questions.
                           
\n\033[93m\033[1mGame Play \033[0m\033[0m \n
Players will be presented with questions from the survey.\n
They need to guess the top 5 answers in order of popularity within 30 seconds.\n
The order in which players guess does not matter as long as the answer is one among the top 5.
                           
\n\033[93m\033[1mScoring \033[0m\033[0m \n
Points are awarded based on the popularity of the guessed answers.\n
The most popular answer earns the highest points, followed by decreasing points for the subsequent answers.
                           
\n\033[93m\033[1mWinning \033[0m\033[0m \n
The player with the highest total points at the end of the game wins! Have fun!
\n\033[93m\033[1mLet's play Sneha's Family Feud!\033[0m\033[0m
"""
        )

        time.sleep(1)
        client_socket.send(b"\n\n Enter your name: ")

        used_questions = []
        guesses = []

        # Receive and print the client's name
        username = client_socket.recv(1024).decode("utf-8").strip()
        logger.info(f"Client {username} connected.")

        # Add the client to the list
        clients.append((client_socket, username))
        player_scores = [{username: 0} for _, username in clients]
        logger.info(f"CLIENT INFO:{player_scores}")

        # Wait for 2 players to join
        client_socket.send(b"Waiting for another player to join..\n")
        barrier.wait()

        # Send a starting game message
        client_socket.send(b"All players have joined. Starting game in\n")
        for i in range(3, 0, -1):
            time.sleep(1)
            client_socket.send(f"{i}..\n".encode("utf-8"))

        # Get a random question and send it to the client
        for question_number in range(1, 6):
            question = get_next_question(used_questions)
            client_socket.send(
                f"\n\n\033[37m\033[1mQuestion {question_number}: {question['prompt']}\033[0m\033[0m".encode(
                    "utf-8"
                )
            )

            # Simulate receiving the client's response
            time.sleep(1)

            # Set a 30-second time limit for the user to answer
            time_limit = 30  # in seconds
            start_time = time.time()

            for i in range(1, 6):
                client_socket.send(f"\n\033[93mGuess {i}:\033[0m ".encode("utf-8"))
                guess = client_socket.recv(1024).decode("utf-8")

                if time.time() - start_time > time_limit:
                    client_socket.send(b"\033[91mTime's up! Moving to the next question.\033[0m\n")
                    break

                guesses.append(guess)

            logger.info(f"Client {username} answered: {guesses}")
            logger.info(f"{player_scores}")

            question_score = calculate_score(question, guesses)
            with scores_lock:
                for player_score in player_scores:
                    if username == list(player_score.keys())[0]:
                        player_score[username] += question_score
            client_socket.send(
                f"\033[92mYour score for this question is: {question_score}\033[0m\n".encode(
                    "utf-8"
                )
            )
            time.sleep(1)
            client_socket.send(
                f"\033[93mYour total score so far: {player_score[username]}\033[0m\n\n".encode(
                    "utf-8"
                )
            )
            time.sleep(1)

            # Wait for all players to finish before moving to the next question
            barrier.wait()

        final_score = print_in_box(f"Your final score: {player_score[username]}")

        client_socket.send(f"{final_score}\n\n".encode("utf-8"))
        time.sleep(1)
        client_socket.send(b"Thanks for playing this game. Good bye! :) ")

    except Exception as e:
        import traceback

        traceback.print_exc()
        logger.error(f"Error handling client: {e}")

    finally:
        # Close the client socket
        client_socket.close()


def calculate_score(question, guesses):
    """
    Calculates the score for a given question and set of guesses.

    Args:
        question (dict): The question data from the database.
        guesses (list): List of guesses provided by the player.

    Returns:
        int: The calculated score for the question.
    """
    score = 0
    for guess in guesses:
        for i in range(1, 6):
            if guess.strip().lower() == question[f"guess{i}"]:
                logger.info(question[f"guess{i}"])
                score += question[f"guess{i}_score"]
    logger.info(f"SCORE: {score}")
    return score


def get_next_question(used_questions):
    """
    Gets the next question sequentially from the database.

    Args:
        used_questions (list): List of questions already used.

    Returns:
        dict: The next question from the database.
    """

    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()
    logger.info("connected to database")

    # Get all questions
    cursor.execute("SELECT * FROM questions;")
    all_questions = cursor.fetchall()

    # Convert rows to dictionaries for easier access
    questions_dict_list = []
    for row in all_questions:
        columns = [column[0] for column in cursor.description]
        question_dict = dict(zip(columns, row))
        questions_dict_list.append(question_dict)

    # Filter out used questions
    available_questions = [
        q for q in questions_dict_list if q["prompt"] not in used_questions
    ]

    if not available_questions:
        # Reset used questions if all have been used
        used_questions.clear()
        available_questions = questions_dict_list

    # Select a random question from available questions
    question = available_questions[len(used_questions) % len(available_questions)]

    # Add the used question to the list
    used_questions.append(question["prompt"])

    conn.close()
    return question


def print_in_box(text):
    """
    Formats a message in a styled box.

    Args:
        text (str): The text message to be formatted.

    Returns:
        str: The formatted message in a box.
    """
    box_width = len(text) + 4  # Adjust the width based on the length of the text
    horizontal_line = "+" + "-" * (box_width - 2) + "+"
    box_string = f"\033[1;92m{horizontal_line}\n| {text} |\n{horizontal_line}\033[0m"
    return box_string


barrier = threading.Barrier(2)


@logger.catch()
def main():
    # Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    SERVER_IP = "0.0.0.0"
    SERVER_PORT = 5020

    # Bind the server socket to the IP and port
    server_socket.bind((SERVER_IP, SERVER_PORT))

    # Listen for incoming connections
    server_socket.listen(2)
    logger.info(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

    clients = []

    try:
        # Accept incoming connections
        while True:
            client, address = server_socket.accept()
            print(f"Accepted connection from {address}")

            # Start a new thread to handle the client
            threading.Thread(
                target=handle_client, args=(client, clients, barrier)
            ).start()

            # If two clients have connected, reset the barrier for the next round
            if len(clients) == 2:
                barrier.reset()

    except Exception as e:
        print(f"Error in main loop: {e}")

    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
