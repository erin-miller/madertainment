import driver
import pandas as pd
import time
from selenium.common.exceptions import NoSuchElementException
import eventdate, eventtime, eventlocation, eventsetting
from datetime import datetime
import re

driver = driver.get_driver()

# dict used for date processing
month_to_number = {
    "January": "01",
    "February": "02",
    "March": "03",
    "April": "04",
    "May": "05",
    "June": "06",
    "July": "07",
    "August": "08",
    "September": "09",
    "October": "10",
    "November": "11",
    "December": "12"
}

def load_events():
    # this website doesn't use a button to load more events but instead relies on page indexing
    pass

def get_events():
    # create events dict
    events = {}

    # create index for searching https://today.wisc.edu/events/index.html?page=<index>
    index = 1
    url = "https://today.wisc.edu/events/index.html?page="
    driver.get("https://today.wisc.edu/events/index.html?page=" + str(index))

    while len(driver.find_elements("class name", "day-row-header")) > 0:
        # get headers. these headers contain dates
        headers = driver.find_elements("class name", "day-row-header")

        # get the events lists
        events_lists_by_day = driver.find_elements("class name", "events-list")

        # iterate through each day. events_list_by_day[i] cooresponds to the events on day headers[i]
        for i in range(len(headers)):
            # get the raw day in format: Sunday, November 12, 2023
            day_raw = headers[i].text
            
            # process day_raw into "MM-DD-YYYY" format
            year = day_raw.split(", ")[2]
            month = month_to_number[day_raw.split(", ")[1].split(" ")[0]]
            day = day_raw.split(", ")[1].split(" ")[1]
            date = month + "-" + day + "-" + year

            # get a list of events in this day
            events_in_day = events_lists_by_day[i].find_elements("class name", "event-details")

            # loop through each event in the day
            for j in range(len(events_in_day)):
                # create event dict to be added to events later
                event = {}

                # get the link on the name of the event to check in the next condition
                link = events_in_day[j].find_element("tag name", "a").get_property("href")

                pattern = re.compile(r'today\.wisc\.edu')
                match = pattern.search(link)
                if match:
                    # if the link in the name of the event is another today.wisc.edu link, we can get more details easily
                    
                    # save the current url
                    url_capture = driver.current_url

                    # update the driver to the new url
                    driver.get(link)

                    # TODO: scrape https://today.wisc.edu/events/view/188842 or similar
                    name = format_data(driver, "class name", "view-event-title")
                    category = None # TODO: maybe we can generate category from description?
                    price = format_data(driver, "class name", "event-cost")
                    description = format_data(driver, "class name", "event-description")
                    location = format_data(driver, "class name", "event-location")
                    time = format_data(driver, "class name", "event-time")
                    event_date = eventdate.EventDate(date=date)
                    event_setting = eventsetting.EventSetting(event_date, time, location)

                    # load data into event
                    event["name"] = name
                    event["category"] = category
                    event["price"] = price
                    event["description"] = description
                    event["setting"] = event_setting

                    # load event into events using setting as the key
                    events[event_setting] = event

                else:
                    # do nothing for now
                    pass
        
        # increment index by 1 and go to the next page
        index += 1
        driver.get("https://today.wisc.edu/events/index.html?page=" + str(index))
    # TODO: loop through https://today.wisc.edu/events/index.html?page=<n> until data stops getting found
    # TODO: for each page, scrape data
        # TODO: create event dict for each event
    # TODO: collect name, category, price (no prices here), description, setting (setting has date, location, time)
    # TODO: after collection, create setting, location, time
    # TODO: fill out event dict
    # TODO: add event to events dict using the setting as the key and event as value
    # return the events dict as a pandas series
    return pd.Series(events)


def format_data(event, tag_or_class, tag_or_class_name):
    # try to grab the data, and return None if for some reason the tag/class isn't found
    try:
        data = event.find_element(tag_or_class, tag_or_class_name).text
    except NoSuchElementException:
        data = None
    
    return data

# debug
events = get_events()
for event in events:
    print(event.to_json() + "\n")