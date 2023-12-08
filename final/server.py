import socket
import threading

def handle_client(client_socket, client_id):
    # Send welcome message
    client_socket.sendall("Welcome to Family Feud! What is your name? ".encode('utf-8'))

    # Receive and print the user's name
    user_name = client_socket.recv(1024).decode('utf-8').strip()
    print(f"Client {client_id}: {user_name} connected")

    # Send personalized greeting and prompt to create/join a room
    greeting = f"Hello {user_name}! Do you want to create or join a room? "
    client_socket.sendall(greeting.encode('utf-8'))

    # Receive user's response (create/join)
    response = client_socket.recv(1024).decode('utf-8').strip()

    # Process user's response
    if response.lower() == "create":
        client_socket.sendall("Ok! Creating a room!".encode('utf-8'))
        # Implement logic for creating a room here
    else:
        client_socket.sendall("Invalid response. Connection closed.".encode('utf-8'))
    
    # Close the connection
    client_socket.close()
    print(f"Client {client_id}: Connection closed")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5020))
    server.listen(2)  # Listen for up to 2 connections

    print("Family Feud server started. Waiting for connections...")

    client_id = 1  # Client identifier

    while True:
        client_socket, client_addr = server.accept()

        # Handle each client in a separate thread
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_id))
        client_thread.start()

        client_id += 1

if __name__ == "__main__":
    main()