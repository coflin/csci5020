#!/usr/bin/python
"""
Assignment 6: Celsius/Farhenheit convertor. Imports functions from 2a.py file
to convert the temperature. Input the temperature either in Celsius or Farhenheit.
Check the help page for more information. python 2b.py -h
"""

import argparse

a2 = __import__("2a")


def main():
    exampletext = "Example usage: python 2b.py 32F; python 2b.py 0C"
    parser = argparse.ArgumentParser(
        epilog=exampletext,
        description="Celsius/Farheinheit converter. Saves people around the world some calculations.",
    )
    parser.add_argument(
        "temperature",
        action="store",
        help="<temperature number>F or <temperature number>C",
    )
    parser.add_argument("-v", "--version", action="version", version="1.0")
    args = parser.parse_args()
    if "F" in args.temperature:
        a2.farheinheittocelsius(args.temperature[:-1])
    elif "C" in args.temperature:
        a2.celsiustofarheinheit(args.temperature[:-1])
    else:
        print(
            f'Please input the temperature in "<temperature>F" or "<temperature>C" format. "python 2b.py -h" for more help'
        )


if __name__ == "__main__":
    main()
