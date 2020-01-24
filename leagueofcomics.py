#!/usr/bin/python3
# -*-coding:utf-8 -*-

"""League of comics API."""
import datetime
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# publisher 1 is DC
# publisher 2 is Marvel
# indie comics are all comics, excluding 1 and 2 (the Big Two)


def fetch_issues(publisher=None,
                 week=False,
                 m=None, y=None,
                 firsts_only=False):
    loc_url = "https://leagueofcomicgeeks.com"
    api_url = "https://leagueofcomicgeeks.com/comic/get_comics"

    params = {"addons": 1,
              "list": "releases",
              "date_type": "previews",
              "date": None,
              "date_end": None,
              "user_id": 0,
              "view": "list",
              "format[]": [1, 6],  # Regular issues + Annuals ??
              "publisher_exclude[]": [],
              "publisher[]": [],
              "list_refinement": None,
              "order": "alpha-asc"  # or by popularity : "order": "pulls"
              }

    # Select by publisher DC / Marvel / Indie
    if publisher == "DC":
        params["publisher[]"] = 1
    elif publisher == "Marvel":
        params["publisher[]"] = 2
    elif publisher == "Indie":
        params["publisher_exclude[]"] = [1, 2]

    today = datetime.date.today()

    # Current week
    if week:
        params["date_type"] = "week"
        params["date"] = today.strftime("%m/%d/%Y")
    # User month and year
    elif m and y:
        params["date"] = f"{m}/01/{y}"
    # Current month
    else:
        params["date"] = today.strftime("%m/01/%Y")

    # Only first issues ?
    if firsts_only:
        params["list_refinement"] = "firsts"

    # fetch league of comics
    resp = requests.get(api_url, params=params)
    # Parse response
    json_ = resp.json()['list']
    soup = BeautifulSoup(json_, "html.parser")
    raw_list = soup.select("li.media")
    # each element of raw_list is a comic html html div
    # with cover, title, synopsis, date, price, etc...

    # We make a list of comics dictionnary like :
    # {"title": <title>,
    #  "cover": <cover url>,
    #   "url": <league of comics url>}
    comics = [{"title": r.select_one("div.comic-title").text,
               "cover": r.select_one("div.comic-cover-art").img["data-original"],  # noqa: E501
               "url": urljoin(loc_url, r.select_one("div.comic-title > a")["href"])}  # noqa: E501
              for r in raw_list]

    return comics


def print_issue(issue):
    """Pretty prints a "comic" dictionnary."""
    print('\t' + issue["title"])
    print('\t' + issue["cover"].split("?")[0])
    print('\t' + issue["url"])
    print()


# MAIN - TESTS
# #1 current week
print("#####################################")
print("Fetching DC #1 - week mode")
print("-------------------------------------")
issues = fetch_issues(publisher="DC", week=True, firsts_only=True)

print(f"{len(issues)} issues")
for i in issues:
    print_issue(i)
print("#####################################")


# All issues current week
print("#####################################")
print("Fetching DC ALL - week mode")
print("-------------------------------------")
issues = fetch_issues(publisher="DC", week=True)

print(f"{len(issues)} issues")
for i in issues:
    print_issue(i)
print("#####################################")

# #1 current week for INDIE
print("#####################################")
print("Fetching Indie #1 - week mode")
print("-------------------------------------")
issues = fetch_issues(publisher="Indie", week=True, firsts_only=True)

print(f"{len(issues)} issues")
for i in issues:
    print_issue(i)
print("#####################################")

# #1 current month (Preview mode), Marvel
print("#####################################")
print("Fetching Marvel #1 previews - no user month")
print("-------------------------------------")
issues = fetch_issues(publisher="Marvel", firsts_only=True)

print(f"{len(issues)} issues")
for i in issues:
    print_issue(i)
print("#####################################")

# #1 Febr 2020 (Preview mode), Marvel
print("#####################################")
print("Fetching Marvel #1 previews- Febr 2020")
print("-------------------------------------")
issues = fetch_issues(publisher="Marvel", firsts_only=True, m=2, y=2020)

print(f"{len(issues)} issues")
for i in issues:
    print_issue(i)
print("#####################################")

# #1 current week - All publishers
print("#####################################")
print("Fetching All #1 - week mode")
print("-------------------------------------")
issues = fetch_issues(week=True, firsts_only=True)

print(f"{len(issues)} issues")
for i in issues:
    print_issue(i)
print("#####################################")
