from bs4 import BeautifulSoup
import codecs
import re

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
