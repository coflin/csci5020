#!/usr/bin/python

import argparse
import socket

"""
Assignment 15: TCP Client. Sends the contents of a file to a server using TCP.
Takes a file as an input.
"""


def readfile(inputfile, s):
    with open(inputfile, "rb") as file:
        data = file.read()
        s.sendall(data)
        s.close()

def main():
    parser = argparse.ArgumentParser(
        description="Forms a TCP connection, connects to a TCP server and sends a file."
    )
    parser.add_argument("--inputfile", help="Input file", action="store", required=True)
    args = parser.parse_args()

    TCP_IP = "127.0.0.1"
    TCP_PORT = 10000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))

    readfile(args.inputfile, s)


if __name__ == "__main__":
    main()