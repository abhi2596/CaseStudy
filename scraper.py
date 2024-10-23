import requests 
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def scrape(website):
    response = requests.get(website)
    soup = BeautifulSoup(response.text,"html.parser")
    return soup

def get_all_links(website):
    response = requests.get(website)
    soup = BeautifulSoup(response.text,"html.parser")
    links = soup.find_all('a')
    redirect_links = []
    for link in links:
        href = link.get('href')
        if href:
            full_url = urljoin(website, href)
            redirect_links.append(full_url)
    return redirect_links