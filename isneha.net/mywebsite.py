#!/usr/bin/python

"""
Assignment 17: URL to my personal website: https://isneha.net
"""

from flask import Flask, render_template

app=Flask(__name__)

@app.route("/")
def staticpage():
    return render_template("index.html",ResumeRoute="/resume",PythonProjectRoute="/python",LinuxProjectRoute="/linux",NetworkingProjectRoute="/networking",WebsiteProjectRoute="/python/website")

@app.route("/resume")
def resume():
    return render_template("resume.html",HomepageRoute="/")

@app.route("/python")
def python_projects():
    return render_template("python-projects.html",MainPageRoute="/",ResumeRoute="/resume",ProjectRoute="/#my-work",AboutRoute="/#about",LinkedinProjectRoute="/python/linkedin-job-scraper",PnmapProjectRoute="/python/pnmap",WebsiteProjectRoute="/python/website",FamilyFeudProjectRoute="/python/family-feud")

@app.route("/linux")
def linux_projects():
    return render_template("linux-projects.html",MainPageRoute="/",ResumeRoute="/resume",ProjectRoute="/#my-work",AboutRoute="/#about",DunderMifflinProjectRoute="/linux/dunder-mifflin",DHCPProjectRoute="/linux/dhcp",LVMProjectRoute="/linux/lvm")

@app.route("/networking")
def networking_projects():
    return render_template("networking-projects.html",MainPageRoute="/",ResumeRoute="/resume",ProjectRoute="/#my-work",AboutRoute="/#about",NetworkAutomationProjectRoute="/networking/network-automation")


#Python Projects
@app.route("/python/linkedin-job-scraper")
def linkedin_job_scraper():
    return render_template("linkedin-job-scraper.html",MainPageRoute="/",ResumeRoute="/resume",ProjectRoute="/#my-work",AboutRoute="/#about")

@app.route("/python/pnmap")
def pnmap():
    return render_template("pnmap.html",MainPageRoute="/",ResumeRoute="/resume",ProjectRoute="/#my-work",AboutRoute="/#about")

@app.route("/python/website")
def website():
    return render_template("website.html",MainPageRoute="/",ResumeRoute="/resume",ProjectRoute="/#my-work",AboutRoute="/#about")

@app.route("/python/family-feud")
def familyfeud():
     return render_template("family-feud.html",MainPageRoute="/",ResumeRoute="/resume",ProjectRoute="/#my-work",AboutRoute="/#about")   

#Linux Projects

@app.route("/linux/dunder-mifflin")
def dundermifflin():
    return render_template("dundermifflin.html",MainPageRoute="/",ResumeRoute="/resume",ProjectRoute="/#my-work",AboutRoute="/#about")

@app.route("/linux/dhcp")
def dhcp():
    return render_template("dhcp.html",MainPageRoute="/",ResumeRoute="/resume",ProjectRoute="/#my-work",AboutRoute="/#about")

@app.route("/linux/lvm")
def lvm():
    return render_template("lvm.html",MainPageRoute="/",ResumeRoute="/resume",ProjectRoute="/#my-work",AboutRoute="/#about")

# Networking Projects

@app.route("/networking/network-automation")
def network_automation():
    return render_template("network-automation.html",MainPageRoute="/",ResumeRoute="/resume",ProjectRoute="/#my-work",AboutRoute="/#about")

if __name__ == "__main__":
    app.debug = True
    app.run("127.0.0.1",port=80)