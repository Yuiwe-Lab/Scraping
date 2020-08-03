#! python3
# ~mikey

import sqlite3
from sqlite3 import Error
import feedparser
from bs4 import BeautifulSoup
import requests


class Source:
	source_url = ''
	src_master_list = []
	
	def __init__(self,url):
		self.source_url = url
		self.sort_link(self.source_url)
	
	def sort_link(self,url):
		if 'popsci' in url[:35]:
			self.popsci_source(url)
		elif 'slashdot' in url[:35]:
			self.slashdot_source(url)
		elif 'motherjones' in url[:35]:
			self.mojo_source(url)	
		elif "sciencemag" in url[:30]:
			self.scimag_source(url)
		elif "uVCDwng32TgGk0nJ.xml" in url:
			self.nyt_source(url)
		elif "JyMVgKu36v8JT4H0.xml" in url:
			self.nytbus_source(url)
	#	elif "new_source_trigger" :								Source Trigger (add source #1/2)
	#		self.new_source_definition(url)
			
		else:
			print(f"No match for {url}")
			
#source Definitions yield portions of src_master_list	
	def popsci_source(self,url):
		for entry in self.simple_fp(url):
			trim_link = entry[0][:entry[0].find("?")]
			self.sift(self.wordize(entry[1]),trim_link)
			
	def slashdot_source(self,url):
		for entry in self.simple_fp(url):
			trim_link = entry[0][:entry[0].rfind("/")]
			self.sift(self.wordize(entry[1]),trim_link)
			
	def mojo_source(self,url):
		for entry in self.simple_req(url, True):
			trim_link = entry[0]
			summary = entry[1][entry[1].find(".entry-header")+80:entry[1].find("Looking for news you can trust?")]
			self.sift(self.wordize(summary),trim_link)
			
	def scimag_source(self,url):
		for entry in self.simple_fp(url):
			trim_link = entry[0][:entry[0].find("?")]
			summary = entry[1][3:-4]
			self.sift(self.wordize(summary),trim_link)
			
	def nyt_source(self,url):
		for e in self.simple_req(url,True):
			trim_link = e[0][:-5]
			if 'THIS IS A GENERATED TEMPLATE FILE. DO NOT EDIT.' in e[1]:
				if e[1].rfind("THIS IS A GENERATED TEMPLATE FILE. DO NOT EDIT.") == e[1].find("THIS IS A GENERATED TEMPLATE FILE. DO NOT EDIT."):
					summary = e[1][e[1].find("Continue reading the main story"):e[1].rfind("THIS IS A GENERATED TEMPLATE FILE. DO NOT EDIT.")]
				else:
					summary = e[1][e[1].find("Continue reading the main story"):e[1].rfind("THIS IS A GENERATED TEMPLATE FILE. DO NOT EDIT.")]
					summary = summary[:summary.rfind("THIS IS A GENERATED TEMPLATE FILE. DO NOT EDIT.")]
			else:
				summary = e[1][e[1].find("Skip to content Skip to site index")+47:e[1].rfind("Times Company NYTCo")-109]
				
			if '#masthead' in summary[:300]:
				summary = summary[summary.rfind("Continue reading the main story"):]
			self.sift(self.wordize(summary),trim_link)
			
	def nytbus_source(self,url):
		for e in self.simple_req(url,True):
			trim_link = e[0][:-5]
			summary = e[1][e[1].find("|")+2:e[1].rfind("Advertisement")]
			if "@media"in summary[:200]:
				summary = summary[summary.find("Continue reading the main story"):]
			if 'IS IS A GENERATED TEMPLATE FILE. DO NOT EDIT.' in summary:
				summary = summary[summary.rfind("Continue reading the main story"):summary.find("IS IS A GENERATED TEMPLATE FILE. DO NOT EDIT.")] + summary[summary.rfind("|"):]
			if "ai2html" in summary:
				while "ai2html" in summary:
					summary = summary[:summary.find("ai2html")-14] + summary[summary.find('End ai2html')+12:]
					summary = summary[summary.find("|")+2:]
					summary = summary[summary.find("|")+24:]
			self.sift(self.wordize(summary),trim_link)
			
	
#	def new_source_definition(self, url):									Source Definition (add SOurce 2/2)	
#		for entry in feed: or wahtever
#			define trim link
#			define summary (a single string of words separated by spaces)
#			self.sift(self.wordize(summary),trim_link)
			
	
#access definitions
	def simple_fp(self,url,souped = False):
		il = []
		for entry in feedparser.parse(url).entries:
			lnk = entry.get('link')
			summ = entry.get('summary')
			if souped == True:
				summ = self.soup_sandwich(summ)
			il.append((lnk,summ))
		return il
		
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
		
			
#main sift			
	def sift(self,list_trimmed_words,link):
		ship_words = [];	ship_except = 	 []
		ation_words = [];	ation_except =	 []
		hyphen_words = [];	hyphen_except =  ["--","sars-cov-2","covid-19","-","---"]
		neering_words = [];	neering_except = []														#add term #1 
		hashtag_words = []; hashtag_except = []
		counter = 0
	
		for word in list_trimmed_words:
			if word[-4:] == 'ship':
				if word not in ship_words and word not in ship_except:
					ship_words.append(word)
					counter += 1
			if word[-5:] == 'ation':
				if word not in ation_words and word not in ation_except:
					ation_words.append(word)
					counter += 1
			if "-" in word:
				if word not in hyphen_words and word not in hyphen_except and word[:4] != "href":
					hyphen_words.append(word)
					counter += 1
			if word[-7:] == 'neering':
				if word not in neering_words and word not in neering_except:
					neering_words.append(word)
					counter += 1
			if word[:1] == "#":
				if word not in hashtag_words and word not in hashtag_except:
					hashtag_words.append(word)

		if counter > 0:
			tuple = (link,ship_words,ation_words,hyphen_words,neering_words,hashtag_words)						#add term #3
			self.src_master_list.append(tuple) 
		elif counter == 0:
			pass
			
	
				
	
		
		
