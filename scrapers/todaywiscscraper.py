import driver
import pandas as pd
import time
from selenium.common.exceptions import NoSuchElementException
import eventdate, eventtime, eventlocation, eventsetting
from datetime import datetime
import re
from concurrent.futures import ThreadPoolExecutor, as_completed # multithreading

driver1 = driver.get_driver()

# global list of events
events = {}

# create a dict of links and dates because we need to use multithreading to scrape a large amount of pages at once
# this dict will ONLY hold today.wisc.edu links because we need to load a large amount of pages seperately
# this list will be scraped in scrape()
links = {}

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

# helper method for scrape()
def scrape_page(url, date):
    global events
    # Initialize WebDriver
    driver_multi = driver.get_driver()

    # Navigate to the URL
    driver_multi.get(url)

    # create blank event
    event = {}

    name = format_data(driver_multi, "class name", "view-event-title")
    category = None # TODO: maybe we can generate category from description?
    price = format_data(driver_multi, "class name", "event-cost")
    description = format_data(driver_multi, "class name", "event-description")
    location = format_data(driver_multi, "class name", "event-location")
    time = format_data(driver_multi, "class name", "event-time")
    if time is not None:
        time = re.sub(r"\s", "", time)
    event_date = eventdate.EventDate(date=date)
    event_setting = eventsetting.EventSetting(event_date, time, location)

    # load data into event
    event["name"] = name
    event["category"] = category
    event["price"] = price
    event["description"] = description
    event["setting"] = event_setting

    # load event into events using setting as the key
    events[event_setting] = pd.Series(event)

    # quit the driver
    driver_multi.quit()

def scrape():

    # NOTE: to improve performance, you can take a subset of each of the below. 100 urls/dates runs pretty quick.

    urls = list(links.keys())
    dates = list(links.values())

    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(scrape_page, urls, dates)

def get_events():
    global events
    # create index for searching https://today.wisc.edu/events/index.html?page=<index>
    index = 1
    url = "https://today.wisc.edu/events/index.html?page="
    driver1.get("https://today.wisc.edu/events/index.html?page=" + str(index))

    while len(driver1.find_elements("class name", "day-row-header")) > 0:
        # get headers. these headers contain dates
        headers = driver1.find_elements("class name", "day-row-header")

        # get the events lists
        events_lists_by_day = driver1.find_elements("class name", "events-list")

        # iterate through each day. events_list_by_day[i] cooresponds to the events on day headers[i]
        for i in range(len(headers)):
            # get the raw day in format: Sunday, November 12, 2023
            day_raw = headers[i].text

            # process day_raw into "MM-DD-YYYY" format
            year = day_raw.split(", ")[2]
            month = month_to_number[day_raw.split(", ")[1].split(" ")[0]]
            day = day_raw.split(", ")[1].split(" ")[1]
            day_extended = day
            if len(day) == 1:
                day_extended = "0" + day
            date = month + "-" + day_extended + "-" + year

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
                    links[link] = date # add the link to be multithreaded later
                else:
                    # extract data
                    name = format_data(events_in_day[j], "class name", "event-title")
                    category = None # TODO: maybe use keywords to generate a category?
                    price = None # no price information on this page :(
                    description = None # no real description either
                    event_date = eventdate.EventDate(date)
                    time = format_data(events_in_day[j], "class name", "event-time")
                    if time is not None:
                        time = re.sub(r"\s", "", time)
                    event_location = format_data(events_in_day[j], "class name", "event-location")

                    setting = eventsetting.EventSetting(event_date, time, event_location)

                    # load the event into event
                    event["name"] = name
                    event["category"] = category
                    event["price"] = price
                    event["description"] = description
                    event["setting"] = setting

                    event = pd.Series(event)

                    # add event to events using setting as key and event as value
                    events[setting] = event

        index += 1
        driver1.get("https://today.wisc.edu/events/index.html?page=" + str(index))


    # after the while loop, go back to https://today.wisc.edu/events/day/<TODAY> in "YYYY-MM-DD" format and scrape that
    # for some reason https://today.wisc.edu/events/index.html?page=1 skips the current day

    current_date = datetime.now().strftime("%Y-%m-%d")

    url = "https://today.wisc.edu/events/day/" + current_date
    driver1.get(url)
    
    headers = driver1.find_elements("class name", "day-row-header")

    # get the events lists
    events_lists_by_day = driver1.find_elements("class name", "events-list")

    # iterate through each day. events_list_by_day[i] cooresponds to the events on day headers[i]
    for i in range(len(headers)):
        # get the raw day in format: Sunday, November 12, 2023
        day_raw = headers[i].text

        # process day_raw into "MM-DD-YYYY" format
        year = day_raw.split(", ")[2]
        month = month_to_number[day_raw.split(", ")[1].split(" ")[0]]
        day = day_raw.split(", ")[1].split(" ")[1]
        day_extended = day
        if len(day) == 1:
            day_extended = "0" + day
        date = month + "-" + day_extended + "-" + year

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
                links[link] = date # add the link to be multithreaded later
            else:
                # extract data
                name = format_data(events_in_day[j], "class name", "event-title")
                category = None # TODO: maybe use keywords to generate a category?
                price = None # no price information on this page :(
                description = None # no real description either
                event_date = eventdate.EventDate(date)
                time = format_data(events_in_day[j], "class name", "event-time")
                if time is not None:
                    time = re.sub(r"\s", "", time)
                event_location = format_data(events_in_day[j], "class name", "event-location")

                setting = eventsetting.EventSetting(event_date, time, event_location)

                # load the event into event
                event["name"] = name
                event["category"] = category
                event["price"] = price
                event["description"] = description
                event["setting"] = setting

                event = pd.Series(event)

                # add event to events using setting as key and event as value
                events[setting] = event

    # call scrape() to scrape the https://today.wisc.edu/events/view/<n> urls
    scrape()

    # return pandas series
    return pd.Series(events)


def format_data(event, tag_or_class, tag_or_class_name):
    # try to grab the data, and return None if for some reason the tag/class isn't found
    try:
        data = event.find_element(tag_or_class, tag_or_class_name).text
    except NoSuchElementException:
        data = None
    
    return data

# debug
# get_events()
# print()
# print(len(links))
# print(len(events))

# events_pd = pd.Series(events)

# json_data = events_pd.to_json()

# # Save the JSON data to a local file
# with open('output.json', 'w') as json_file:
#     json_file.write(json_data)