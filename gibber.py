#!/usr/bin/env python3

# Grab RSS feeds and displays x # of headlines

from bs4 import BeautifulSoup
import requests
from rich.console import Console
from rich.table import Table
from datetime import datetime
import os.path

feeds = None

def read_feed_file():
    with open(os.path.join(os.path.dirname(__file__), 'feeds.txt'), 'r') as file:
        global feeds
        feeds = file.read().splitlines()

def get_rss_data(feeds):
    headlines = {}
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux; rv:74.0) Gecko/20100101 Firefox/74.0'}

    for f in feeds:
        response = requests.get(f, headers=headers)
        if response.status_code != 404:
            soup = BeautifulSoup(response.content, 'xml')
            articles = soup.find_all(['item', 'entry'], limit = 5)
            headlines[soup.find('title').text] = articles

    return headlines

def rprint_articles(article_data):
    todays_date = datetime.now().strftime("%A, %d - %B")

    site_title = None
    for a in article_data:
        site_title = a

        print_table(site_title, todays_date, article_data[a])

def print_table(site_title, todays_date, data):
    table = Table(title=f"{site_title} - {todays_date}", show_lines=True)

    table.add_column("Title", justify="left", style="cyan")
    table.add_column("Link", style="magenta")

    for h in data:
        title = h.find('title').text
        link = h.find('link').text or h.find('id').text
        table.add_row(title, link)

    console = Console()
    console.print(table)

if __name__ == "__main__":
    read_feed_file()
    article_data = get_rss_data(feeds)
    rprint_articles(article_data)
