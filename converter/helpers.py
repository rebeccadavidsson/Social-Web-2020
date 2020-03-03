import os
from subprocess import call


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
