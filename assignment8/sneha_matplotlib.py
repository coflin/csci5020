#!/usr/bin/python
"""
Assignment 8: Plots a graph of all car models and the number of thefts for the respective models.
No user input required in this program.
"""

import matplotlib.pyplot as plt
import csv


def read_file(csvfile):
    # X-Axis
    x = []
    # Y-Axis
    y = []
    try:
        with open(csvfile, "r") as cartheft:
            reader = list(
                csv.DictReader(
                    cartheft,
                    fieldnames=[
                        "Make",
                        "Model",
                        "Thefts",
                        "Production",
                        "Rate",
                        "Year",
                        "Type",
                    ],
                )
            )
            for line in reader[-10:]:
                x.append(line["Make"])
                y.append(line["Thefts"])
        plotgraph(x, y)
    except FileNotFoundError:
        print(f"cartheft.csv file does not exist.")


def plotgraph(listx, listy):
    plt.plot(listx, listy)
    plt.xlabel("Make")
    plt.ylabel("Thefts")
    plt.title("Car Thefts")
    plt.show()


def main():
    read_file("cartheft.csv")


if __name__ == "__main__":
    main()
