#!/usr/bin/python3
import socket
from loguru import logger

logger.add("/var/log/family_feud_server.log")

def family_feud_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5020))
    server.listen(100)
    print("Family Feud started. Waiting for connections..")

    while True:
        client, addr = server.accept()
        handle_client(client, addr)

def handle_client(client,addr):

    # data = client.recv(1024)
    # logger.info(f"Received message from {addr}:{data}\n")

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

    action_response = client.recv(1024)
    logger.info(action_response.decode("utf-8"))


@logger.catch
def main():
    family_feud_server()

if __name__ == "__main__":
    family_feud_server()
