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
			r"http://science.sciencemag.org/rss/express.xml",
			r"https://rss.app/feeds/JyMVgKu36v8JT4H0.xml", #ny times business
			r"https://rss.app/feeds/uVCDwng32TgGk0nJ.xml"  # ny times world  best so far
		  ]

Populate_Tables('wordsort.db',rss_urls)

