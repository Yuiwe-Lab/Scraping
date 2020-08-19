#! python3
# ~mikey

#rss_tools
from sift import Sift
#imports
import feedparser
from bs4 import BeautifulSoup
import sqlite3
from sqlite3 import Error
import requests

#rss.app currently Broken
rss_urls = [r"http://rss.slashdot.org/Slashdot/slashdotMain",	#Slashdot
			r"https://www.popsci.com/arcio/rss/",				#Popsci
			r"https://www.motherjones.com/feed/",				#Mother Jones
			r"http://science.sciencemag.org/rss/express.xml",	#Science Magazine
			#r"https://rss.app/feeds/JyMVgKu36v8JT4H0.xml", 	#ny times business
			#r"https://rss.app/feeds/uVCDwng32TgGk0nJ.xml", 	# ny times world  
			#r"https://rss.app/feeds/fHPzIIzHJVqtIjr3.xml", 	 	#Entrpreneur
			#r"https://rss.app/feeds/1Pqsw7njparMZi7B.xml",  	#wired
			#r"https://rss.app/feeds/feANofWEfawQKkQr.xml",		#Fast Company
			r"https://plato.stanford.edu/rss/sep.xml",		    #Philosophy Encyclopedia
			r"http://feeds.feedburner.com/tedtalks_video",		#ted Talk RSS Feed
			r"",
			r""
		  ]



for feed in rss_urls:
	Sift(feed,'wordsort.db')