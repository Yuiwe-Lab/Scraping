#! python3
#~ mikey

import sqlite3
from sqlite3 import Error
import feedparser
from bs4 import BeautifulSoup
import requests





def create_master(feed_link):
	'''
	Returns list of tuples [(link),(ship_words),(ation_words),(hyphen_words)]
	'''
	master_list = []									#return Object
	feedpage = feedparser.parse(feed_link)				#call to feedparser
	for entry in feedpage.entries:
		link = entry.get("link")
		if "slashdot" in link[:35]:						#slasdot trim params
			link = link[:link.rfind("/")]
			to_trim = entry.get("summary")
			summ = wordize(to_trim[:to_trim.find("<p>")])
			sift_summ(summ,link,master_list)
		elif "sciencemag" in link[:30]:					#scienceman trim params
			link = link[:link.find("?")]
			to_trim = entry.get("summary")
			summ = wordize(to_trim[3:-4])
			sift_summ(summ,link,master_list)
		elif "popsci" in link[:25]:						#popsci trim params
			link = link[:link.find("?")]
			to_trim = entry.get("description")
			summ = wordize(to_trim)
			sift_summ(summ,link,master_list)
		elif "motherjones" in link[:30]:				#mother jones trim params
			res = requests.get(link)
			summary = res.text
			summary = soup_sandwich(summary)
			summary = summary[summary.find(".entry-header")+80:summary.find("Looking for news you can trust?")]
			sift_summ(wordize(summary),link,master_list)
		elif "randomcrit" in link[:35]:
			link = link[:46] 
			summ = wordize(entry.get("summary"))
			sift_summ(summ,link,master_list)
		elif "kottke" in link[:25]:
			summ = entry.get("summary")
			summ = soup_sandwich(summ)
			sift_summ(wordize(summ),link,master_list)
		elif "jmsardina1" in link[:35]:
			summary = entry.get("summary")
			summary = soup_sandwich(summary)
			sift_summ(wordize(summary),link,master_list)
		else:
			print(f"could not find a match for {link}")
	#for thing in master_list:
		#print(thing,"\n")
	return(master_list)

rss_urls = (r"http://science.sciencemag.org/rss/express.xml",			#list of RSS URLS to check
			r"http://rss.slashdot.org/Slashdot/slashdotMain",
			r"https://www.popsci.com/arcio/rss/",
			r"https://www.motherjones.com/feed/",
			r"https://randomcriticalanalysis.com/feed/",
			r"http://feeds.kottke.org/main",
			r"https://pine.blog/u/jmsardina1_editor/rss.xml"
			)	

#Filters
def soup_sandwich(text_with_html):
	soup = BeautifulSoup(text_with_html, 'html.parser')
	text = soup.find_all(text=True)
	output = ''
	stoplist = ['[document]','noscript','header','html','meta','head', 'input','script']
	for t in text:
		if t.parent.name not in stoplist:
			output += f'{t} '
	return output

			
def wordize(ts):						#once a large string with text is achieved, turn it into a list of words
	puncts = '''!()[]{};:"\,<>./?@#=$%^&*_~'''
	for char in ts:					#remove punctuation
		if char in puncts:
			ts = ts.replace(char,"")
	li = list(ts.split(" "))
	return li
	
def sift_summ(summary,link,li):						#sifting parameters
	ship_words = []
	ation_words = []
	hyphen_words = []
	neering_words = []
	counter = 0
	
	for word in summary:
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
		else:
			pass
	if counter > 0:
		tuple = (link,ship_words,ation_words,hyphen_words,neering_words)
		li.append(tuple) 
	elif counter == 0:
		pass

hyphen_except =["COVID-19","--","SARS-CoV-2","Covid-19","-","---"]
ation_except = []
ship_except = []
neering_except = []	
	
def db_connect(db_file):
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		print("Connecting...")
	except Error as e:
		print(e)
	return conn

def enter_words(table, w,lnk_id):
	if word_in_table(table,w) is True:
		duplicate_add(table,w)
	else:
		cur = conn.cursor()
		cur.execute(f"INSERT INTO {table}(word,link_id) VALUES (?,?)",(w,lnk_id))
		conn.commit()
	
def duplicate_add(table,wrd):
	duptb = "dup_" + table
	if word_in_table(duptb,wrd) is True:
		cur = conn.cursor()
		cur.execute(f"SELECT num FROM {duptb} WHERE word = ?",(wrd,))
		rows = cur.fetchall()
		if len(rows) == 1:
			t = rows[0]
			ut = t[0] + 1
			cur = conn.cursor()
			cur.execute(f"UPDATE {duptb} SET num = ? WHERE word = ?",(ut,wrd))
			conn.commit()
		
	else:
		cur = conn.cursor()
		cur.execute(f"INSERT INTO {duptb}(word,num) VALUES  (?,?)",(wrd,2))
		conn.commit()
		
		
