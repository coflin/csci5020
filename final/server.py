import socket
import selectors
from loguru import logger

logger.add("/var/log/family_feud_server.log")
sel = selectors.DefaultSelector()

class Connection:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.conn.setblocking(False)
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
            print(f"Echoing {connection.outb!r} to {connection.addr}")
            sent = sock.send(connection.outb)
            connection.outb = connection.outb[sent:]
            handle_client(connection)

def handle_client(connection):
    try:
        # Add your custom logic here based on connection.inb
        response = f"Hello {connection.inb.decode('utf-8')}! Let's play Sneha Feud!"
        connection.sock.sendall(response.encode('utf-8'))
    except Exception as e:
        logger.error(f"Exception in handle_client for {connection.addr}: {e}")
    finally:
        sel.unregister(connection.sock)
        connection.sock.close()

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
