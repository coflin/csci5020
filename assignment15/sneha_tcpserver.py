#!/usr/bin/python

"""
Assignment 15: TCP Server. Reads the contents of a file sent by the client and
writes it to a file on the server.
Optional: Takes outputfile name to write contents of the received file.
"""

import argparse
import socket


def writefile(outputfile, BUFFER_SIZE, conn):
    with open(outputfile, "wb") as file:
        while 1:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            file.write(data)
        print(f"Data stored in {outputfile}")
    conn.close()

def main():
    parser = argparse.ArgumentParser(
        description="Starts a TCP server and writes content to a file."
    )
    parser.add_argument("--outputfile", help="Output File", default="filewrite.txt")
    args = parser.parse_args()

    TCP_IP = "127.0.0.1"
    TCP_PORT = 10000
    BUFFER_SIZE = 20
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    conn, addr = s.accept()
    print(f"Connection from {addr}")

    writefile(args.outputfile, BUFFER_SIZE, conn)

if __name__ == "__main__":
    main()