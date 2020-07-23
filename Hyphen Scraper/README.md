## Hyphen Scraper

Currently the scraper asks the used for a URL and is based around the Forbes website.

as a starting point, you cant try and use the following URL:

"https://www.forbes.com/innovation/#746589796834"

The program will then sift through the link and since the website may not contain any substantial body of text, ask the user to again input the number of sub-links to sift through. 
After this, the scraper will sift through bodies of text and tokenize it. The list is then cleaned. the criteria can be seen in the code. 
Current output is a csv file containing all words in the text foud to contin a hyphen.

## Packages Required:
    bs4
    requests
    pandas
    nltk
    string
    csv
                    


