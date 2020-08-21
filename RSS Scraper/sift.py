#! python3
# ~mikey
#READ

import sqlite3
from sqlite3 import Error
import feedparser
from bs4 import BeautifulSoup
import requests



class Sift:
	feed_url = ''
	conn = None
	db = None
	
##Table Definitions

	def __init__(self, feed,db):
		self.feed_url = feed
		self.db = db
		self.sort_list = []
		self.feed_parse(self.feed_url)
		



	def feed_parse(self,feed_url):
		with self.db_connect(self.db) as conn:
			self.make_tables(self.conn,"ship_words",								#Add Table Name to Table list
									   "hyphen_words",
									   "ation_words",
									   "neering_words",
									   "hashtag_words",
									   "hashtag_words"
										)
##Source Definitions
																#Source Def: Getting to a single string of readable words
			if 'slashdot' in feed_url[:35]:								#Catch for link
				print("........Connecting to Slashdot!........")
				for link,entry in self.simple_fp(feed_url):		#Parse feed
					if self.link_in_db(link) == False:			#Check DB for link (already processed)
						ar = self.wordize(entry)
						self.exec_sift(link,ar)
				self.sort_entries()
#I	
	
			elif 'sciencemag' in feed_url[:30]:
				print("........Connecting to Science magazine!........")
				for link,entry in self.simple_fp(feed_url):
					if self.link_in_db(link) == False:
						ar = self.wordize(entry)
						self.exec_sift(link,ar)
				self.sort_entries()
	
	
			elif '1Pqsw7njparMZi7B' in feed_url:
				print("........Connecting to Wired Magazine........")
				for e,z in self.simple_req(feed_url,True):
					if self.link_in_db(e) == False:	
						link = e
						summary = z[z.find('Search Backchannel Business Culture Gear ')+64:z.rfind("Facebook Twitter Pinterest Youtube")]
						if "You must  login or create an account  to comment" in summary:
							summary = "nerp"
						self.exec_sift(link,summary)
				self.sort_entries()
	
			
			elif 'fHPzIIzHJVqtIjr3' in feed_url:
				print("........Connecting to Entrepreneur Magazine........")
				for e,z in self.simple_req(feed_url,True):
					if self.link_in_db(e) == False:
						summary = z[:z.find("More from Entrepreneur")]
						if "contributors are their own." in summary:
							summary = summary[summary.find("contributors are their own.")+27:]
						if "Disclosure: Our goal is to feature products and servi" in summary or "zergnet-widget" in summary:
							summary = "nerp"
						if "font-family: 'Trim';" in summary:
							summary = summary[summary.rfind("accordance with our  Privacy Policy")+168:]
						if "Subscribe to our email list and be in the know" in summary:
							summary = summary[:summary.find(" Join The Newsletter")]
						summary = self.wordize(summary)		
						self.exec_sift(e,summary)
				self.sort_entries()
#S		
			elif "https://plato.stanford.edu/rss/sep.xml" in feed_url:
				print("........Connecting to The Stanford Philosophy Encyclopedia........")
				for e,z in self.simple_req(feed_url,True):
					if self.link_in_db(e) == False:
						z = z[z.rfind("BEGIN ARTICLE HTML"):z.rfind("Bibliography")]
						ar = self.wordize(z)
						self.exec_sift(e,ar)
				self.sort_entries()
			
			elif 'motherjones' in feed_url[:35]:
				print("........Connecting to Mother Jones........")
				for e,z in self.simple_req(feed_url, True):
					if self.link_in_db(e) == False:
						ar = z[z.find(".entry-header")+80:z.find("Looking for news you can trust?")]
						ar = self.wordize(ar)
						self.exec_sift(e,ar)
				self.sort_entries()
			
			elif 'popsci' in feed_url[:35]:
				print("........Connecting to Popular Science........")
				for e,z in self.simple_fp(feed_url):
					if self.link_in_db(e) == False:
						ar = self.wordize(z)
						self.exec_sift(e,ar)
				self.sort_entries()
			
			elif "http://feeds.feedburner.com/tedtalks_video" in feed_url:
				print("........Connecting to TED.com RSS for transcript........")
				for e,z in self.simple_fp(feed_url):
					lnk = "https://www.ted.com/talks" + e[e.rfind("/"):] + "/transcript"
					if self.link_in_db(lnk) == False:
						chk = requests.get(lnk)
						if chk.ok:
							ar = chk.text
							ar = self.soup_sandwich(ar)
							ar = ar[ar.find("Transcript text")+16:ar.find("/Transcript text")]
							ar = self.wordize(ar)
							self.exec_sift(lnk,ar)								
				self.sort_entries()	
