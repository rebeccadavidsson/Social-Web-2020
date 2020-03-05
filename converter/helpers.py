import os
from subprocess import call
from datetime import date
import datetime


def convertdate(date):

    month_dict = {1: "January", 2: "February", 3: "March", 4: "April"}
    temp = date.split("T")[0].split("-")
    month, day = temp[1], temp[2]
    total_string = str(int(day)) + " " + month_dict.get(int(month))

    return total_string


def refreshschedule():

    # if os.path.exists('./converter/templates/output.html'):
    #     os.remove('./converter/templates/output.html')
    # else:
    call(["node", "scraper/scraper.js"])

    return True


def geteventday(events):

    today = today = date.today()
    previousevents, futurevents = [], []
    for event in events:
        date_time_str = event.start
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S')

        if date_time_obj.date() < today:
            previousevents.append(event)
        else:
            futurevents.append(event)

    return previousevents, futurevents
