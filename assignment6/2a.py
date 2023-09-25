#!/usr/bin/python
"""
Assignment 6: Celsius/Farheinheit converter. 
Input the temperature either in Celsius or Farhenheit.
Check the help page for more information. python 2a.py -h
"""

import argparse


def celsiustofarheinheit(celsius):
    farheinheit = (float(celsius) * (9 / 5)) + 32
    print(f"{celsius}C is {round(farheinheit,2)}F")


def farheinheittocelsius(farhenheit):
    celsius = (float(farhenheit) - 32) * (5 / 9)
    print(f"{farhenheit}F is {round(celsius,2)}C")


def main():
    parser = argparse.ArgumentParser(
        description="Celsius/Farheinheit converter. Saves people around the world some calculations.\nSypnosis: <temperature number>F or <temperature number>C"
    )
    parser.add_argument(
        "temperature",
        action="store",
        help="Use in this format: <temperature number>F or <temperature number>C",
    )
    parser.add_argument("-v", "--version", action="version", version="1.0")
    args = parser.parse_args()
    if "F" in args.temperature:
        farheinheittocelsius(args.temperature[:-1])
    elif "C" in args.temperature:
        celsiustofarheinheit(args.temperature[:-1])
    else:
        print(
            f'Please input the temperature in "<temperature>F" or "<temperature>C" format. "python 2a.py -h" for more help'
        )


if __name__ == "__main__":
    main()
