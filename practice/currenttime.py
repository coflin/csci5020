#!/usr/bin/python

from datetime import datetime
import time

def get_current_time():
    print(datetime.now().strftime('%H:%M:%S'))

def main():
    while True:
        get_current_time()
        time.sleep(30)

if __name__ == "__main__":
    main()
