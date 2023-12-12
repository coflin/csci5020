import socket
from tabnanny import check
import threading
import time
import sqlite3
import random
from loguru import logger

logger.add("/var/log/family_feud_server.log")


def check_winner(username,player_scores):
    if player_scores[0][username] > player_scores[1][username]:
        return list(player_scores[0].keys())[0]
    elif player_scores[0][username] < player_scores[1][username]:
        return list(player_scores[1].keys())[0]
    else:
        return None

def handle_client(client_socket,clients):
    try:
        
        # Send a welcome message
        client_socket.send(b"Enter your username: ")
        
        used_questions = []
        guesses = []

        # Receive and print the client's name
        username = client_socket.recv(1024).decode("utf-8").strip()
        logger.info(f"Client {username} connected.")
        player_score={}
        player_scores = []

        # Add the client to the list
        clients.append((client_socket, username))
        for client, username in clients:
            player_scores.append({username: 0})
        logger.info(f"CLIENT INFO:{player_scores}")

        # Wait for 2 players to join
        while len(clients) <2:
            time.sleep(1)

        # Send a starting game message
        client_socket.send(b"Starting game in\n")
        for i in range(3,0,-1):
            time.sleep(1)
            client_socket.send(f"{i}..\n".encode("utf-8"))

        # Get a random question and send it to the client
        for question_number in range(1,3):
            question = get_random_question(used_questions)
            client_socket.send(f"\033[1mQuestion {question_number}: {question['prompt']}\033[0m\n".encode("utf-8"))
                    
            # Simulate receiving the client's response
            time.sleep(1)
            for i in range(1,6):
                client_socket.send(f"\033[93mGuess {i}:\033[0m ".encode("utf-8"))
                guess = client_socket.recv(1024).decode("utf-8")
                guesses.append(guess)
            logger.info(f"Client {username} answered: {guesses}")

            question_score = calculate_score(question,guesses)
            logger.info(f"QUESTION SCORE: {question_score}\n PLAYER SCORE: {player_score[username]}")
            player_score[username] += question_score
            logger.info(f"PLAYER SCORE: {player_score}")

            client_socket.send(f"\033[92mYour score for this question is: {question_score}\033[0m\n".encode("utf-8"))
            time.sleep(1)
            client_socket.send(f"\033[93mYour score so far: {player_score[username]}\033[0m\n\n".encode("utf-8"))
            time.sleep(1)

        winner = check_winner(username,player_scores)
        if winner:
            client_socket.send(f"{winner.upper()} WINS!".encode("utf-8"))
        else:
            client_socket.send(f"IT'S A TIE!".encode("utf-8"))

    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error(f"Error handling client: {e}")    
        
    finally:
        # Close the client socket
        client_socket.close()

def calculate_score(question,guesses):
    score = 0
    for guess in guesses:
        for i in range(1,6):
            if guess.strip().lower() == question[f'guess{i}']:
                logger.info(question[f'guess{i}'])
                score += question[f'guess{i}_score']
    logger.info(f"SCORE: {score}")
    return score

def get_random_question(used_questions):
    """Gets and returns a random question that has not been used before"""
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
    available_questions = [q for q in questions_dict_list if q["prompt"] not in used_questions]

    if not available_questions:
        # Reset used questions if all have been used
        used_questions.clear()
        available_questions = questions_dict_list

    # Select a random question from available questions
    question = random.choice(available_questions)

    # Add the used question to the list
    used_questions.append(question["prompt"])

    conn.close()
    return question

@logger.catch()
def main():
    # Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    SERVER_IP = '0.0.0.0'
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
            threading.Thread(target=handle_client, args=(client,clients)).start()

    except Exception as e:
        print(f"Error in main loop: {e}")

    finally:
        server_socket.close()

if __name__ == "__main__":
    main()