#!/usr/bin/python

"""
Assignment 11: This code performs web scraping of LinkedIn job listings, checks for new 
job listings, stores them in an SQLite database (job_listing.db), and sends email 
notifications when new jobs are found. The task function is the core of this script, 
and it's executed every 24 hours, as defined in the main function.
TODO: Put in AWS and run it everyday
"""


import requests
from bs4 import BeautifulSoup
import time
import sqlite3
from prettytable import PrettyTable
from loguru import logger
import argparse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule

"""
This function establishes a connection to an SQLite database named "job_listings.db" 
and returns the database connection and cursor.
The optional verbose argument, when provided, enables verbose output via the logger.
"""


def connect_to_database(*verbose):
    try:
        conn = sqlite3.connect("job_listings.db")
        cursor = conn.cursor()
        if verbose:
            logger.debug("Connected to the job_listings.db database")
    except Exception as e:
        logger.error("Database connection failed")

    # Create a table to store job listings if it doesn't exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS job_listings (
            id INTEGER PRIMARY KEY,
            company TEXT,
            jobtitle TEXT,
            location TEXT,
            timeposted, TEXT,
            applyurl TEXT,
            joburl TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    if verbose:
        logger.debug("job_listings table created")
    return conn, cursor


# This function inserts a new job listing into the SQLite database.
def insert_job_listing(
    cursor, company, jobtitle, location, timeposted, applyurl, joburl, *verbose
):
    try:
        cursor.execute(
            """
            INSERT INTO job_listings (company, jobtitle,location,timeposted,applyurl,joburl)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (company, jobtitle, location, timeposted, applyurl, joburl),
        )
        cursor.connection.commit()
    except:
        logger.error(
            f"An unexpected error occured while inserting {company}:{jobtitle} to job_listings table"
        )
    if verbose:
        logger.debug(f"Inserted {company}:{jobtitle} to job_listings table")


"""
This function checks whether a job listing with the specified company 
and job title already exists in the database. Returns True if the job 
listing is new (not found in the database), otherwise False.
"""


def is_new_job_listing(cursor, company, jobtitle, *verbose):
    try:
        cursor.execute(
            """
            SELECT id
            FROM job_listings
            WHERE company = ? AND jobtitle = ?
        """,
            (company, jobtitle),
        )
        if verbose:
            logger.debug("Fetched job listings from job_listings.db")
    except:
        logger.error("An unexpected error occured retrieving info from job_listings.db")
    return cursor.fetchone() is None


"""
This function sends an email notification with a specified subject 
and message to the provided to_email address.
"""


def send_email_notification(to_email, subject, message, *verbose):
    try:
        email = "<your_email_here>"
        password = "<your_password>"
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(email, password)

        msg = MIMEMultipart()
        msg["From"] = email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        server.sendmail(email, to_email, msg.as_string())
        server.quit()
        if verbose:
            logger.debug("Email sent")
    except:
        logger.error("Error sending email")


"""
This function scrapes LinkedIn job listings for a given jobtitle.
Returns a list of dictionaries, with each dictionary representing 
a job listing and containing information such as company name, 
job title, location, time posted, apply URL, and job URL.
"""


def scrape_linkedin(jobtitle, *verbose):
    response = requests.get(
        f"https://www.linkedin.com/jobs/search?keywords={jobtitle.replace(' ','%20')}&location=United%20States&sortBy=R"
    )
    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find_all(
        "div",
        {
            "class": "base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card"
        },
    )
    jobslist = []

    for job in jobs:
        jobdetails = {}
        if job:
            jobid = job.get("data-entity-urn").split(":")[3]

            res = requests.get(
                f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{jobid}"
            )
            soup1 = BeautifulSoup(res.text, "html.parser")

            company = soup1.find(
                "a", {"class": "topcard__org-name-link topcard__flavor--black-link"}
            )
            jobdetails.update(
                {"companyName": company.text.strip()}
                if company
                else {"companyName": "-"}
            )

            title = soup1.find(
                "h2",
                {
                    "class": "top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title"
                },
            )
            jobdetails.update(
                {"title": title.text.strip()} if title else {"title": "-"}
            )

            if verbose:
                logger.debug(
                    f"Retrieved {company.text.strip()} : {title.text.strip()}"
                    if company and title
                    else ""
                )

            location = soup1.find(
                "span", {"class": "topcard__flavor topcard__flavor--bullet"}
            )
            jobdetails.update(
                {"location": location.text.strip()} if location else {"location": "-"}
            )

            timeposted = soup1.find(
                "span", {"class": "posted-time-ago__text topcard__flavor--metadata"}
            )
            jobdetails.update(
                {"timePosted": timeposted.text.strip()}
                if timeposted
                else {"timePosted": "-"}
            )

            apply = soup1.find("code", {"id": "applyUrl"})
            jobdetails.update(
                {"applyUrl": apply.string} if apply else {"applyUrl": "-"}
            )

            joburl = f"https://www.linkedin.com/jobs/view/{jobid}"
            jobdetails.update({"jobUrl": joburl} if joburl else "")

            jobslist.append(jobdetails)

    return jobslist


logger.add("log_output.log")
logger.debug("Created log_output.log file")
"""
This is the main task that performs the following:
    1. Parses command-line arguments: jobtitle and a flag for verbose output.
    2. Connects to the SQLite database using the connect_to_database function.
    3. Scrapes LinkedIn job listings based on the specified jobtitle.
    4. Checks if each job listing is new using is_new_job_listing.
    5. If a job listing is new, it adds it to the database and constructs an email message.
    6. Sends an email notification with the job listings using send_email_notification.
    7. The task is designed to be run every 24 hours.
"""


def task(title, *verbose):
    try:
        if verbose:
            conn, cursor = connect_to_database("verbose")
        else:
            conn, cursor = connect_to_database()
        if verbose:
            logger.debug(f"Checking New Linkedin Job postings for {title}")
            jobs = scrape_linkedin(title, "verbose")
        else:
            jobs = scrape_linkedin(title)

        if jobs:
            jobmessage = "New job listing:\n"
            for job in jobs:
                company = job["companyName"]
                jobtitle = job["title"]
                location = job["location"]
                timeposted = job["timePosted"]
                applyurl = job["applyUrl"]
                joburl = job["jobUrl"]

                if is_new_job_listing(cursor, company, jobtitle):
                    jobmessage += f"Company: {company}\nJob Title: {jobtitle}\nLocation: {location}\nPosted: {timeposted}\nApply here: {applyurl}\nSee job description here: {joburl}\n----------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n"
                    if verbose:
                        logger.debug(
                            f"Inserting {company}:{jobtitle} to job_listings table"
                        )
                        insert_job_listing(
                            cursor,
                            company,
                            jobtitle,
                            location,
                            timeposted,
                            applyurl,
                            joburl,
                            "verbose",
                            )
                    else:
                        insert_job_listing(
                            cursor,
                            company,
                            jobtitle,
                            location,
                            timeposted,
                            applyurl,
                            joburl,
                            )

            if jobmessage != "New job listing:\n":
                if verbose:
                    logger.debug("Sending email notification")
                    send_email_notification(
                        "<your_email@gmail.com>",
                        f"New Job Listing Notification:{title}",
                        jobmessage,
                        "verbose",
                    )

                else:
                    send_email_notification(
                        "<your_email@gmail.com>",
                        f"New Job Listing Notification:{title}",
                        jobmessage,
                    )
            else:
                logger.debug("Up-to-date with all job listings. Not sending an email notification.")
        else:
            logger.info("No job listings found.")
        conn.close()

    except Exception as e:
        logger.error(f"An error occured in the task function: {e}")


"""
Uses the schedule module to run the task function every 24 hours.
The while True loop allows the script to continue running and scheduling the task.
"""


def main():
    exampletext = (
        "Example usage: python milestone1.py --jobtitle 'network engineer intern' --verbose"
    )
    parser = argparse.ArgumentParser(
        epilog=exampletext, description="Scrapes LinkedIn job listings"
    )
    parser.add_argument(
        "-j",
        "--jobtitle",
        type=str,
        action="store",
        required=True,
        help="Job title to search for",
    )
    parser.add_argument(
        "-vvv", "--verbose", action="store_true", help="For verbose output"
    )
    parser.add_argument("-v", "--version", action="version", version="1.0")
    args = parser.parse_args()

    if args.verbose:
        process = schedule.every(24).hours.do(task, args.jobtitle, "verbose")
        process.run()
    else:
        process = schedule.every(24).hours.do(task, args.jobtitle)
        process.run()
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
