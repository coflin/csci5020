import socket
import threading
import time
import sqlite3
from loguru import logger

logger.add("/var/log/family_feud_server.log")

def handle_client(client_socket,clients):
    try:
        
        # Send a welcome message
        client_socket.send(b"Enter your username: ")
        
        used_questions = []
        guesses = []

        # Receive and print the client's name
        username = client_socket.recv(1024).decode("utf-8")
        print(f"Client {username} connected.")
        player_score = {username: 0}

        # Add the client to the list
        clients.append(client_socket)
        
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
            client_socket.send(f"Question {question_number}: {question['prompt']}\n".encode("utf-8"))
                    
            # Simulate receiving the client's response
            time.sleep(1)
            for i in range(1,6):
                client_socket.send(f"Guess {i}: ".encode("utf-8"))
                guess = client_socket.recv(1024).decode("utf-8")
                guesses.append(guess)
            logger.info(f"Client {username} answered: {guesses}")

            question_score = calculate_score(question,guesses)
            client_socket.send(f"Your score for this question is: {question_score}".encode("utf-8"))
            
            total_score = update_score(player_score,username,question_score)
            client_socket.send(f"Your score so far: {total_score}\n\n".encode("utf-8"))

    except Exception as e:
        logger.error(f"Error handling client: {e}")
    
    finally:
        # Close the client socket
        client_socket.close()

def calculate_score(question,guesses):
    for guess in guesses:
        for i in range(1,6):
            logger.info(question[f'guess{i}'])
            if guess.strip() == question[f'guess{i}']:
                score = question[f'guess{i}_score']
                logger.info(f"SCORE: {score}")
    return score

def update_score(player_score,username,question_score):
    total_score = player_score[username]+question_score
    player_score = {username:total_score}
    return player_score


def get_random_question(used_questions):
    """Gets and returns a random question that has not been used before"""
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()
    logger.info("connected to database")

    # Get all questions
    cursor.execute("SELECT * FROM questions;")
    all_questions = cursor.fetchall()

    # Filter out used questions
    available_questions = [q for q in all_questions if q['prompt'] not in used_questions]

    if not available_questions:
        # Reset used questions if all have been used
        used_questions.clear()
        available_questions = all_questions

    # Select a random question from available questions
    question = random.choice(available_questions)

    # Add the used question to the list
    used_questions.append(question['prompt'])

    conn.close()
    logger.info(f"Question: {question}")
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