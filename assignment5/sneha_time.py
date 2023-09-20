#!/usr/bin/python
"""
Assignment 5: Endlessly prints current time until keyboard interrupt
"""
from datetime import datetime


def currenttime():
    while True:
        print(f'{datetime.now().strftime("%H:%M:%S")}')


def main():
    currenttime()


if __name__ == "__main__":
    main()
