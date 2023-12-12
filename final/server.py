import socket
import threading
import time

SERVER_IP = '0.0.0.0'  # Listen on all available interfaces
SERVER_PORT = 5020

questions = [
    {"prompt": "What is the capital of France?", "answer": "Paris"},
    {"prompt": "What is 2 + 2?", "answer": "4"},
]

clients = []

def handle_client(client_socket):
    try:
        # Send a welcome message
        client_socket.send(b"Enter your name: ")
        
        # Receive and print the client's name
        username = client_socket.recv(1024).decode("utf-8")
        print(f"Client {username} connected.")
        
        # Add the client to the list
        clients.append(client_socket)
        
        # Wait for 2 players to join
        while len(clients) <2:
            time.sleep(1)

        # Send a starting game message
        client_socket.send(b"Starting game in 3..\n")
        time.sleep(3)
        
        # Get a random question and send it to the client
        question = get_random_question()
        client_socket.send(f"Question: {question['prompt']}\n".encode("utf-8"))
        
        # Simulate waiting for the client's response
        time.sleep(5)  # Adjust this delay as needed
        
        # Simulate receiving the client's response
        client_response = client_socket.recv(1024).decode("utf-8")
        print(f"Client {username} answered: {client_response}")
        
    except Exception as e:
        print(f"Error handling client: {e}")
    
    finally:
        # Close the client socket
        client_socket.close()

def get_random_question():
    """Gets and returns a random question from the list"""
    for question in questions:
        return question

def main():
    # Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the server socket to the IP and port
    server_socket.bind((SERVER_IP, SERVER_PORT))

    # Listen for incoming connections
    server_socket.listen(2)
    print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

    try:
        # Accept incoming connections
        while True:
            client, address = server_socket.accept()
            print(f"Accepted connection from {address}")

            # Start a new thread to handle the client
            threading.Thread(target=handle_client, args=(client,)).start()

    except Exception as e:
        print(f"Error in main loop: {e}")

    finally:
        server_socket.close()

if __name__ == "__main__":
    main()