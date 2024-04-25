from bs4 import BeautifulSoup
import requests
import requests_cache
import re
from math import ceil
from dateutil.parser import parse

#url = "https://www.friluftsframjandet.se/lat-aventyret-borja/hitta-aventyr/?showFullBookings=false&showClosedRegistration=false&filterBy=&startDate=null&endDate=null&query=&sortBy=&page=1&adventureTypes=Vandring&adventureTypes=Sn%C3%B6skor&adventureTypes=Vandring&counties=V%C3%A4stra%20G%C3%B6talands%20l%C3%A4n&organizers=&targetAudiences=&difficulties=&layout=banner"
#url = "https://www.friluftsframjandet.se/lat-aventyret-borja/hitta-aventyr/?showFullBookings=false&showClosedRegistration=false&filterBy=&startDate=null&endDate=null&query=&sortBy=&page=1&adventureTypes=Vandring&adventureTypes=Sn%C3%B6skor#adventuretype#&counties=#county#&organizers=&targetAudiences=&difficulties=&layout=banner"
url = "https://www.friluftsframjandet.se/lat-aventyret-borja/hitta-aventyr/?showFullBookings=false&showClosedRegistration=false&filterBy=&startDate=null&endDate=null&query=&sortBy=&#adventuretype#&counties=#county#&organizers=&targetAudiences=&difficulties=&layout=banner"
baseurl = "https://www.friluftsframjandet.se"
#url = "https://www.friluftsframjandet.se/lat-aventyret-borja/hitta-aventyr/?showFullBookings=false&showClosedRegistration=false&filterBy=&startDate=null&endDate=null&query=&sortBy=&page=1&adventureTypes=&counties=V%C3%A4stra%20G%C3%B6talands%20l%C3%A4n&organizers=&targetAudiences=&difficulties=&layout=banner"
# https://www.friluftsframjandet.se/lat-aventyret-borja/hitta-aventyr/ # find categories

requests_cache.install_cache('github_cache', backend='sqlite', expire_after=250)


def get_soup(url: str) -> BeautifulSoup:
    """ creates soup from url """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    html_content = requests.get(url, headers=headers).text
    #soup = BeautifulSoup(html_content, "lxml")
    soup = BeautifulSoup(html_content, "html.parser")
    return soup


def get_count(url: str) -> int:
    """ returns pagination from page """
    soup = get_soup(url)
    should_continue = soup.find('div', class_='Pagination__Wrap')
    if (should_continue):
        value = re.findall(r'\d+', should_continue.text)
        return int(value[1]) if len(value) > 1 else None
    else:
        return None


def get_page_count(url: str) -> int:
    """ returns page count based on items """
    items_count = get_count(url)
    return ceil(items_count/40) if items_count > 40 else 1


def get_item_date(item: str) -> str:
    """ returns date based on partial date """
    item_date_raw = item.split("/")[-1]
    try:
        item_date = parse(item_date_raw, fuzzy=True) #.date() #.strftime("%Y-%m-%d")
    except:
        item_date = "N/A"
    #print(f'original: {item_date_raw}, inpreted: {item_date}, type: {type(item_date)}')
    return item_date


def get_items(url: str) -> list:
    """ returns dict in list with values from soup """
    soup = get_soup(url)
    items = list()
    result1 = soup.find_all('div', class_='AdventureCard-content')
    result2 = soup.find_all('a', class_='AdventureCard-contentLink')
    for i in range(len(result1)):
        item = {
            "titel": result1[i].find("h6", class_="AdventureCard-heading").text,
            "description": result1[i].find("p", class_="AdventureCard-description").text,
            "href": baseurl+result2[i].get("href"),
            "price": result2[i].find("span", class_="AdventureCard-price").text,
        }
        #item["date"] = get_item_date(item['description'])
        items.append(item)
    return items


#item_list = get_items(url)
#print(item_list)

def get_pages(current_url: str) -> str:
    """ loops content """
    for i in range(1, get_page_count(url)+1):
        current_result = get_items(current_url)
        current_url = current_url.replace(f"&page={i}&", f"&page={i+1}&")
    return current_result

#output = get_pages(url)
#print(output)
#print(f'count: {len(output)}')

# get adventure type
def get_adventuretype():
    soup = get_soup(baseurl)
    #result1 = soup.find_all('div', class_='HeadingGroup')
    result1 = soup.find_all('div', class_="option")
    result1 = soup.find_all("div", {"class": "option"})
    #result1 = soup.select_one(".Form_AdventureArea")
    #id Form_AdventureArea #option
    
    return result1

#print(get_adventuretype())