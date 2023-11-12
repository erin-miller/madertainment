from scrapers import driver
import pandas as pd
from scrapers import eventdate, eventtime, eventlocation, eventsetting
from datetime import datetime, timedelta
from selenium.common.exceptions import NoSuchElementException
import re

web_driver = driver.get_driver()
index = 1
url = "https://hilldale.com/events/list/page/"
links = []
events = {}

# collect all of the events' expanded links for scraping later
def load_events():
    global web_driver, index
    # get the 1st page
    web_driver.get("https://hilldale.com/events/list/page/" + str(index))

    # continue searching more pages until there's no more events
    while len(web_driver.find_elements("class name", "event-card-wrap")) > 0:
        
        # find all of the events
        events = web_driver.find_elements("class name", "event-card-wrap")

        # grab the link so we can get more detailed information later
        for event in events:
            links.append(event.find_element("tag name", "a").get_attribute("href"))
        
        # increment index and get the next page
        index += 1
        web_driver.get("https://hilldale.com/events/list/page/" + str(index))
    web_driver.quit()

def get_events():
    web_driver = driver.get_driver()
    for link in links:
        # load the page
        web_driver.get(link)

        # create event for this event
        event = {}

        # extract and parse data
        name = format_data(web_driver, "class name", "tribe-events-single-event-title")
        category = None # TODO: can we extract a category from name/description?
        price = None # unfortunately not much we can do here
        description = format_data(web_driver, "class name", "tribe-events-single-event-description")
        date_time_raw = format_data(web_driver, "class name", "subtitle")
        if '-' in date_time_raw and "|" not in date_time_raw:
            converted_date = convert_date_range(date_time_raw)
        else:
            converted_date = convert_single_date(date_time_raw)
        event_date = eventdate.EventDate(converted_date.replace('1900', '2023'))
        event_location = "Hilldale Shopping Mall" # no location info but they're all at hilldale
        event_time = extract_first_time(date_time_raw)
        if event_time is not None:
            event_time = re.sub(r"\s", "", event_time)

        event_setting = eventsetting.EventSetting(event_date, event_time, event_location)

        # load data into event
        event["name"] = name
        event["category"] = category
        event["price"] = price
        event["description"] = description
        event["setting"] = event_setting

        # add the event to events using setting as the key and event as the value
        events[event_setting] = pd.Series(event)

    # after all links have been scraped, return events as a pandas series
    web_driver.quit()
    return pd.Series(events)
        


def extract_first_time(event_str):
    time_match = re.search(r'\b\d{1,2}(:\d{2})? [APMapm.]+\b', event_str)
    if time_match:
        return time_match.group()
    return None

def convert_date_range(date_range):
    start_day, end_day = date_range.split(' - ')
    start_date = datetime.strptime(start_day, '%a, %B %d')
    end_date = datetime.strptime(end_day, '%a, %B %d')
    middle_date = start_date + (end_date - start_date) / 2
    return middle_date.strftime('%m-%d-%Y')

def convert_single_date(date_str):
    if "|" in date_str:
        date_str = date_str.split(" | ")[0]
    date = datetime.strptime(date_str, '%a, %B %d')
    return date.strftime('%m-%d-%Y')

def format_data(event, tag_or_class, tag_or_class_name):
    # try to grab the data, and return None if for some reason the tag/class isn't found
    try:
        data = event.find_element(tag_or_class, tag_or_class_name).text
    except NoSuchElementException:
        data = None
    
    return data

# debug
# load_events()
# events = get_events()
# for event in events:
#     print(event.to_json())