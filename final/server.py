import asyncio
import selectors
import types

sel = selectors.DefaultSelector()

async def accept_wrapper(sock):
    conn, addr = sock.accept()
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    
    welcome_message = "What is your name? "
    conn.sendall(welcome_message.encode('utf-8'))

    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

async def service_connection(key, mask):
    sock = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.inb += recv_data
            lines = data.inb.split(b'\n')
            for line in lines[:-1]:
                await handle_input_line(sock, line.decode('utf-8'))
            data.inb = lines[-1]

    if mask & selectors.EVENT_WRITE:
        if data.outb:
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]

async def handle_input_line(sock, line):
    try:
        # Add your logic to handle each line of input (e.g., process answers)
        response = f"Received: {line}\n"
        # Assume a function process_answer exists to handle answers
        answer_result = process_answer(line)
        response += f"Response: {answer_result}\n"
        sock.sendall(response.encode('utf-8'))
    except Exception as e:
        print(f"Exception in handle_input_line: {e}")

def process_answer(answer):
    # Add your logic to process the received answer
    # For example, you can check if the answer is correct, update scores, etc.
    return f"Processing answer: {answer}"

async def main():
    server = await asyncio.start_server(
        accept_wrapper, '0.0.0.0', 5020)

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())