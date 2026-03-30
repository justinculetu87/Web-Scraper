import requests
from bs4 import BeautifulSoup as bs
import os
from urllib.parse import urljoin, urlparse
import re

#give option to enter what url it is
def get_url_input():
    print("===Web Scraper - Hyperlink Download===\n")
    enter_url = input('Enter the URL to scrape: ').strip()
    if not enter_url.startswith(("http://", "https://")):
        url = "https://" + enter_url

    folder = input("Enter a file path to download the files (press Enter for user downloads): ").strip()
    if not folder:
        folder = './downloads'
    
    return url, folder

def get_downloads(url, folder):
    os.makedirs(folder, exists_ok=True)
    print(f"\nFetching page: {url}")
    headers = {"User-Agent": "Mozilla/5.0"} #http for modern browsers
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    get_soup = bs(response.text, "html.parser")
    links = get_soup.find_all("a", href=True)
    print(f"Found {len(links)} hyperlinks.\n")

    downloaded, skipped = 0, 0

    for link in links:
        href = link["href"]
        full_url = urljoin(url, href) #handle partial urls








def get_soup(url):  #define function to get the files
    return bs(requests.get(url).text, 'html.parser')

for link in get_soup(enter_url).find_all('a'):
    file_link = link.get('href')
    if file_type in file_link:
        print(file_link)
        with open(link.text, 'wb') as file:
            response = requests.get(enter_url + file_link)
            file.write(response.content)