import socket
import selectors
import types
from loguru import logger

logger.add("/var/log/family_feud_server.log")
sel = selectors.DefaultSelector()

def accept_wrapper(sock):
    conn, addr = sock.accept()
    logger.info(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")

    # Welcome Message
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
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.outb += recv_data

            # Check if the data is complete
            if b'\n' in data.outb:
                # Call handle_client with the received data
                handle_client(sock, data.addr, data.outb.decode('utf-8').strip())
                
                # Reset outb for the next message
                data.outb = b""
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()

    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f"Echoing {data.outb!r} to {data.addr}")
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]

def handle_client(sock, addr, received_data):
    try:
        response = f"Hello {received_data}! Let's play Sneha Feud!\nDo you want to create a room or join a room? create/join "
        sock.sendall(response.encode('utf-8'))

        while True:
            response = sock.recv(1024).decode('utf-8').strip()

            if not response:
                # Client has closed the connection
                break

            if response == "create":
                action = "Creating a room"
            elif response == "join":
                action = "Joining a room"
            else:
                action = "Invalid response. Please enter 'create' or 'join'"

            # You can add logic here based on the client's response

    except ConnectionResetError:
        print(f"Connection closed by {addr}")
    except Exception as e:
        logger.error(f"Exception in handle_client for {addr}: {e}")
        
    finally:
        sel.unregister(sock)
        sock.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5020))
    server.listen()
    print("Family Feud started. Waiting for connections..")
    server.setblocking(0)
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