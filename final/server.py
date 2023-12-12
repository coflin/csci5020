import socket
import threading
import time
from loguru import logger


logger.add("/var/log/family_feud_server.log")

questions = ["Question 1", "Question 2", "Question 3"]
current_question_index = 0
#start_game_event = threading.Event()

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
    #start_game_event.set()

def handle_client(client_socket, client_id):
    # Send welcome message
    welcome_message = """\033[92m
__        __   _                            _        
\ \      / /__| | ___ ___  _ __ ___   ___  | |_ ___  
 \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \ 
  \ V  V /  __/ | (_| (_) | | | | | |  __/ | || (_) |
   \_/\_/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/ 
                                                     
 ____             _           _     
/ ___| _ __   ___| |__   __ _( )___ 
\___ \| '_ \ / _ \ '_ \ / _` |// __|
 ___) | | | |  __/ | | | (_| | \__ \
|____/|_| |_|\___|_| |_|\__,_| |___/
                                    
 _____               _ _         _____              _ 
|  ___|_ _ _ __ ___ (_) |_   _  |  ___|__ _   _  __| |
| |_ / _` | '_ ` _ \| | | | | | | |_ / _ \ | | |/ _` |
|  _| (_| | | | | | | | | |_| | |  _|  __/ |_| | (_| |
|_|  \__,_|_| |_| |_|_|_|\__, | |_|  \___|\__,_|\__,_|
                         |___/                        
                                                       
\033[0m""" + "\n Enter a username: "
    
    client_socket.sendall(welcome_message.encode('utf-8'))

    # Receive and print the user's name
    user_name = client_socket.recv(1024).decode('utf-8').strip()
    print(f"Client {client_id}: {user_name} connected")

    player_dict = {"username": user_name, "socket": client_socket}
    players.append(player_dict)
    
    logger.info(f"Players list: {players}")

    # Send personalized greeting and prompt to create/join a room
    greeting = f"Hello {user_name}!"
    client_socket.sendall(greeting.encode('utf-8'))

    while len(players) < 2:
        time.sleep(1)

    creator = players[0]
    player2 = players[1]

    logger.info(f"creator:{creator}\nplayer2:{player2}")

        # Notify the creator to start the game
    creator["socket"].sendall("Type 'start' to begin the game: ".encode('utf-8'))

    player2["socket"].sendall("Waiting for the creator to start the game")
    start_game_response = creator["socket"].recv(1024).decode('utf-8').strip().lower()


        # if start_game_response == "start":
        #     # Notify both players to start the game
        #     countdown_threads = []
        #     for player in players:
        #         player["socket"].sendall("The game is starting!".encode('utf-8'))
        #         player["socket"].sendall("Game starting in...".encode('utf-8'))
        #         countdown_thread_creator = threading.Thread(target=countdown, args=(player["socket"],))
        #         countdown_thread_creator.start()
        #         countdown_threads.append(countdown_thread_creator)

        #     # Wait for the countdown threads to finish
        #     for thread in countdown_threads:
        #         thread.join()

            # Send the first question to both players
    question = get_next_question()
    for player in players:
        player["socket"].sendall(f"Your question is: {question}".encode('utf-8'))

        # elif response.lower() == "join":
        #     client_socket.sendall("Ok! Joining a room...\n".encode('utf-8'))

            # Notify the joiner to wait for the creator
            # client_socket.sendall("Waiting for the creator to start the game...".encode('utf-8'))

            # # Wait for the creator to start the game
            # start_game_event.wait()

            # # Send countdown to the joiner
            # client_socket.sendall("Game starting in...".encode('utf-8'))
            # countdown_thread_joiner = threading.Thread(target=countdown, args=(client_socket,))
            # countdown_thread_joiner.start()

            # Wait for the countdown to finish
            # countdown_thread_joiner.join()

            # # Send the first question to the joiner
            # question = get_next_question()
            # client_socket.sendall(f"Your question is: {question}".encode('utf-8'))


@logger.catch
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5020))
    server.listen(4)  # Listen for up to 20 connections

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