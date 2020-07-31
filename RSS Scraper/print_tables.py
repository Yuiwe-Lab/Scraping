
import sqlite3
from sqlite3 import Error



def db_connect(db_file):
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		print("Connecting...\n")
	except Error as e:
		print(e)
	return conn
	
def display_words(t,pw = False):
	with db_connect('wordsort.db') as conn:
		cur = conn.cursor()
		cur.execute(f"SELECT word FROM {t}")
		rows = cur.fetchall()
		print(f"      {len(rows)} words in {t} Table")
		li = []
		for word in rows:
			if word not in li:
				li.append(word)
		print(f"       {len(li)} unique entries")
		if pw is True:
			for s in li:
				print (s)
			
		#for i in rows:
			#print(i)
			
def display_freq(t):
	with db_connect('wordsort.db') as conn:
		duptb = "dup_"+ t
		cur = conn.cursor()
		cur.execute(f"SELECT word,num FROM {duptb}")
		rows = cur.fetchall()
		print(f"{len(rows)} in dup_{t} \n")
		for row in rows:
			print(row)

def report(*tables):
	for table in tables:
		display_words(table)
		display_freq(table)
		
		
			
report("hyphen_words","ation_words", "ship_words","neering_words")
#display_words("hyphen_words", pw = True)
