import socket

def family_feud_client():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("54.215.236.176", 5020))

    welcome_message = client.recv(1024)
    print(welcome_message.decode('utf-8'))

    action = input("1. Create a room\n2. Join a room")
    client.send(action.encode('utf-8'))
    
if __name__ == "__main__":
    family_feud_client()
