#Script to generate formatted list of browser histories with durations between each site visit.
from browser_history.browsers import Firefox
from browser_history.browsers import Chromium
import json
import datetime
import csv

#Set path
path = "/path_to_project/"

#Function to pull raw browser histories.
def generate_raw_browser_histories(browser_type, browser_name):
    b = browser_type
    outputs = b.fetch_history()
    outputs.save(path + f"{browser_name}_histories.json")
    with open(path + f"{browser_name}_histories.json", 'r') as his_file:
        his = json.load(his_file) 
    return his


#Function to generate cleaned list of browser histories, with elapsed times between each website visit.
def history_list(histories):
    hist_list = []
    for i in range(1,  len(histories["history"])):
        obj = dict.fromkeys(["Timestamp", "URL", "TimeElapsed(min)"])
        obj["Timestamp"] = histories["history"][i-1]["Timestamp"]
        if i != len(histories["history"]) - 1:
            date_time_obj = datetime.datetime.strptime(histories["history"][i-1]["Timestamp"], '%Y-%m-%dT%H:%M:%S%z')    
            date_time_obj2 = datetime.datetime.strptime(histories["history"][i]["Timestamp"], '%Y-%m-%dT%H:%M:%S%z')
            difference = date_time_obj2 - date_time_obj
            min_difference = difference.total_seconds()/60
            obj["TimeElapsed(min)"] = min_difference 
        else:
            obj["TimeElapsed(min)"] = None
        if '&' in histories["history"][i-1]["URL"]:
            obj["URL"] = histories["history"][i-1]["URL"].split('&')[0]
        else:
            obj["URL"] = histories["history"][i-1]["URL"]
        hist_list.append(obj) 
    return hist_list


#Function to write browser history lists to a CSV file.
def browser_list_write(browser, hist_list):
    with open(path + f"{browser}_history_cleaned.csv", 'w', newline='') as fout:
        writer = csv.DictWriter(fout, fieldnames = ["Timestamp", "URL", "TimeElapsed(min)"])
        writer.writeheader()
        writer.writerows(hist_list)

#Generate raw browser history lists for Firefox and Chromium.
firefox_histories = generate_raw_browser_histories(Firefox(), "Firefox")
chromium_histories = generate_raw_browser_histories(Chromium(), "Chromium")

#Call browser history function for Chromium and Firefox web browsers
#to clean/shorten website URLs and calculate time intervals for site
#visits.
firefox_hist_list = history_list(firefox_histories)
chromium_hist_list = history_list(chromium_histories)


#Write formatted browser histories to CSV files.
browser_list_write("Firefox", firefox_hist_list)
browser_list_write("Chromium", chromium_hist_list)

