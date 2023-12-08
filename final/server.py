#!/usr/bin/python3
import socket
from loguru import logger

logger.add("/var/log/family_feud_server.log")

def family_feud_server(server):

    while True:
        client, addr = server.accept()
        handle_client(client, addr)

def handle_client(client,addr):

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
""" + "\033[0m" + "What is your name?"
    client.sendall(welcome_message.encode('utf-8'))

    username = client.recv(1024)
    logger.info(f" Player 1: {username.decode('utf-8')}")

    hello_message = b"Hello " + username
    client.sendall(hello_message)

@logger.catch
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5020))
    server.listen(100)
    print("Family Feud started. Waiting for connections..")
    family_feud_server(server)

if __name__ == "__main__":
    main()
