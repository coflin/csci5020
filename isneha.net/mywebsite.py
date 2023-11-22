#!/usr/bin/python

from flask import Flask, render_template

app=Flask(__name__)

@app.route("/")
def staticpage():
    return render_template("index.html",ResumeRoute="/resume",PythonProjectRoute="/python-projects",LinuxProjectRoute="/linux-projects",NetworkingProjectRoute="/networking-projects")

@app.route("/resume")
def resume():
    return render_template("resume.html")

@app.route("/python-projects")
def python_projects():
    return render_template("python-projects.html",MainPageRoute="/",ResumeRoute="/resume",ProjectRoute="/#my-work",AboutRoute="/#about",LinkedinProjectRoute="/linkedin-job-scraper",PnmapProjectRoute="/pnmap",WebsiteProjectRoute="/website")

@app.route("/linux-projects")
def linux_projects():
    return render_template("linux-projects.html",MainPageRoute="/",ResumeRoute="/resume",ProjectRoute="/#my-work",AboutRoute="/#about")

@app.route("/networking-projects")
def networking_projects():
    return render_template("networking-projects.html",MainPageRoute="/",ResumeRoute="/resume",ProjectRoute="/#my-work",AboutRoute="/#about")

@app.route("/linkedin-job-scraper")
def linkedin_job_scraper():
    return render_template("linkedin-job-scraper.html",MainPageRoute="/",ResumeRoute="/resume",ProjectRoute="/#my-work",AboutRoute="/#about")

@app.route("/pnmap")
def pnmap():
    return render_template("pnmap.html",MainPageRoute="/",ResumeRoute="/resume",ProjectRoute="/#my-work",AboutRoute="/#about")

@app.route("/website")
def website():
    return render_template("website.html",MainPageRoute="/",ResumeRoute="/resume",ProjectRoute="/#my-work",AboutRoute="/#about")

if __name__ == "__main__":
    app.debug = True
    app.run("127.0.0.1",port=80)
