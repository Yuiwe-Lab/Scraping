## Linkedin Scraper

Currently the scraper searches for hashtags and stores them into a csv file.
Uses sylenium to access linkedin using a headless browser. It then utilizes the linkedin search function with a predifined search term (currently #a-#z).
Since linkedin uses infinite scroll, the scraper scrolls trough each page for a pre-defined time and then the html code of the page is filtered to create a list of all hastags that show up.
The list is then eported to a csv file.

## geckodriver required

## Packages Required:
    bs4
    requests
    selenium
    pandas
                    
#### Be sure to have "geckodriver" placed in a local directory and script pointing to correct path.

