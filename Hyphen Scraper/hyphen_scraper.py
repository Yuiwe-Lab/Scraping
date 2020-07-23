from bs4 import BeautifulSoup
import requests
import pandas as pd
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
import time
import csv

start=time.time()
pause=2
href=[]
unique=[]


# gets all links from the page
def get_all_website_links(url):
    
    response=requests.get(url).content
    soup = BeautifulSoup(response,'html5lib')
    
    global href           
    href=[]
    
    #Search for <a /a> in html soup and extract links
    for a_tag in soup.find_all('a'):
        href_attr=a_tag.attrs.get('href')
        href.append(href_attr)
        if href =="" or href is None:
            continue


###### CREATE A LIST OF UNIQUE LINKS ON THE PAGE #########################
def unique_links():
    global unique
    unique=[]
    
    for link in href:
        if link not in unique:
            unique.append(link)

##############  Scrape for Text ####################################  

def crawl(link):

    url=link
    response=requests.get(url).content
    soup = BeautifulSoup(response,'html.parser')
    
    text = soup.find_all('p')
    if len(text)<1:
        print('No paragraphs in this page, page may only contain links')

        return None #if no paragraphs found, returns None. We will use this later.
    
    #print(text)
    
    else:
    
        text = soup.find_all(text=True)
        
 ##### CREATE BLACKLIST TO CLEAN OUTPUT ####### 

        set([t.parent.name for t in text])  # Commented out tags are included in scraping.

        blacklist = [
        '[document]',
         'a',
         #'blockquote',
         'button',
         'div',
         'em',
         'figcaption',
         'figure',
         #'h1',
         #'h2',
         #'h3',
         #'h4',
         'label',
         'li',
         #'p',
         'script',
         'small',
         'span',
         'strong',
         'style',
         'sup',
         'time',
         'title'
        ]


########################################################################### 

        output=''

        for t in text:
            if t.parent.name not in blacklist:
                output+='{} '.format(t)

        return output #returns string output of all the text in the link

###########################################################################

### TOKENIZE ###
def tokenize_and_clean():
	global tokens
	global tok_puncrem
	global tokens_numremoved
	global final_tokens
	global hyphenated

	tokens=[]
	tok_puncrem=[]
	tokens_numremoved=[]
	final_tokens=[]

	for i in range(len(list_of_texts)):
	    tokens+=word_tokenize(list_of_texts[i])

	### CLEAN UP TOKENS ####
	    
	### Remove stopwords
	stop = stopwords.words('english')
	punc=string.punctuation+'"'+"'"+"’"+'“'+'”'

	

	for token in tokens:
	    if (token not in punc) and (len(token)>1) and (token not in stop):
	        tok_puncrem.append(token)
	        
	        
	### Remove numerics
	        
	for token in tok_puncrem:
	    if token not in tokens_numremoved:
	        try:
	            float(token)
	        except:
	            tokens_numremoved.append(token)

	final_tokens=tokens_numremoved

	#Create list of hyphenated words
	for token in final_tokens:
	    if '-' in token:
	        hyphenated.append(token)

############################################################################

if __name__ == '__main__':
	
	url=input('Enter main URL:')  # Get URL from user input  

	get_all_website_links(url)

	print(f'{len(href)} links in total')  # prints out total number of links in the URL provided

	unique_links()

	num_links=int(input('How many links to crawl?:')) #Since some links might not contain any text, get number of links from user

	list_of_texts=[]
	hyphenated=[]
	list_of_links=[]

	#loop through links and crawl each
	for i in range(num_links):
	    time.sleep(pause)
	    temp_data=(crawl(unique[i]))
	    if temp_data==None:
	        list_of_links.append(unique[i])       #if no text in link, store as a possible link to scrape in the future
	        continue
	    else:
	        list_of_texts.append((temp_data))


	tokenize_and_clean()

	# for token in final_tokens:
	#     if '-' in token:
	#         hyphenated.append(token)


	file=open('hyphenated.csv','w')
	file.close()

	file=open('hyphenated.csv','a',newline='')
	with file:
		write=csv.writer(file)
		for item in hyphenated:
			write.writerow([item])
	file.close()


