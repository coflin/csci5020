import socket
import threading
import random

players = []
questions = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10"]
used_questions = []

def handle_client(client_socket, client_id):
    # Send welcome message
    client_socket.sendall("Welcome to Family Feud! What is your name? ".encode('utf-8'))

    # Receive and print the user's name
    user_name = client_socket.recv(1024).decode('utf-8').strip()
    print(f"Client {client_id}: {user_name} connected")

    for player in players:
        if user_name == player["username"]:
            welcome_user = f"Welcome back, {user_name}\n"
            client_socket.sendall(welcome_user.encode('utf-8'))
            break
    else:
        player_dict = {"username": user_name}
        players.append(player_dict)

    # Send personalized greeting and prompt to create/join a room
    greeting = f"Hello {user_name}! Do you want to create or join a room? "
    client_socket.sendall(greeting.encode('utf-8'))

    # Receive user's response (create/join)
    response = client_socket.recv(1024).decode('utf-8').strip()

    # Process user's response
    while response.lower() != "create" and response.lower() != "join":
        client_socket.sendall("Invalid response. Please enter 'create' or 'join' ".encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8').strip()         

    if response.lower() == "create":
        client_socket.sendall("Ok! Creating a room!".encode('utf-8'))
        join_room(client_socket,user_name)

    elif response.lower() == "join":
        client_socket.sendall("Ok! Joining a room!".encode('utf-8'))  
        join_room(client_socket,user_name)

def join_room(client_socket,user_name):
    question = get_question()
    client_socket.sendall(f"Room Question:{question}".encode('utf-8'))

def get_question():
    question = random.choice(questions)
    used_questions.append(question)
    questions.remove(question)
    return question
 
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5020))
    server.listen(20)  # Listen for up to 2 connections

    print("Family Feud server started. Waiting for connections...")

    client_id = 1  # Client identifier

    while True:
        client_socket, client_addr = server.accept()

        #Handle each client in a seperate thread
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_id))
        client_thread.start()

        client_id += 1
    

if __name__ == "__main__":
    main()