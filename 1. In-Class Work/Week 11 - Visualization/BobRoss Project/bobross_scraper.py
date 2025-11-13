import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from requests import get
import time
import os


def parse_painting(file_name):
    """
    Takes the path to a saved HTML file from the twoinchbrush site and outputs a formatted dictionary from the results
    """
    with open(file_name, encoding="utf-8", mode='r') as file:
        soup = BeautifulSoup(file, 'html.parser')
    colors = soup.select('#color-list span ')
    painting_info = {
        'title':soup.select(".flex-grow-1")[0].get_text(),
        'episode':soup.select('.mb-3 span')[0].get_text(),
        'hexcolors':[i.get('data-hex') for i in colors],
        'color_names':[i.get('data-name') for i in colors],
        'tags':[i.get_text() for i in soup.select_one('.mb-2').select(' .color-list .badge')],
        'image_url':urljoin('https://www.twoinchbrush.com/painting/', soup.select('.col-md-6.mb-3 img')[0].get('src'))
    }
    return painting_info

# get a list of all links on the landing page 
links = []
for i in range(1, 18):
    print(i, end='\r')
    params = {'page':i}
    paintings = get('https://www.twoinchbrush.com/all-paintings', params=params)
    soup = BeautifulSoup(paintings.content, 'html.parser')
    links.extend([urljoin(paintings.url, i.get('href')) for i in soup.select('.bob-ross-painting-holder a')])
    time.sleep(.1)

# create a directory to hold the HTML from each page
os.makedirs('./bobross_paintings/', exist_ok=True)


# scrape data on each painintg (or skips if there is already a file in this directory.
for i in links:    
    newfile_name = i.replace('https://www.twoinchbrush.com/painting/', './bobross_paintings/') + ".html"
    if os.path.isfile(newfile_name):
        print('skipping', end='\r')
        next
    else:
        page = get(i)
        page.raise_for_status()  # will raise an error if no response
        with open(newfile_name, "w", encoding="utf-8") as file:
            file.write(page.text)
        time.sleep(.1)

# list all the files in the directory with a .html extension
all_pages = ['./bobross_paintings/' + i for i in os.listdir('./bobross_paintings/')  if '.html' in i ]

# read all the pages and parse the results
data = [parse_painting(i) for i in all_pages]

# make a data frame from the dictionary
paintings_df = pd.DataFrame(data)

# write the resulting file to json in the current working directory
paintings_df.to_json("bobross_data.json")