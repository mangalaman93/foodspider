# Author: Aman Mangal <mangalaman93@gmail.com>
# Created on July 23, 2017

import __init__
import us

SEARCH_TERMS = [
    "food bank",
    "food charity",
    "food donation",
    "food assistance",
    "food outreach",
    "food advocacy",
    "food organisations"
]

SEARCH_PREFIX = [
    "national",
    "domestic",
] + list(map(lambda s: str(s), us.states.STATES))
