#!/usr/bin/python
"""
Assignment 5: Dice roller app using argparse. Takes arguments on the command line where the first 
argument is the number of dice to be rolled and the second argument is 
the number of sides the dice has
"""

import argparse
from random import randint


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
    parser = argparse.ArgumentParser(
        description="Dice Roller App. Takes number of dice to be rolled as first argument and number of sides of the dice as second argument"
    )
    parser.add_argument("dice", action="store", help="number of dice to be rolled")
    parser.add_argument("sides", action="store", help="number of sides of the dice")
    parser.add_argument("-v", "--version", action="version", version="1.0")
    args = parser.parse_args()
    diceroll(args.dice, args.sides)


if __name__ == "__main__":
    main()
