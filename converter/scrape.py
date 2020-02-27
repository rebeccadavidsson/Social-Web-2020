from bs4 import BeautifulSoup
import codecs
import re
from datetime import datetime
import time

import os
module_dir = os.path.dirname(__file__)  # get current directory
file_path = os.path.join(module_dir, 'templates/output.html')


def scrape_whole_html():
    soup = BeautifulSoup(codecs.open("templates/output.html"), 'html.parser')

    year = "2020" # TODO: DIT IS TIJDELIJK GEHARDCODED
    month_dict = {"januari": "01", "februari": "02", "maart": "03"} #TODO: OOIT MOET DIT NAAR ENGELS

    all_p = soup.find_all('p')
    date = ""
    for i,_ in enumerate(all_p):

        # get correct date in correct format
        if all_p[i]['class'][0] == 'title':
            date = all_p[i].get_text()
            for key in month_dict:
                if key in date:
                    month = month_dict[key]
                    break
            day = re.search(r'\d+', date).group()
            if len(day) == 1:
                day = "0" + day
            date = year + "-" + month + "-" + day

        # get all info of a class
        if i + 5 >= len(all_p):
            break
        else:

            # check if i is at the correct element for the link
            link = all_p[i]
            for a in link.find_all('a', href=True):

                # deal with the date element
                if all_p[i + 1]['class'][0] == 'title':
                    i += 1

                # get all information
                time = all_p[i + 1].get_text()
                sort = all_p[i + 2].get_text()
                studio = all_p[i + 3].get_text()
                trainer = all_p[i + 4].get_text()
                link = a['href']

                # set time in correct format (DATETIME)
                starttime = date + "T" + time[0:5] + ":00"
                endtime = date + "T" + time[-5:] + ":00"

                # hierzo opslaan in de class (want alleen hier de categoriën goed lol)
                print(starttime, endtime, sort, studio, trainer, link)


def scrape_item(input):

    dict = {}

    soup = BeautifulSoup(input, 'html.parser')

    all_p = soup.find_all('p')
    print(all_p, "hoi")
    timedate = all_p[0].get_text().split("-")
    start = timedate[0].split(":")
    end = timedate[1].split(":")

    start1 = int(start[0].strip(""))
    start2 = int(start[1].strip(""))
    end1 = int(end[0].strip(""))
    end2 = int(end[1].strip(""))

    # convert day
    datum = all_p[5].get_text()
    print(datum)
    day = 29             # TODO GEHARDCODE
    month = 2           # TODO GEHARDCODE
    year = 2020

    print(start1, start2, end1, end2, "HA")
    # TODO: DAY!
    start_time = datetime(year, day, month, start1, start2, 0)
    end_time = datetime(year, day, month, end1, end2, 0)

    dict["day"] = day
    dict["start"] = start_time
    dict["end"] = end_time
    dict["sort"] = all_p[1].get_text()
    dict["studio"] = all_p[2].get_text()
    dict["teacher"] = all_p[3].get_text()

    print(dict)
    print()

    return dict
