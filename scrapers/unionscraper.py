from scrapers import driver
import pandas as pd
import time
from selenium.common.exceptions import NoSuchElementException
from scrapers import eventdate, eventtime, eventlocation, eventsetting
from datetime import datetime
import re

# dict for converting Union-specific month format "JAN, FEB, etc." to month numbers 01-12
month_dict = {
    'JAN': '01',
    'FEB': '02',
    'MAR': '03',
    'APR': '04',
    'MAY': '05',
    'JUN': '06',
    'JUL': '07',
    'AUG': '08',
    'SEP': '09',
    'OCT': '10',
    'NOV': '11',
    'DEC': '12'
}

web_driver = driver.get_driver()
web_driver.get("https://union.wisc.edu/events-and-activities/event-calendar/")

def load_events(seconds = 3):
    # locate the "load more" button
    load_button = web_driver.find_element("class name", "js-infinite-scroll__btn")
    
    # continue to click on "load more" until we have all of the events loaded
    last = -1
    curr = len(web_driver.find_elements("class name", "event-list-item"))
    while last != curr:
        last = curr
        # click the button to load 9 more events
        web_driver.execute_script("arguments[0].click();", load_button)

        # give the page a second to load
        # NOTE: 3 seconds seems to be consistent. if the page loads slower, the loading may stop and we may not get all of the events
        time.sleep(seconds)

        # update curr
        curr = len(web_driver.find_elements("class name", "event-list-item"))

        # debug: see how many events are being loaded
        # print(curr)

def get_events():
    # init dict of events
    events = {}

    # get the elements from selenium webdriver 
    raw_events = web_driver.find_elements("class name", "event-list-item")

    # loop through each event
    for raw_event in raw_events:

        # create empty dict
        event = {}

        # get month
        month = format_data(raw_event, "class name", "event-list-item--date-badge--month")
        # event["month"] = month

        # get day
        day = format_data(raw_event, "class name", "event-list-item--date-badge--day")
        # event["day"] = day

        # get name
        name = format_data(raw_event, "tag name", "h3")
        event["name"] = name

        # get category
        category = format_data(raw_event, "class name", "event-list-item--category")
        event["category"] = category

        # get location
        location = format_data(raw_event, "class name", "event-list-item--location")
        # event["location"] = location

        # get price
        price = format_data(raw_event, "class name", "event-list-item--tickets")
        event["price"] = price

        # get time
        time = format_data(raw_event, "class name", "event-list-item--time")
        # event["time"] = time

        # get description
        description = format_data(raw_event, "class name", "event-list-item--desc")
        event["description"] = description
        
        # convert the month 'APR' into '04'
        month_as_num = month_dict[month]
        
        # standardize the date format. Union's website formats the 3rd as '3'. convert it to '03'.
        day_extended = day
        if len(day) == 1:
            day_extended = "0" + day

        # get the current year. start by assuming the event is in this year
        event_year = datetime.now().year

        # if the event's month is less than the current month, we know it's in the next calendar year
        if int(month_as_num) < datetime.now().month:
            event_year += 1

        event_date = eventdate.EventDate(month_as_num + '-' + day_extended + '-' + str(event_year))

        # remove spaces from event time to standardize
        event_time = re.sub(r"\s", "", time)

        # create event_setting
        event_setting = eventsetting.EventSetting(event_date, event_time, location)

        # add event_setting to the event so we can access setting information later
        event["setting"] = event_setting

        # append the event to events as a pandas series using the setting as the key
        events[event_setting] = pd.Series(event)
    
    # convert events into a pandas series and return
    return pd.Series(events)

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
#     print(e.to_json())