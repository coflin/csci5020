import socket
import selectors
from loguru import logger

logger.add("/var/log/family_feud_server.log")
sel = selectors.DefaultSelector()

class Connection:
    def __init__(self, sock, addr):
        self.sock = sock
        self.addr = addr
        self.sock.setblocking(False)
        self.inb = b""
        self.outb = b""

def accept_wrapper(sock):
    conn, addr = sock.accept()
    logger.info(f"Accepted connection from {addr}")
    
    connection = Connection(conn, addr)
    welcome_message = "\033[92m" + """ 
__        __   _                            _        
\ \      / /__| | ___ ___  _ __ ___   ___  | |_ ___  
 \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \ 
  \ V  V /  __/ | (_| (_) | | | | | |  __/ | || (_) |
   \_/\_/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/ 
                                                     
 ____             _             _____              _ _ 
/ ___| _ __   ___| |__   __ _  |  ___|__ _   _  __| | |
\___ \| '_ \ / _ \ '_ \ / _` | | |_ / _ \ | | |/ _` | |
 ___) | | | |  __/ | | | (_| | |  _|  __/ |_| | (_| |_|
|____/|_| |_|\___|_| |_|\__,_| |_|  \___|\__,_|\__,_(_)

    """ + "\033[0m" + "What is your name? "
    
    conn.sendall(welcome_message.encode('utf-8'))
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=connection)

    handle_client(connection)

def service_connection(key, mask):
    connection = key.data
    sock = connection.sock

    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            connection.inb += recv_data
        else:
            print(f"Closing connection to {connection.addr}")
            sel.unregister(sock)
            sock.close()

    if mask & selectors.EVENT_WRITE:
        if connection.outb:
            logger.info(f"Echoing {connection.outb!r} to {connection.addr}")
            sent = sock.send(connection.outb)
            connection.outb = connection.outb[sent:]

def handle_client(connection):
    try:
        connection.sock.sendall("What is your name? ".encode('utf-8'))
        username = connection.sock.recv(1024).decode('utf-8').strip()

        response = f"Hello {username}! Let's play Sneha Feud!\n Do you want to create or join a room? "
        connection.sock.sendall(response.encode('utf-8'))
        action = connection.sock.recv(1024).decode('utf-8').strip()

        # while True:
        #     data = connection.sock.recv(1024)
        #     if not data:
        #         logger.error(f"Connection closed by {connection.addr}")
        #         break
        #     response = process_data(data)
        #     connection.sock.sendall(response.encode('utf-8'))
                
    except Exception as e:
        logger.error(f"Exception in handle_client for {connection.addr}: {e}")

    finally:
        sel.unregister(connection.sock)
        connection.sock.close()

def process_data(data):
    # Implement your logic to process the received data and generate a response
    # This is where you can handle different commands or game-related interactions
    # Modify this function according to your requirements
    if data.decode('utf-8') == "create":
        return f"{data.decode('utf-8')}ing room"
    elif data.decode('utf-8') == "join":
        return f"{data.decode('utf-8')}ing room"
    else:
        return f"Error! Type either 'create or join' to create or join a room"
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5020))
    server.listen()
    print("Family Feud started. Waiting for connections..")
    server.setblocking(False)
    sel.register(server, selectors.EVENT_READ, data=None)

    try:
        while True:
            events = sel.select()
            for key, mask in events:
                logger.info(f"key:{key}")
                logger.info(f"mask:{mask}")
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    service_connection(key, mask)
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        sel.close()

if __name__ == "__main__":
    main()
