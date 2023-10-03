#!/usr/bin/python
"""
Assignment 8: Plots a graph of all car models and the number of thefts for the respective models.
No user input required in this program.
"""

import matplotlib.pyplot as plt
import csv


def read_file(csvfile):
    make = []
    thefts = []
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
                car = line["Make"]+" "+line["Model"]
                make.append(car)
                thefts.append(line["Thefts"])
        plotgraph(make, thefts)
    except FileNotFoundError:
        print(f"cartheft.csv file does not exist.")


def plotgraph(make, thefts):
    plt.xlabel("Thefts")
    plt.ylabel("Model")
    plt.title("Car Thefts")
    plt.barh(make,thefts,color = '#00095B')
    plt.show()


def main():
    read_file("cartheft.csv")


if __name__ == "__main__":
    main()
