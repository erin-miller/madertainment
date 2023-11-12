from scrapers import unionscraper
from scrapers import todaywiscscraper
import pandas as pd
import json
import numpy as np

pretty_json_string = ""

def update_data():
    # load and get today.wisc.edu events
    todaywiscscraper.load_events()
    today_wisc_events = todaywiscscraper.get_events()

    # load and get union events
    unionscraper.load_events()
    union_events = unionscraper.get_events()

    # get raw values for all events
    today_raw = today_wisc_events.values
    union_raw = union_events.values

    # combine all raw data into one np array
    combined_raw_data = np.concatenate((today_raw, union_raw), axis=0)

    # create and format the json string containing all data
    all_data_as_json = "["
    for i in range(len(combined_raw_data)):
        all_data_as_json += combined_raw_data[i].to_json()
        if i != len(combined_raw_data)-1:
            all_data_as_json += ", "
    all_data_as_json += "]"

    # make the json string look nice
    pretty_json_string = json.dumps(json.loads(all_data_as_json), indent=2)

    # write the resulting json to "all_json.json"
    with open("flask/data.json", 'w') as json_file:
        json_file.write(pretty_json_string)

def get_json_as_string():
    if len(pretty_json_string) == 0:
        # the data hasn't been loaded yet
        return None
    else:
        return pretty_json_string