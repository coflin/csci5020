#!/usr/bin/python
"""
Assignment 5: Dice roller app using sysargv. Takes arguments on the command line where the first 
argument is the number of dice to be rolled and the second argument is 
the number of sides the dice has
"""
from random import randint
import sys


def diceroll(dice, sides):
    roll = 0
    for i in range(int(dice)):
        roll += randint(1, int(sides))
    if roll == int(dice):
        print(f"Critical failure! Rolled {roll}")
    elif roll == int(sides) * int(dice):
        print(f"Critical success! Rolled {roll}")
    else:
        print(f"You rolled {roll}")


def main():
    if len(sys.argv) < 3:
        print(f"Please specify the number of dice and number of sides")
        sys.exit
    else:
        diceroll(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
