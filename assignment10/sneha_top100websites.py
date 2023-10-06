#!/usr/bin/python
"""
Assignment 10: Fetches the top 100 websites from moz.com.
Run 'python sneha_top100websites.py --verbose' for verbosity.
"""

import argparse
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from loguru import logger

def writetofile(data):
    with open("websites.csv","w") as file:
        file.write(str(data))

def top100websites(headers,cookies,*verbose):
    response = requests.get("https://moz.com/top500", headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.text,'html.parser')
    lines = 1
    results = []
    tables = soup.find_all("table")
    """
    I am extracting each <table> tag. The find_all puts all the tables (till it reaches a page break) 
    in one list. I am looping in through all these lists (which essentially contains tables) 
    & extracting everything between the <a> tags.
    """
    for table in tables:
        for atag in table.find_all("a"):
            website = atag.text
            url = atag.nextSibling
            if website and lines <= 100:
                try:
                    res = BeautifulSoup(requests.get(url['href'],headers=headers).text,'html.parser')
                    title = res.title.string
                    if verbose:
                        logger.debug(f"{lines}: Retrieved {website}")
                    results.append((website,url['href'],title))
                except Exception as e:
                    logger.error(f"An error occured retrieving {website}")
                    results.append((website,url['href'],"ERR"))
                lines += 1
    return results

def main():
    cookies = {
        '_moz_csrf':'dd5ccd9197a9d9b9ab7d9c01bace41c39bf3e4b7',
        '__cf_bm':'V8pHjjjOuvJqRqfw9WWwBr_a9qiL4GA.6n3R2JHjYiI-1696474436-0-AR8K9dGA7w6xRRLvOdnWUqa9D5EfakB/6QfnUVXnV6XNhSCskHCSXeZx/w236W/c4IqThOM2slNlF/SPvArzklQ=',
        'cf_clearance':'Pd_bweR02Ya8fq3mRikCsu10.z88saCO3qCbbGw3r54-1696474711-0-1-98f3d8a2.2ad60db0.cff28742-0.2.1696474711',
        'ajs_anonymous_id':'b15541d1-2b00-4576-8c87-52ee5bb178f0',
        '_gcl_au':'1.1.1958288820.1696474439',
        '_ga_DS7K9Q3S5W':'GS1.1.1696474438.1.1.1696474711.0.0.0',
        '_ga':'GA1.2.196076407.1696474439',
        '_ga_LGQZKGRBE5':'GS1.1.1696474438.1.1.1696474711.46.0.0',
        '_rdt_uuid':'1696474438850.75533786-02fa-44b5-9cc7-74e9e2e6396e',
        '__stripe_mid':'d00c9f96-ce51-4275-9a54-3a1e79acc722e0070b',
        '__stripe_sid':'1eaaa548-4292-4734-a6c2-25cd8028ea8c1ff35c',
        '_gid':'GA1.2.163370180.1696474439',
        '_fbp':'fb.1.1696474440167.1301838646',
        '__hstc':'103427807.827cd9c849f54d739383cd92282ea19f.1696474439419.1696474439419.1696474439419.1',
        'hubspotutk':'827cd9c849f54d739383cd92282ea19f',
        '__hssrc':'1',
        '__hssc':'103427807.3.1696474439419',
        'ln_or':'eyIxMDcyMiI6ImQifQ%3D%3D',
        '_ga_QLCPR2NDVP':'GS1.1.1696474697.1.0.1696474697.0.0.0',
        '_uetsid':'6e3ddcc0632a11ee8c12bb1544dad60f',
        '_uetvid':'6e3dbfb0632a11ee9bb6a38994e735d1',
        }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux aarch64; rv:109.0) Gecko/20100101 Firefox/115.0'
    }

    parser = argparse.ArgumentParser(description="Fetch top 100 websites.")
    parser.add_argument("--verbose", action="store_true", help="Get verbose output")
    args = parser.parse_args()
    logger.info("Retrieving the top 100 websites from moz.com..")
    if args.verbose:
        results = top100websites(headers,cookies,"verbose")
    else:
        results = top100websites(headers,cookies)
    
    webscraper = PrettyTable(["Website", "URL", "Website Title"])
    webscraper.align["Website Title"] = "l"
    webscraper.align["URL"] = "l"
    webscraper.align["Website"] = "l"

    # Add rows to the table from the results
    for website, url, title in results:
        webscraper.add_row([website, url, title])

    writetofile(webscraper)
    logger.info("List of websites saved in 'websites.csv'")

if __name__ == "__main__":
    main()