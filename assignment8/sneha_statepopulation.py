#!/usr/bin/python
"""
Assignment 8: Plots a graph of population and states using pandas and plotly.
"""

import pandas as pd
import plotly.express as px


def main():
    try:
        statepopcsv = pd.read_csv(
            "statepop.csv", header=None, names=["State", "Population"]
        )
    except FileNotFoundError:
        print(f"statepop.csv file not found.")
    bargraph = px.bar(statepopcsv, x="State", y="Population")
    bargraph.show()


if __name__ == "__main__":
    main()
