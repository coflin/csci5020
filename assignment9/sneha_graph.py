#!/usr/bin/python
"""
Assignment 9: Takes beansprice file as input, and graphs it using pandas and plotly.
"""


from datetime import datetime
import pandas as pd
import plotly.express as px


def main():
    currentdate = datetime.now().strftime("%m/%d/%Y")
    beanspricecsv = pd.read_csv(
        "beansprice", header=None, names=["Price of Beans", "Time"]
    )
    linegraph = px.line(
        beanspricecsv,
        x="Time",
        y="Price of Beans",
        title=f"Prices of Beans on {currentdate}",
    )
    linegraph.show()


if __name__ == "__main__":
    main()
