import socket
import threading
import time
from loguru import logger


logger.add("/var/log/family_feud_server.log")

questions = ["Question 1", "Question 2", "Question 3"]
current_question_index = 0
start_game_event = threading.Event()

players = []

def get_next_question():
    global current_question_index
    if current_question_index < len(questions):
        question = questions[current_question_index]
        current_question_index += 1
        return question
    else:
        return None

def countdown(client_socket):
    for i in range(3, 0, -1):
        time.sleep(1)
        client_socket.sendall(str(i).encode('utf-8'))

    # Notify that the countdown is over
    start_game_event.set()

def handle_client(client_socket, client_id):
    # Send welcome message
    client_socket.sendall("Welcome to Family Feud! What is your name? ".encode('utf-8'))

    # Receive and print the user's name
    user_name = client_socket.recv(1024).decode('utf-8').strip()
    print(f"Client {client_id}: {user_name} connected")

    for player in players:
            player_dict = {"username": user_name, "socket": client_socket}
            players.append(player_dict)
    logger.info(f"Players list: {players}")

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
        client_socket.sendall("Ok! Creating a room..".encode('utf-8'))

        #while len(players) < 2:
        time.sleep(3)

        client_socket.sendall("Start game?".encode('utf-8'))
        
        # Notify both players to start the game
        for player in players:
            if player["socket"] != client_socket:
                player["socket"].sendall("Start game?".encode('utf-8'))

        # Wait for both players to agree to start the game
        start_game_event.wait()

        # Send countdown to both players
        for player in players:
            player["socket"].sendall("Game starting in...".encode('utf-8'))
            countdown_thread = threading.Thread(target=countdown, args=(player["socket"],))
            countdown_thread.start()

        # Wait for the countdown to finish
        countdown_thread.join()

        # Send the first question to both players
        question = get_next_question()
        for player in players:
            player["socket"].sendall(f"Your question is: {question}".encode('utf-8'))

    elif response.lower() == "join":
        client_socket.sendall("Ok! Joining a room!".encode('utf-8'))

        # Wait for the other player to create the room

        # Notify both players to start the game
        for player in players:
            player["socket"].sendall("Start game? (yes/no) ".encode('utf-8'))

        # Wait for both players to agree to start the game
        start_game_event.wait()

        # Send countdown to both players
        for player in players:
            player["socket"].sendall("Game starting in...".encode('utf-8'))
            countdown_thread = threading.Thread(target=countdown, args=(player["socket"],))
            countdown_thread.start()

        # Wait for the countdown to finish
        countdown_thread.join()

        # Send the first question to both players
        question = get_next_question()
        for player in players:
            player["socket"].sendall(f"Your question is: {question}".encode('utf-8'))

@logger.catch
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5020))
    server.listen(20)  # Listen for up to 2 connections

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