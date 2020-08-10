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
			r"https://www.ted.com/talks/ibram_x_kendi_the_difference_between_being_not_racist_and_antiracist",
			r"https://www.ted.com/talks/bill_gates_how_the_pandemic_will_shape_the_near_future/",
			r"https://www.ted.com/talks/matt_walker_how_caffeine_and_alcohol_affect_your_sleep",
			r"https://www.ted.com/talks/chloe_valdary_how_to_use_love_to_repair_social_inequality"
		  ]



for feed in rss_urls:
	Sift(feed,'wordsort.db')
