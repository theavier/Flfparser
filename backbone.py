from bs4 import BeautifulSoup
import requests
import re
from math import ceil

url = "https://www.friluftsframjandet.se/lat-aventyret-borja/hitta-aventyr/?showFullBookings=false&showClosedRegistration=false&filterBy=&startDate=null&endDate=null&query=&sortBy=&page=1&adventureTypes=Vandring&adventureTypes=Sn%C3%B6skor&adventureTypes=Vandring&counties=V%C3%A4stra%20G%C3%B6talands%20l%C3%A4n&organizers=&targetAudiences=&difficulties=&layout=banner"
#url = "https://www.friluftsframjandet.se/lat-aventyret-borja/hitta-aventyr/?showFullBookings=false&showClosedRegistration=false&filterBy=&startDate=null&endDate=null&query=&sortBy=&page=1&adventureTypes=&counties=V%C3%A4stra%20G%C3%B6talands%20l%C3%A4n&organizers=&targetAudiences=&difficulties=&layout=banner"
# https://www.friluftsframjandet.se/lat-aventyret-borja/hitta-aventyr/ # find categories

def get_soup(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    html_content = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html_content, "lxml")
    return soup


def get_count(url):
    soup = get_soup(url)
    should_continue = soup.find('div', class_='Pagination__Wrap')
    if (should_continue):
        value = re.findall(r'\d+', should_continue.text)
        return int(value[1]) if len(value) > 1 else None
    else:
        return None


def get_page_count(url):
    items_count = get_count(url)
    return ceil(items_count/40) if items_count > 40 else 1


def get_items(url):
    soup = get_soup(url)
    items = list()
    for link in soup.find_all('div', class_='AdventureCard-content'):
        item = {
            "titel": link.find("h6", class_="AdventureCard-heading").text,
            "description": link.find("p", class_="AdventureCard-description").text
        }
        items.append(item)
    return items

#item_list = get_items(url)
#print(item_list)

def get_pages(current_url):
    for i in range(1, get_page_count(url)+1):
        current_result = get_items(current_url)
        current_url = current_url.replace(f"&page={i}&", f"&page={i+1}&")
    return current_result

output = get_pages(url)
print(output)
print(f'count: {len(output)}')