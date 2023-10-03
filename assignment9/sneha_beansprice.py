#!/usr/bin/python
"""
Assignmet 9: code which runs for 35 minutes and retrieves beans prices every 5 minutes
and stores it in the beansprice file. Logs everything in logfile.log.
"""


import requests
import re
import schedule
import time
import signal, sys
from datetime import datetime
from loguru import logger

logger.add("logfile.log")


def handler(signum, frame):
    sys.exit()


def task():
    req = requests.get("https://beans.itcarlow.ie/prices.html")
    price = re.search("\$\d+.\d+", req.text)
    newprice = price[0].replace("$", "")
    currenttime = datetime.datetime.now().strftime("%H:%M:%S")
    currentdate = datetime.datetime.now().strftime("%m/%d/%Y")
    with open("beansprice", "a") as myfile:
        myfile.write(newprice + "," + currenttime + "\n")
        logger.info(f"The price of beans is ${newprice} at {currentdate} {currenttime}")


@logger.catch
def main():
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(35 * 60)
    schedule.every(5).minutes.do(task)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
