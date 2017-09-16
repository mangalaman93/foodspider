# Author: Aman Mangal <mangalaman93@gmail.com>
# Created on July 23, 2017

import __init__
import csv
import us
import random
import sys
import time
from GoogleScraper import scrape_with_config, GoogleSearchError

NUM_PAGES = 2

SEARCH_STATES = list(map(lambda s: str(s), us.states.STATES))

SEARCH_TERMS = [
    "food bank",
    "food charity",
    "food donation",
    "food assistance",
    "food outreach",
    "food advocacy",
    "food organisations",
    "food insecurity"
]

HEADER = [
    "State",
    "Search Term",
    "Page Number",
    "Index of Search within the Page",
    "Number of Times Domain Appeared within state",
    "Title",
    "Description",
    "Link",
    "Google Link"
]

def makeDecision():
    cmd = input("enter 0 to skip, 1 to retry, 2 to exit > ")
    if cmd != '0' and cmd != '1' and cmd != '2':
        print("invalid input, try again!")
        return makeDecision()
    elif cmd == '0':
        return True
    elif cmd == '1':
        return False
    else:
        sys.exit(0)

def process(state, term, page_number, seen, writer, result, last_last_count):
    if seen.get(result.domain, -1) > 0:
        seen[result.domain] = seen[result.domain] + 1
    else:
        seen[result.domain] = 1

    row = [
        state,
        term,
        page_number,
        result.rank + last_last_count,
        seen[result.domain],
        result.title,
        result.snippet,
        result.link,
        result.visible_link
    ]
    writer.writerow(row)

def serachForState(state):
    seen = dict()
    for term in SEARCH_TERMS:
        query = ""
        if state == "":
            query = term
        else:
            query = state + " " + term

        config = {
            'use_own_ip': True,
            'keyword': query,
            'search_engines': ['bing'],
            'num_pages_for_keyword': NUM_PAGES,
            'scrape_method': 'selenium',
            'sel_browser': 'chrome',
            'do_caching': False
        }

        done = False
        while not done:
            time.sleep(random.uniform(0, 1))
            try:
                search = scrape_with_config(config)
                last_count = 0
                last_last_count = 0
                for serp in search.serps:
                    last_last_count = last_count
                    for result in serp.links:
                        last_count = last_count + 1
                        process(state, term, serp.page_number, seen, writer, result, last_last_count)
                done = True
            except GoogleSearchError as e:
                print(e)
                done = makeDecision()

with open("res/5/foodbanks.csv", "w", newline='') as csvfd:
    writer = csv.writer(csvfd, delimiter='\t')
    writer.writerow(HEADER)
    for state in SEARCH_STATES:
        print("searching for state: "  + state)
        serachForState(state)

    SEARCH_TERMS.remove("food insecurity")
    serachForState("national")
    serachForState("")
