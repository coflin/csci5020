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
        
        score = 0
        guesses = []

        # Receive and print the client's name
        username = client_socket.recv(1024).decode("utf-8")
        print(f"Client {username} connected.")
        
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
        question = get_random_question()
        client_socket.send(f"Question: {question['prompt']}\n".encode("utf-8"))
                
        # Simulate receiving the client's response
        time.sleep(1)
        for i in range(1,6):
            client_socket.send(f"Guess {i}: ".encode("utf-8"))
            guess = client_socket.recv(1024).decode("utf-8")
            guesses.append(guess)
        logger.info(f"Client {username} answered: {guesses}")

        #score = calculate_score(question,score,guesses)
        client_socket.send(f"Your score is: {score}".encode("utf-8"))
        
    except Exception as e:
        logger.error(f"Error handling client: {e}")
    
    finally:
        # Close the client socket
        client_socket.close()

def calculate_score(question,score,guesses):
    for guess in guesses:
        for i in range(1,6):
            if guess == question[f'guess{i}']:
                score += question[f'guess{i}_score']
    return score

def get_random_question():
    """Gets and returns a random question from the list"""
    conn = sqlite3.connect("/home/ubuntu/csci5020/final/questions.db")
    cursor = conn.cursor()
    logger.info("connected to database")
    cursor.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 1;")
    question_data = cursor.fetchone()
    logger.info(f"Question data: {question_data}")
    # Convert the question data into a dictionary
    columns = [column[0] for column in cursor.description]
    question = dict(zip(columns, question_data))

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