class Populate_Tables:
	database = ''
	li = []
	master_list = []
	conn = None
	
	def __init__(self, db, rss_feeds):
		self.database = db
		self.conn = self.db_connect(self.database)
		self.make_tables(self.conn,"ship_words","ation_words","hyphen_words","neering_words","hashtag_words")		#add term #4
		self.li = rss_feeds
		for feed in self.li:
			p = Source(feed).src_master_list
			for m_entry in p:
				self.master_list.append(m_entry)
		
		for entry in self.master_list:
			if self.link_in_db(entry[0]) is False:
				print(entry,"\n")
				#enter data	
				cur = self.conn.cursor()
				cur.execute("INSERT INTO links (linkurl) VALUES (?)",(entry[0],))
				self.conn.commit()
				lnk_id = cur.lastrowid
				if len(entry[1]) > 0:													#put words in respective tables
					for word in entry[1]:
						self.enter_words("ship_words",word,lnk_id)								##Explicit
				if len(entry[2]) > 0:		
					for word in entry[2]:
						self.enter_words("ation_words",word,lnk_id)
				if len(entry[3]) > 0: 		
					for word in entry[3]:
						self.enter_words("hyphen_words",word,lnk_id)
				if len(entry[4]) > 0:
					for word in entry[4]:
						self.enter_words("neering_words",word,lnk_id)
				if len(entry[5]) > 0:												#add term #5
					for word in entry[5]:
						self.enter_words("hashtag_words",word,lnk_id)
		if self.conn:
			self.conn.close()
	
	def db_connect(self, db_file):
		self.conn = None
		try:
			conn = sqlite3.connect(db_file)
			print("Connecting...")
		except Error as e:
			print(e)
		return conn

	def enter_words(self,table, w,lnk_id):
		if self.word_in_table(table,w) is True:
			self.duplicate_add(table,w)
		else:
			cur = self.conn.cursor()
			cur.execute(f"INSERT INTO {table}(word,link_id) VALUES (?,?)",(w,lnk_id))
			self.conn.commit()
	
	def duplicate_add(self,table,wrd):
		duptb = "dup_" + table
		if self.word_in_table(duptb,wrd) is True: # Increment Usage Number
			cur = self.conn.cursor()
			cur.execute(f"SELECT num FROM {duptb} WHERE word = ?",(wrd,))
			rows = cur.fetchall()
			if len(rows) == 1:
				t = rows[0]
				ut = t[0] + 1
				cur = self.conn.cursor()
				cur.execute(f"UPDATE {duptb} SET num = ? WHERE word = ?",(ut,wrd))
				self.conn.commit()
		
		else:  # First Duplicate
			cur = self.conn.cursor()
			cur.execute(f"INSERT INTO {duptb}(word,num) VALUES  (?,?)",(wrd,2))
			self.conn.commit()
		
		
	def word_in_table(self,tb,drw):
		rows =[]
		cur = self.conn.cursor()
		cur.execute(f"SELECT (id) FROM {tb} WHERE word = ?",(drw,))
		rows = cur.fetchall()
		if len(rows) >= 1:
			return True
		else:
			return False	

	def link_in_db(self,trim_link):
		rows = []
		cur = self.conn.cursor()
		cur.execute("SELECT link_id FROM links WHERE linkurl = ?",(trim_link,))
		rows = cur.fetchall()
		if len(rows) >= 1:
			return True
		else:
			return False
	
	def create_word_tables(self,conn,table_name):
		if conn is not None:
			try:
				c = conn.cursor()
				c.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
								id integer PRIMARY KEY,
								word text NOT NULL,
								link_id INTEGER,
								CONSTRAINT fk_links
								FOREIGN KEY (link_id)
								REFERENCES links(link_id)
								);''')
				conn.commit()
			except Error as e:
				print(e)
			try:
				c = conn.cursor()
				c.execute(f'''CREATE TABLE IF NOT EXISTS {'dup_'+table_name} (
								id integer PRIMARY KEY,
								word text NOT NULL,
								num INTEGER NOT NULL
								);''')
				conn.commit()
			except Error as e:
				print(e)
				
	def make_tables(self,conn,*tables):
		if conn is not None:
			try:
				c = conn.cursor()
				c.execute('''CREATE TABLE IF NOT EXISTS links (
								link_id integer PRIMARY KEY,
								linkurl text NOT NULL
								);''')
				conn.commit()
			except Error as e:
				print(e)
		for name in tables:
			self.create_word_tables(conn,name)
			
	

	



	
	
	
	
	
