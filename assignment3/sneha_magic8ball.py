#!/usr/bin/python
"""
Assignment: 3
Magic 8 ball app. The user thinks of a yes/no question and this app would randomly 
select one item from the list of fortunes. Used 'black' tool to format the code 
"""
from random import choice
from time import sleep

fortunes = [
    "Yes, definitely!",
    "Certainly",
    "Some things are better left unsaid",
    "Mostly not",
    "You can count on it",
    "Doubtful",
    "Concentrate and ask again",
    "Sure!",
]


def prediction():
    print(f"Think of a yes/no question. I will predict it for you")
    sleep(2)
    print(f"Answer: {choice(fortunes)}")


prediction()
sleep(2)
repeat = input("Would you like to ask another question? Y/N\n")

while repeat == "Y" or repeat == "y":
    prediction()
    sleep(2)
    repeat = input("Would you like to ask another question? Y/N\n")
else:
    print(f"I hope I answered all your questions. See you next time!")
