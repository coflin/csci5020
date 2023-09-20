#!/usr/bin/python
"""
Assignment: 3
This program generates current price, day low, day high, etc. information of 
a user-provided company's stock using yfinance module. Additionally, it also 
gives related news.
Note that currently, the program only accepts company 'symbols' and not the company 
names. Needs improvement, yes. Used 'black' tool to format the code.
The symbols for company can be found here: https://finance.yahoo.com/lookup/
Another note: Run 'pip install yfinance' and 'pip install pyshorteners' on your CLI  
before running this program
"""

from prettytable import PrettyTable as pt
import pyshorteners
import yfinance as yf

# Declaring variables for my pretty tables. Definitely pleasing to the eye
companystockprice = pt(
    [
        "Company",
        "Symbol",
        "Currency",
        "Current Price",
        "Day Low",
        "Day High",
        "Regular Market Previous Close",
        "Regular Market Open",
    ]
)
companynews = pt(["News Title", "URL link"])

print(f"The symbols for company can be found here: https://finance.yahoo.com/lookup/")
company = yf.Ticker(
    input(
        "Enter the company symbol for which you want to see info about (ex: AAPL, AMZN): "
    )
)

companystockprice.add_row(
    [
        company.info.get("longName"),
        company.info.get("symbol"),
        company.info.get("currency"),
        company.info.get("currentPrice"),
        company.info.get("dayLow"),
        company.info.get("dayHigh"),
        company.info.get("regularMarketPreviousClose"),
        company.info.get("regularMarketOpen"),
    ]
)

# Shortens the huge URL. Again, really pleasing to the "pretty" table and the eye
tiny = pyshorteners.Shortener()

for news in range(len(company.news)):
    companynews.add_row(
        [
            company.news[news].get("title"),
            tiny.tinyurl.short(company.news[news].get("link")),
        ]
    )
print(f"{companystockprice}\n\n\t\t\t\t\t\t\tInteresting News\n\n{companynews}")
