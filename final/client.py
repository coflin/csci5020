import socket

def family_feud_client():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("54.215.236.176", 5020))

    #Welcome message from the server
    welcome_message = client.recv(1024)
    print(welcome_message.decode('utf-8'))

    #Start Game
    action = input("1. Create a room\n2. Join a room\n")
    while action != 1 or action != 2:
        print("Incorrect option. Try again.")
        action = input("1. Create a room\n2. Join a room\n")
    else:
        client.send(action.encode('utf-8'))
    
def main():
    family_feud_client()

if __name__ == "__main__":
    main()