def word_in_table(tb,drw):
	rows =[]
	cur = conn.cursor()
	cur.execute(f"SELECT (id) FROM {tb} WHERE word = ?",(drw,))
	rows = cur.fetchall()
	if len(rows) >= 1:
		return True
	else:
		return False
	
def make_tables(conn,*tables):
	if conn is not None:
		for i in tables:
			try:
				c = conn.cursor()
				c.execute(i)
			except Error as e:
				print(e)

#tables_in_db		
links_table_tb = '''CREATE TABLE IF NOT EXISTS links (
								link_id integer PRIMARY KEY,
								linkurl text NOT NULL
								); '''
ship_words_tb = '''CREATE TABLE IF NOT EXISTS ship_words (
								id integer PRIMARY KEY,
								word text NOT NULL,
								link_id INTEGER,
								CONSTRAINT fk_links
								FOREIGN KEY (link_id)
								REFERENCES links(link_id)
								); '''
								
ation_words_tb = '''CREATE TABLE IF NOT EXISTS ation_words (
								id integer PRIMARY KEY,
								word text NOT NULL,
								link_id INTEGER,
								CONSTRAINT fk_links
								FOREIGN KEY (link_id)
								REFERENCES links(link_id)
								); '''
								
hyphen_words_tb = '''CREATE TABLE IF NOT EXISTS hyphen_words (
								id integer PRIMARY KEY,
								word text NOT NULL,
								link_id INTEGER,
								CONSTRAINT fk_links
								FOREIGN KEY (link_id)
								REFERENCES links(link_id)
								); '''
								
neering_words_tb = '''CREATE TABLE IF NOT EXISTS neering_words (
								id integer PRIMARY KEY,
								word text NOT NULL,
								link_id INTEGER,
								CONSTRAINT fk_links
								FOREIGN KEY (link_id)
								REFERENCES links(link_id)
								); '''

dupe_neering = '''CREATE TABLE IF NOT EXISTS dup_neering_words (
								id integer PRIMARY KEY,
								word text NOT NULL,
								num INTEGER NOT NULL
								); '''
dupe_hyphen = '''CREATE TABLE IF NOT EXISTS dup_hyphen_words (
								id integer PRIMARY KEY,
								word text NOT NULL,
								num INTEGER NOT NULL
								); '''
dupe_ation = '''CREATE TABLE IF NOT EXISTS dup_ation_words (
								id integer PRIMARY KEY,
								word text NOT NULL,
								num INTEGER NOT NULL
								); '''	
dupe_ship =    '''CREATE TABLE IF NOT EXISTS dup_ship_words (
								id integer PRIMARY KEY,
								word text NOT NULL,
								num INTEGER NOT NULL
								); '''								



with db_connect('wordsort.db') as conn:									#Database Connection creates/checks in CWD
	make_tables(conn,links_table_tb,ship_words_tb,ation_words_tb,hyphen_words_tb,neering_words_tb,dupe_ship,dupe_ation,dupe_hyphen,dupe_neering)	#Creates tables for word management and foreign key
	for href in rss_urls:												#RSS Link loop start
		feed_analysis = create_master(href)									#make list of tuples [link,ship_words,...]
		for entry in feed_analysis:												#Entry loop start
			cur = conn.cursor()
			cur.execute("SELECT linkurl FROM links WHERE linkurl=?",(entry[0],))	#check if link is in database
			result = cur.fetchall()													
			if len(result) == 0:
				lnk_id = None
			#if no rows selected, its not in there
				cur = conn.cursor()
				print(entry)
				cur.execute("INSERT INTO links (linkurl) VALUES (?)",(entry[0],))	#put the link in the database
				conn.commit()
				lnk_id = cur.lastrowid												#check which row for relation to words
				print (lnk_id)
				if len(entry[1]) > 0:													#put words in respective tables
					for word in entry[1]:
						enter_words("ship_words",word,lnk_id)								##Explicit
				if len(entry[2]) > 0:		
					for word in entry[2]:
						enter_words("ation_words",word,lnk_id)
				if len(entry[3]) > 0: 		
					for word in entry[3]:
						enter_words("hyphen_words",word,lnk_id)
				if len(entry[4]) > 0:
					for word in entry[4]:
						enter_words("neering_words",word,lnk_id)
	print("I'm Done...")
print("connection Closed")