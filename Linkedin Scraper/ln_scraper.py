# import libraries
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pandas as pd
import datetime
import time
import os


def browser(url):

    options=Options()
    options.headless=False
    
    driver = webdriver.Firefox(options=options,executable_path="") #Enter Path to geckodriver
    
    driver.get(url)
    
    return driver


def login(username,password):
    
    sign_in=driver.find_element_by_class_name('nav__button-secondary')
    sign_in.click()

    email=driver.find_element_by_id('username')
    secret_key=driver.find_element_by_id('password')


    # Enter username string
    email.send_keys(username) 

    # Enter password string
    secret_key.send_keys(password)

    login=driver.find_element_by_class_name('login__form_action_container')
    time.sleep(pause_time)
    login.click()

    print('logged in')

    return driver


def getnewpage():
    
    search_url=(f'https://www.linkedin.com/search/results/content/?keywords=%23&origin=SWITCH_SEARCH_VERTICAL')
    
    time.sleep(pause_time)
    driver.get(search_url)
    
    return driver



def scroll_through():
    start=time.time()
    elapsed=0

    last_height = driver.execute_script("return document.body.scrollHeight")

    count = 0

    while elapsed < 30:
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
    
    return required_html


def make_soup():
    soup = []
    soup=BeautifulSoup(required_html,'lxml')
    print('Done!')
    driver.quit()
    return soup


def make_lists():
    global links
    global hashtags
    global ation_words
    global ship_words
    
    links=[]
    hashtags=[]
    ation_words=[]
    ship_words = []
    all_links=[]
    
    all_links=soup.select('a')
    
    for link in all_links:
    
        if '#' in link.text and '\n' not in link.text and link.text not in hashtags: # search for '#' in all links and append to list
            hashtags.append(link.text)

    # filter hashtags with 'ation' or 'ship' at the end
    
    for tag in hashtags:
        if 'ation' in tag[-5:]:
            ation_words.append(tag)

        if 'ship' in tag[-4:]:
            ship_words.append(tag)


    print('links are ready')


def make_csv():

    hashtags.sort()

    df = pd.DataFrame(hashtags,columns=['Hashtags'])

    ation_df=pd.DataFrame(ation_words,columns=['-ation'])

    ship_df=pd.DataFrame(ship_words,columns=['-ation'])

    df.to_csv('hashtags.csv',header = False, index = False)
    ation_df.to_csv('ation.csv',header = False, index = False)
    ship_df.to_csv('ship.csv',header = False, index = False)
    
    print('files exported')



if __name__ == '__main__':
    
    base_start=time.time()
    pause_time=5 

    link='http://www.linkedin.com'

    username='' #Enter Username Here
    password='' #Enter Password Here

    driver=browser(link)

    driver=login(username,password)

    driver=getnewpage()

    required_html=scroll_through()

    soup=make_soup()

    make_lists()

    make_csv()

    t_elapsed=time.time()-base_start
    minutes=int(t_elapsed/60)
    seconds=int(t_elapsed/60)

    print('Done Scraping. Output file: hashtags.csv')
    print(f'Time to complete: {minutes}m {seconds}s')
