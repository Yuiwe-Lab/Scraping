#! python3
# ~mikey

#rss_tools
from parse_source import Source, Populate_Tables

#imports
import feedparser
from bs4 import BeautifulSoup
import sqlite3
from sqlite3 import Error
import requests

rss_urls = [r"http://rss.slashdot.org/Slashdot/slashdotMain",
			r"https://www.popsci.com/arcio/rss/",
			r"https://www.motherjones.com/feed/",
			r"www.garfield.com"
		  ]

Populate_Tables('db_test_class.db',rss_urls)

