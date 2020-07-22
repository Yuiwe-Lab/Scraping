# import libraries
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pandas as pd
import datetime
import time
import os

base_start=time.time()
pause_time=5 
options=Options()
options.headless=False # Headless browser. Set False to open browser window

driver = webdriver.Firefox(options=options,executable_path=" ") #ENTER PATH TO GECKODRIVER

print("Headless Browser Initialized")

driver.get('http://www.linkedin.com')

print("Webpage loaded")

sign_in=driver.find_element_by_class_name('nav__button-secondary')

sign_in.click()

email=driver.find_element_by_id('username')

password=driver.find_element_by_id('password')


# Enter username string
email.send_keys('') 

# Enter password string
password.send_keys('')

login=driver.find_element_by_class_name('login__form_action_container')

time.sleep(pause_time)

login.click()

print('logged in')

hashtag_input=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
soup = []

for i in range(0,len(hashtag_input)):

    search_url=(f'https://www.linkedin.com/search/results/content/?keywords=%23{hashtag_input[i]}&origin=SWITCH_SEARCH_VERTICAL')
    
    time.sleep(pause_time)

    driver.get(search_url)

    start=time.time()

    elapsed=0

    last_height = driver.execute_script("return document.body.scrollHeight")

    count = 0

    while elapsed < 180:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # wait to load page
        time.sleep(pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height: # which means end of page
            break
        # update the last height
        last_height = new_height

        count+=1

        elapsed=time.time()-start

        print(f'...',end='')

    required_html=driver.page_source

    soup.append(BeautifulSoup(required_html,'lxml'))

    print(f'Soup {hashtag_input[i]} is ready')
    
print('Done!')  

driver.quit()


links=[]
hashtags=[]
all_links=[]
for i in range(len(soup)):
    all_links.append(soup[i].select('a'))

parse_links=[]

for link in all_links:
    for i in range(len(link)):
        parse_links.append(link[i])


for link in parse_links:
    
    if '#' in link.text and '\n' not in link.text and link.text not in hashtags: # search for '#' in all links and append to list
        hashtags.append(link.text)

print('links are ready')

hashtags.sort()

df = pd.DataFrame(hashtags,columns=['Hashtags'])

df.to_csv('hashtags.csv',header = False, index = False)

t_elapsed=time.time()-base_start
minutes=int(t_elapsed/60)
seconds=int(t_elapsed/60)

print('Done Scraping. Output file: hashtags.csv')
print(f'Time to complete: {minutes}m {seconds}s')