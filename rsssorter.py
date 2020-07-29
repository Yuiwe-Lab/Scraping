#! python3
#~ mikey

import sqlite3
from sqlite3 import Error
import feedparser


def create_master(feed_link):
	'''
	Returns list of tuples [(link),(ship_words),(ation_words),(hyphen_words)]
	'''
	master_list = []									#return Object
	feedpage = feedparser.parse(feed_link)				#call to feedparser
	for entry in feedpage.entries:
		link = entry.get("link")
		if "slashdot" in link[:35]:						#slasdot trim params
			link_junk = link.rfind("/")
			link = link[:link_junk]
			to_trim = entry.get("summary")
			junk = to_trim.find("<p>")
			summ = to_trim[:junk]
			summ = wordize(summ)
			sift_summ(summ,link,master_list)
		elif "sciencemag" in link[:30]:					#scienceman trim params
			link_junk = link.find("?")
			link = link[:link_junk]
			to_trim = entry.get("summary")
			summ = to_trim[3:-4]
			summ = wordize(summ)
			sift_summ(summ,link,master_list)
		elif "popsci" in link[:25]:						#popsci trim params
			link_junk = link.find("?")
			link = link[:link_junk]
			to_trim = entry.get("summary")
			summ = wordize(to_trim)
			sift_summ(summ,link,master_list)
		elif "motherjones" in link[:30]:				#mother jones trim params
			summ = wordize(entry.get("summary")) 		#lucky i guess
			sift_summ(summ,link,master_list)
		else:
			print(f"could not find a match for {link}")
	#for thing in master_list:
		#print(thing,"\n")
	return(master_list)

rss_urls = (r"http://science.sciencemag.org/rss/express.xml",			#list of RSS URLS to check
			r"http://rss.slashdot.org/Slashdot/slashdotMain",
			r"https://www.popsci.com/arcio/rss/",
			r"https://www.motherjones.com/feed/"
			)	


def wordize(ts):						#once a large string with text is achieved, turn it into a list of words
	puncts = '''!()[]{};:"\,<>./?@#$%^&*_~'''
	for char in ts:					#remove punctuation
		if char in puncts:
			ts = ts.replace(char,"")
	li = list(ts.split(" "))
	return li
	
def sift_summ(summary,link,list):						#sifting parameters
	ship_words = []
	ation_words = []
	hyphen_words = []
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
			if word not in hyphen_words and word not in hyphen_except:
				hyphen_words.append(word)
				counter += 1
		else:
			pass

	if counter > 0:
		tuple = (link,ship_words,ation_words,hyphen_words)
		list.append(tuple) 
	elif counter == 0:
		pass

hyphen_except =["COVID-19","--","SARS-CoV-2","Covid-19","-"]
ation_except = []
ship_except = []
		
def db_connect(db_file):
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		print("Connecting...")
	except Error as e:
		print(e)
	return conn
	
def make_tables(conn,*tables):
	if conn is not None:
		for i in tables:
			try:
				c = conn.cursor()
				c.execute(i)
			except Error as e:
				print(e)

#tables_in_db		
links_table = '''CREATE TABLE IF NOT EXISTS links (
								link_id integer PRIMARY KEY,
								linkurl text NOT NULL
								); '''
ship_words = '''CREATE TABLE IF NOT EXISTS ship_words (
								id integer PRIMARY KEY,
								ship_word text NOT NULL,
								link_id INTEGER,
								CONSTRAINT fk_links
								FOREIGN KEY (link_id)
								REFERENCES links(link_id)
								); '''
								
ation_words = '''CREATE TABLE IF NOT EXISTS ation_words (
								id integer PRIMARY KEY,
								ation_word text NOT NULL,
								link_id INTEGER,
								CONSTRAINT fk_links
								FOREIGN KEY (link_id)
								REFERENCES links(link_id)
								); '''
								
hyphen_words = '''CREATE TABLE IF NOT EXISTS hyphen_words (
								id integer PRIMARY KEY,
								hyphen_word text NOT NULL,
								link_id INTEGER,
								CONSTRAINT fk_links
								FOREIGN KEY (link_id)
								REFERENCES links(link_id)
								); '''
		



with db_connect('wordsort.db') as conn:									#Database Connection creates/checks in CWD
	make_tables(conn,links_table,ship_words,ation_words,hyphen_words)	#Creates tables for word management and foreign key
	for href in rss_urls:												#RSS Link loop start
		feed_analysis = create_master(href)									#make list of tuples [link,ship_words,...]
		for entry in feed_analysis:												#Entry loop start
			cur = conn.cursor()
			cur.execute("SELECT linkurl FROM links WHERE linkurl=?",(entry[0],))	#check if link is in database
			result = cur.fetchall()													
			if len(result) == 0:							#if no rows selected, its not in there
				lnk_id = None															
				cur = conn.cursor()
				print(entry)
				cur.execute("INSERT INTO links (linkurl) VALUES (?)",(entry[0],))	#put the link in the database
				conn.commit()
				lnk_id = cur.lastrowid												#check which row for relation to words
				print (lnk_id)
				if len(entry[1]) > 0:													#put words in respective tables
					for word in entry[1]:
						cur = conn.cursor()
						cur.execute("INSERT INTO ship_words(ship_word,link_id) VALUES (?,?)",(word,lnk_id))
						conn.commit()
				if len(entry[2]) > 0:		
					for word in entry[2]:
						cur = conn.cursor()
						cur.execute("INSERT INTO ation_words(ation_word,link_id) VALUES (?,?)",(word,lnk_id))
						conn.commit()
				if len(entry[3]) > 0: 		
					for word in entry[3]:
						cur = conn.cursor()
						cur.execute("INSERT INTO hyphen_words(hyphen_word,link_id) VALUES (?,?)",(word,lnk_id))
						conn.commit()
	print("I'm Done...")
print("connection Closed")
