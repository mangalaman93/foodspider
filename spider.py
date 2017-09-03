# Author: Aman Mangal <mangalaman93@gmail.com>
# Created on July 23, 2017

import __init__
import csv
import us
import random
import time
from GoogleScraper import scrape_with_config, GoogleSearchError

NUM_PAGES=2

SEARCH_PREFIX = [
    "national",
    "domestic",
] + list(map(lambda s: str(s), us.states.STATES))

SEARCH_TERMS = [
    "food bank",
    "food charity",
    "food donation",
    "food assistance",
    "food outreach",
    "food advocacy",
    "food organisations"
]

HEADER = [
    "Name",
    "Description",
    "Link",
    "Google Link"
]

seen = dict()
def process(writer, dupwriter, result):
    w = None
    if seen.get(result.domain, False):
        w = dupwriter
    else:
        seen[result.domain] = True
        w = writer

    row = [
        result.title,
        result.snippet,
        result.link,
        result.visible_link
    ]
    w.writerow(row)

def serachFor(query):
    config = {
        'use_own_ip': True,
        'keyword': query,
        'search_engines': ['google'],
        'num_pages_for_keyword': 2,
        'scrape_method': 'selenium',
        'sel_browser': 'chrome',
        'do_caching': False
    }
    try:
        search = scrape_with_config(config)
        for serp in search.serps:
            for result in serp.links:
                process(writer, dupwriter, result)
    except GoogleSearchError as e:
        print(e)

with open("res/2/foodbanks.csv", "w", newline='') as csvfd:
    writer = csv.writer(csvfd, delimiter='\t')
    writer.writerow(HEADER)
    with open("res/2/dupfoodbanks.csv", "w", newline='') as dupcsvfd:
        dupwriter = csv.writer(dupcsvfd, delimiter='\t')
        dupwriter.writerow(HEADER)

        for prefix in SEARCH_PREFIX:
            for term in SEARCH_TERMS:
                query = prefix + " " + term
                print("searching for " + query)
                serachFor(query)
                time.sleep(random.uniform(0, 1))
