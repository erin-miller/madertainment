import driver
import pandas as pd
import time
from selenium.common.exceptions import NoSuchElementException

driver = driver.get_driver()
driver.get("https://union.wisc.edu/events-and-activities/event-calendar/")

def load_events(seconds = 3):
    # locate the "load more" button
    load_button = driver.find_element("class name", "js-infinite-scroll__btn")
    
    # continue to click on "load more" until we have all of the events loaded
    last = -1
    curr = len(driver.find_elements("class name", "event-list-item"))
    while last != curr:
        last = curr
        # click the button to load 9 more events
        driver.execute_script("arguments[0].click();", load_button)

        # give the page a second to load
        # NOTE: 3 seconds seems to be consistent. if the page loads slower, the loading may stop and we may not get all of the events
        time.sleep(seconds)

        # update curr
        curr = len(driver.find_elements("class name", "event-list-item"))

        # debug: see how many events are being loaded
        # print(curr)

def get_events():
    # init list of events
    events = []

    # get the elements from selenium webdriver 
    raw_events = driver.find_elements("class name", "event-list-item")

    # loop through each event
    for raw_event in raw_events:

        # create empty dict
        event = {}

        # get month
        month = format_data(raw_event, "class name", "event-list-item--date-badge--month")
        event["month"] = month

        # get day
        day = format_data(raw_event, "class name", "event-list-item--date-badge--day")
        event["day"] = day

        # get name
        name = format_data(raw_event, "tag name", "h3")
        event["name"] = name

        # get category
        category = format_data(raw_event, "class name", "event-list-item-category")
        event["category"] = category

        # get location
        location = format_data(raw_event, "class name", "event-list-item--location")
        event["location"] = location

        # get price
        price = format_data(raw_event, "class name", "event-list-item--tickets")
        event["price"] = price

        # get time
        time = format_data(raw_event, "class name", "event-list-item--time")
        event["time"] = time

        # get description
        description = format_data(raw_event, "class name", "event-list-item--desc")
        event["description"] = description

        # convert the event dict into a pandas series and append it to the events list
        events.append(pd.Series(event))
    
    return events

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
# for e in events:
#     print(e["description"])