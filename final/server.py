#!/usr/bin/python3
import socket

def family_feud_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5020))
    server.listen(100)
    print("Family Feud started. Waiting for connections..")

    while True:
        client, addr = server.accept()
        welcome_client(client,addr)

def welcome_client(client,addr):

    data = client.recv(1024)
    with open('/var/log/family_feud.log', 'a') as log_file:
        log_file.write(f"Received message from {addr}:{data}\n")

    welcome_message = "\033[92m" + """ 
__        __   _                            _        
\ \      / /__| | ___ ___  _ __ ___   ___  | |_ ___  
 \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \ 
  \ V  V /  __/ | (_| (_) | | | | | |  __/ | || (_) |
   \_/\_/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/ 
                                                     
 _____               _ _         _____              _ _ 
|  ___|_ _ _ __ ___ (_) |_   _  |  ___|__ _   _  __| | |
| |_ / _` | '_ ` _ \| | | | | | | |_ / _ \ | | |/ _` | |
|  _| (_| | | | | | | | | |_| | |  _|  __/ |_| | (_| |_|
|_|  \__,_|_| |_| |_|_|_|\__, | |_|  \___|\__,_|\__,_(_)
                         |___/                          
""" + "\033[0m"
    client.send(welcome_message.encode('utf-8'))
    user = input("Start Game? Y/N")
    client.send(user.encode('utf-8'))

if __name__ == "__main__":
    family_feud_server()
