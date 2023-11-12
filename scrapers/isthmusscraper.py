from scrapers import driver
import pandas as pd
import time
from selenium.common.exceptions import NoSuchElementException
from scrapers import eventdate, eventtime, eventlocation, eventsetting
from datetime import datetime
import re
from concurrent.futures import ThreadPoolExecutor, as_completed # multithreading
import random

# global events list
events = {}

# url init
url = "https://isthmus.com/search/event/calendar-of-events/#page="

# this specifc website has a massive event list that goes over 2 years in advance, at least.
# due to the number of pages to scrape we will have to use multithreading
urls = []

# number of pages to load. each page has 30 events.
num_pages = 200

for i in range(num_pages+1):
    if i == 0:
        continue
    urls.append(url + str(i))

# nothing to load
def load_events():
    pass

def get_events():
    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(scrape, urls)

    return pd.Series(events)

def scrape(url):
    # set up driver
    driver_multi = driver.get_driver()
    driver_multi.get(url)

    # allow page to load
    time.sleep(random.randint(2, 5))

    # each page has multiple events
    events_list = driver_multi.find_elements("class name", "event_result")

    for event_item in events_list:
        # init empty dict
        event = {}

        # extract data
        name = format_data(event_item, "class name", "event_title")
        location = event_item.find_elements("tag name", "a")[1].text
        if location == "":
            location = None
        else:
            location = location.lower().split()
            capitalized_words = [word.capitalize() for word in location]
            location = ' '.join(capitalized_words)
        category = format_data(event_item, "class name", "cats").split(", ")[0].lower().capitalize()
        price = None # TODO: maybe search description for a price
        description = format_data(event_item, "class name", "description")
        raw_date = format_data(event_item, "class name", "event_date")
        event_date = convert_to_date(raw_date)
        match_time = re.search(r"\d{1,2}:\d{2} [APMapm]{2}", raw_date)
        if match_time:
            event_time = match_time.group().replace(" ", "")
        event_setting = eventsetting.EventSetting(event_date, event_time, location)

        # load values into event
        event["name"] = name
        event["category"] = category
        event["price"] = price
        event["description"] = description
        event["setting"] = event_setting
        
        # add event to events using setting as key
        events[event_setting] = pd.Series(event)


def convert_to_date(input_string):
    month_abbreviations = {
        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
        'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
        'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
    }

    date_parts = input_string.split(' ')
    month = month_abbreviations[date_parts[0]]
    day = date_parts[1].replace(',', '')
    year = date_parts[2]

    date_str = f'{month}-{day}-{year}'

    return date_str

def format_data(event, tag_or_class, tag_or_class_name):
    # try to grab the data, and return None if for some reason the tag/class isn't found
    try:
        data = event.find_element(tag_or_class, tag_or_class_name).text
    except NoSuchElementException:
        data = None
    
    return data

# debug
# load_events()
# events_s = get_events()
# for event in events_s:
#     print(event.to_json())

# print(len(events_s))