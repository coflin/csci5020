import socket
import threading
import json
import time
from loguru import logger

# Add your EC2 instance's public IP and port here
SERVER_IP = "54.215.236.176"
SERVER_PORT = 5020

questions = [
    {"prompt": "What is the capital of France?", "answer": "Paris"},
    {"prompt": "What is 2 + 2?", "answer": "4"},
    # Add more questions as needed
]

clients = []


def handle_client(client_socket, username):
    """Handles an incoming client connection"""

    try:
        # Send a welcome message
        send(client_socket, {"message": f"Hello {username}!"})

        # Wait for both clients to connect
        while len(clients) < 2:
            time.sleep(1)

        # Send a starting game message
        send(client_socket, {"message": "Starting game in 3..2..1.."})

        # Get a random question and send it to both clients
        question = get_random_question()
        send(client_socket, {"prompt": question["prompt"]})

        # Wait for both clients to answer the question
        while len(clients) > 0:
            time.sleep(1)

        # Implement scoring logic here if needed

    except Exception as e:
        logger.error(f"Error handling client {username}: {e}")

    finally:
        # Close the client socket
        client_socket.close()


def get_random_question():
    """Gets and returns a random question from the list"""
    return questions[0]  # Replace this with logic to get a random question


def send(client_socket, message):
    """Converts the dictionary to a JSON string and sends it to the client"""
    json_message = json.dumps(message)
    client_socket.send(json_message.encode())


def main():
    # Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the server socket to the IP and port
    server_socket.bind((SERVER_IP, SERVER_PORT))

    # Listen for incoming connections
    server_socket.listen(2)
    logger.info(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

    try:
        # Accept incoming connections
        while True:
            client, address = server_socket.accept()
            logger.info(f"Accepted connection from {address}")

            # Prompt the client for their name
            send(client, {"message": "Enter your name:"})
            username = receive(client)["name"]

            # Add the client to the list
            clients.append(client)

            # Start a new thread to handle the client
            threading.Thread(target=handle_client, args=(client, username)).start()

    except Exception as e:
        logger.info(f"Error in main loop: {e}")

    finally:
        server_socket.close()


def receive(client_socket):
    """Receives a JSON string from the client and converts it to a dictionary"""
    json_string = client_socket.recv(1024).decode("utf-8")
    return json.loads(json_string)


if __name__ == "__main__":
    main()
