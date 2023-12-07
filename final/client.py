import socket

def family_feud_client():
    MESSAGE=b"Hellow"
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("54.215.236.176", 5020))
    client.send(MESSAGE)
    data = client.recv(1024)
    print(data.decode('utf-8'))
    client.close()
if __name__ == "__main__":
    family_feud_client()
