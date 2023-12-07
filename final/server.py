#!/usr/bin/python3
import socket
from termcolor import colored

def family_feud_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5020))
    server.listen(100)
    print("Family Feud started. Waiting for connection..")

    while True:
        client, addr = server.accept()
        handle_client(client,addr)

        client.send(b"{console.log(MESSAGE)}")


def handle_client(client,addr):

    data = client.recv(1024)
    with open('/var/log/family_feud.log', 'a') as log_file:
        log_file.write(f"Received message from {addr}:{data}\n")

    welcome_message = "Welcome to Family Feud!\n Author: Sneha Irukuvajjula\n Created: Dec 7, 2023"



if __name__ == "__main__":
    family_feud_server()
