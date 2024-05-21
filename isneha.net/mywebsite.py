#!/usr/bin/python

"""
URL to my personal website: https://isneha.net
"""

from flask import Flask, render_template

app = Flask(__name__)

# Define the route dictionaries
route_data = {
    "/": {
        "template": "index.html",
        "args": {
            "ResumeRoute": "/resume",
            "PythonProjectRoute": "/python",
            "LinuxProjectRoute": "/linux",
            "NetworkingProjectRoute": "/networking",
            "WebsiteProjectRoute": "/python/website"
        }
    },
    "/resume": {
        "template": "resume.html",
        "args": {"HomepageRoute": "/"}
    },
    "/python": {
        "template": "python-projects.html",
        "args": {
            "MainPageRoute": "/",
            "ResumeRoute": "/resume",
            "ProjectRoute": "/#my-work",
            "AboutRoute": "/#about",
            "LinkedinProjectRoute": "/python/linkedin-job-scraper",
            "PnmapProjectRoute": "/python/pnmap",
            "WebsiteProjectRoute": "/python/website",
            "FamilyFeudProjectRoute": "/python/family-feud"
        }
    },
    "/linux": {
        "template": "linux-projects.html",
        "args": {
            "MainPageRoute": "/",
            "ResumeRoute": "/resume",
            "ProjectRoute": "/#my-work",
            "AboutRoute": "/#about",
            "DunderMifflinProjectRoute": "/linux/dunder-mifflin",
            "DHCPProjectRoute": "/linux/dhcp",
            "LVMProjectRoute": "/linux/lvm"
        }
    },
    "/networking": {
        "template": "networking-projects.html",
        "args": {
            "MainPageRoute": "/",
            "ResumeRoute": "/resume",
            "ProjectRoute": "/#my-work",
            "AboutRoute": "/#about",
            "NetworkAutomationProjectRoute": "/networking/network-automation"
        }
    }
}

# Define the individual project routes
project_routes = {
    "/python/linkedin-job-scraper": "linkedin-job-scraper.html",
    "/python/pnmap": "pnmap.html",
    "/python/website": "website.html",
    "/python/family-feud": "family-feud.html",
    "/linux/dunder-mifflin": "dundermifflin.html",
    "/linux/dhcp": "dhcp.html",
    "/linux/lvm": "lvm.html",
    "/networking/network-automation": "network-automation.html"
}

# General render template function
def render_custom_template(route):
    data = route_data.get(route, {})
    return render_template(data["template"], **data.get("args", {}))

# Set up the main routes
for route in route_data:
    app.add_url_rule(route, route, (lambda r=route: render_custom_template(r)))

# Set up the project routes
for route, template in project_routes.items():
    app.add_url_rule(route, route, (lambda t=template: render_template(t, MainPageRoute="/", ResumeRoute="/resume", ProjectRoute="/#my-work", AboutRoute="/#about")))

if __name__ == "__main__":
    app.debug = True
    app.run("127.0.0.1", port=80)