#H			
			
					
			#elif...
			else:
				print(f"NO MATCH FOR {feed_url}","\n")
			
			
			
##Search Term Definitions			

	def ship_words(self,article_words): 				 #Article words, a list of words prduced by wordize
		ship_except = [] 				 		  			#term except table
		li = []
		for word in article_words:
			if 'ship' in word[-4:]: 						   #Catch Word
				if word not in ship_except and word not in li:    #Filter
					li.append(word)  								#Add Word to list
		return li  													   #Return list of words meeting criteria
		
	def hyphen_words(self,article_words):
		hyphen_except = ["-","--","---","covid-19","sars-cov-2"]
		li =[]
		for word in article_words:
			if '-' in word:
				if word.find('-') == word.rfind('-') and word not in hyphen_except and word not in li:
					if '-' not in word[:1] and '-' not in word[-1:]:
						li.append(word)
		return li
#M	
	def ation_words(self,aw):
		ation_except = []
		li = []
		for word in aw:
			if 'ation' in word[-5:]:
				if word not in ation_except and word not in li:
					li.append(word)
		return li
		
	def neering_words(self,aw):
		neering_except = []
		li = []
		for word in aw:
			if 'neering' in word[-7:]:
				if word not in neering_except and word not in li:
					li.append(word)
		return li
	
	def hashtag_words(self,aw):
		hashtag_except = ["#",]
		li = []
		for word in aw:
			if '#' in word[:1]:
				if word not in hashtag_except and word not in li:
					li.append(word)
		return li
	
#Access Definitions
	def simple_fp(self,url,souped = False):
		il = []
		for entry in feedparser.parse(url).entries:
			lnk = entry.get('link')
			summ = entry.get('summary')
			if souped == True:
				summ = self.soup_sandwich(summ)
			il.append((lnk,summ))
		return il
#A		
	def simple_req(self,url,souped = False):
		il = []
		for entry in feedparser.parse(url).entries:
			lnk = entry.get("link")
			summ = requests.get(lnk).text
			if souped == True:
				summ = self.soup_sandwich(summ)
			il.append((lnk,summ))
		return il
			
			
			
			
#Filter Definitions

	def wordize(self, ts):						
		puncts = '''!()[]{};:"\,<>./?@=$%^&*_~'''
		ts = ts.lower()
		for char in ts:					#remove punctuation
			if char in puncts:
				ts = ts.replace(char,"")
		g_replace = [("\n"," "),("\xa0"," "),("\t","")]
		for c,r in g_replace:
			ts = ts.replace(c,r)
		li = list(ts.split(" "))
		li = [i for i in li if len(i) < 37]
		return li	

	def soup_sandwich(self,text_with_html):
		soup = BeautifulSoup(text_with_html, 'html.parser')
		text = soup.find_all(text=True)
		output = ''
		stoplist = ['[document]','noscript','header','html','meta','head', 'input','script']
		for t in text:
			if t.parent.name not in stoplist:
				output += f'{t} '
		return output
		
#E		
		
##Execute Sift	
	
	def exec_sift(self,link, ar):
		flag = None
		check = ((link,						#Add search term definition to execute tuple
				  self.ship_words(ar),
				  self.ation_words(ar),
				  self.hyphen_words(ar),
				  self.neering_words(ar),
				  self.hashtag_words(ar)))
		ctr = len(check)-1
		while ctr > 0:
			if len(check[ctr]) > 0:
				flag = True
			ctr -= 1
		if flag == True:
			#print(check)		  
			self.sort_list.append(check)	
	
	def db_connect(self, db_file):
		conn = None
		try:
			conn = sqlite3.connect(db_file)
		except Error as err:
			print(err)
		self.conn = conn
		return conn
		
##Entry Definitions		

	def sort_entries(self):
	#	with self.db_connect(self.db) as conn:
			
		for entry in self.sort_list:	
			print(entry,"\n")
			cur = self.conn.cursor()
			cur.execute("INSERT INTO links (linkurl) VALUES (?)",(entry[0],))
			self.conn.commit()
			lnk_id = cur.lastrowid
			if len(entry[1]) > 0:									#if a list with items is in this postion in the	tuple			
				for word in entry[1]:
					self.enter_words("ship_words",word,lnk_id)			#Enter Words into database
			if len(entry[2]) > 0:							
				for word in entry[2]:										##Explicit Term Entry
					self.enter_words("ation_words",word,lnk_id)
			if len(entry[3]) > 0: 		
				for word in entry[3]:
					self.enter_words("hyphen_words",word,lnk_id)
			if len(entry[4]) > 0:
				for word in entry[4]:
					self.enter_words("neering_words",word,lnk_id)
			if len(entry[5]) > 0:												
				for word in entry[5]:
					self.enter_words("hashtag_words",word,lnk_id)
		
#L
	
	def make_tables(self,conn,*tables):
		if conn is not None:
			try:
				c = conn.cursor()
				c.execute('''CREATE TABLE IF NOT EXISTS links (
								link_id integer PRIMARY KEY,
								linkurl text NOT NULL
								);''')
				conn.commit()
			except Error as err:
				print(err)
				
		for name in tables:
			if conn is not None:
				try:
					c = conn.cursor()
					c.execute(f'''CREATE TABLE IF NOT EXISTS {name} (
								id integer PRIMARY KEY,
								word text NOT NULL,
								link_id INTEGER,
								CONSTRAINT fk_links
								FOREIGN KEY (link_id)
								REFERENCES links(link_id)
								);''')
					conn.commit()
				except Error as err:
					print(err)
				try:
					c = conn.cursor()
					c.execute(f'''CREATE TABLE IF NOT EXISTS {'dup_'+name} (
								id integer PRIMARY KEY,
								word text NOT NULL,
								num INTEGER NOT NULL
								);''')
					conn.commit()
				except Error as err:
					print(err)
			
	def enter_words(self,table, w,lnk_id):
		if self.word_in_table(table,w) is True:
			duptb = "dup_" + table
			if self.word_in_table(duptb,w) is True: # Increment Usage Number
				cur = self.conn.cursor()
				cur.execute(f"SELECT num FROM {duptb} WHERE word = ?",(w,))
				rows = cur.fetchall()
				if len(rows) == 1:
					t = rows[0]
					ut = t[0] + 1
					self.commit_to_table(f"UPDATE {duptb} SET num = ? WHERE word = ?",(ut,w))
				
			else:  # First Duplicate
				self.commit_to_table(f"INSERT INTO {duptb}(word,num) VALUES  (?,?)",(w,2))
		self.commit_to_table(f"INSERT INTO {table}(word,link_id) VALUES (?,?)",(w,lnk_id))
		
	def word_in_table(self,table,word):
		rows =[]
		cur = self.conn.cursor()
		cur.execute(f"SELECT (id) FROM {table} WHERE word = ?",(word,))
		rows = cur.fetchall()
		if len(rows) >= 1:
			return True
		else:
			return False	

	def link_in_db(self,link):
		rows = []
		cur = self.conn.cursor()
		cur.execute("SELECT link_id FROM links WHERE linkurl = ?",(link,))
		rows = cur.fetchall()
		if len(rows) >= 1:
			return True
		else:
			return False	
	
	def commit_to_table(self,sql,data):
		cur = self.conn.cursor()
		cur.execute(sql,data)
		self.conn.commit()
		
