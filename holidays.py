import datetime
import json
from unittest import result
from anyio import typed_attribute
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
from datetime import datetime as dt
from matplotlib.pyplot import text

#Files

text_file = open("menu.txt")
menu_lines = text_file.readlines()
text_file.close()

holidays_seed = open('holidays.json')
seed = json.load(holidays_seed)
holidays_seed.close()


#Querys

def getHTML(url):
    response = requests.get(url)
    return response.text

#Weather API
url = "https://community-open-weather-map.p.rapidapi.com/climate/month"
querystring = {"q":"Minneapolis"}
headers = {
	"X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
	"X-RapidAPI-Key": "99edfc553emsh39e5c6842d0d192p1b9907jsn19f2a0887c95"
}
try:
    response = requests.request("GET", url, headers=headers, params=querystring)
    response = response.json()
except:
    print('The weather API is down, at the moment.')
else:
    avgTemp = []
    for day in response['list']:
        avgTemp.append(day['temp']['average'])

#Outer Helper Functions

class Holiday: 
    def __init__(self,namevalue, datevalue):
        self.__name = namevalue
        self.__date = datevalue

    def __str__ (self):
        return f'{self.__name} ({str(self.__date)[0:10]})'

    def get_name(self):
        return self.__name

    def print_name(self):
        return str(self.__name)

    def set_name(self,newname):
        self._name = newname

    def get_date(self):
        return self.__date

    def print_date(self):
        return str(self.__date)[0:10]
#moved upwards. used to be right above the holiday list object

def format_date_object(string):
    year = string[0:4]
    if string[5] == '0':
        month = string[6]
    else:
        month = string[5:7]
    day = string[8:10]
    return dt(int(year),int(month),int(day))

def format_md(year,semi_raw_date):
        semi_raw_date = semi_raw_date.split(" ")
        if semi_raw_date[0] == "Jan":
            semi_raw_date[0] = 1
            return dt(year,semi_raw_date[0],int(semi_raw_date[1]))
        elif semi_raw_date[0] == "Feb":
            semi_raw_date[0] = 2
            return dt(year,semi_raw_date[0],int(semi_raw_date[1]))
        elif semi_raw_date[0] == "Mar":
            semi_raw_date[0] = 3
            return dt(year,semi_raw_date[0],int(semi_raw_date[1]))
        elif semi_raw_date[0] == "Apr":
            semi_raw_date[0] = 4
            return dt(year,semi_raw_date[0],int(semi_raw_date[1]))
        elif semi_raw_date[0] == "May":
            semi_raw_date[0] = 5
            return dt(year,semi_raw_date[0],int(semi_raw_date[1]))
        elif semi_raw_date[0] == "Jun":
            semi_raw_date[0] = 6
            return dt(year,semi_raw_date[0],int(semi_raw_date[1]))
        elif semi_raw_date[0] == "Jul":
            semi_raw_date[0] = 7
            return dt(year,semi_raw_date[0],int(semi_raw_date[1]))
        elif semi_raw_date[0] == "Aug":
            semi_raw_date[0] = 8
            return dt(year,semi_raw_date[0],int(semi_raw_date[1]))
        elif semi_raw_date[0] == "Sep":
            semi_raw_date[0] = 9
            return dt(year,semi_raw_date[0],int(semi_raw_date[1]))
        elif semi_raw_date[0] == "Oct":
            semi_raw_date[0] = 10
            return dt(year,semi_raw_date[0],int(semi_raw_date[1]))
        elif semi_raw_date[0] == "Nov":
            semi_raw_date[0] = 11
            return dt(year,semi_raw_date[0],int(semi_raw_date[1]))
        elif semi_raw_date[0] == "Dec":
            semi_raw_date[0] = 12
            return dt(year,semi_raw_date[0],int(semi_raw_date[1]))
        else:
            print('warning, not all semi-raw dates are of the same format')
 #helper function for scrapeHTML()

def scrape_one_year(year):
    try:
        html = getHTML("https://www.timeanddate.com/holidays/us/" + str(year)) #Years[position])
        soup = BeautifulSoup(html,'html.parser')
        table = soup.find('table',attrs = {'id':'holidays-table'})
    except:
        print('There was a problem acesssing the server.')
    else:
        for row in table.find_all('tbody'):
            cells = row
        raw_dates = cells.find_all('th',class_='nw')
        raw_names = cells.find_all('a')
    #Empty lists for the dates and holiday names
        date_list = []
        name_list = []
        dict_list = []
    #populating lists
        for item in raw_dates:
            date_list.append(item.text)
        for item in raw_names:
            name_list.append(item.text)

        date_objects = list(map(lambda x: format_md(year,x), date_list))

        for holidaynum in range(0,len(date_list)):
            dictX = Holiday(name_list[holidaynum],date_objects[holidaynum])
            dict_list.append(dictX)
        #return dictlist?

        result_dict = []
        for i in range(0,len(dict_list)):
            if dict_list[i].get_name() not in list(map(lambda x: x.get_name(), dict_list[i + 1:])): ##and dict_list[i].get_date() not in list(map(lambda x: x.get_date(), dict_list[i + 1:])): 
                result_dict.append(dict_list[i])
#function taken from devenum.com to remove duplicate holidays
        return result_dict

class HolidayList:
    def __init__(self):
       self.innerHolidays = []
    
    def get_holidayList(self):
        return self.innerHolidays

    def removeHoliday(self,name,date):
        try:
            format_date_object(date)
        except:
            print('Your date must be in the format \'yyyy-mm-dd\'')
        else:
            result_found = False
            for holiday in self.innerHolidays:
                if holiday.get_name() == name and holiday.get_date() == format_date_object(date):
                    self.innerHolidays.remove(holiday)
                    print('Removed ' + name + ' from the draft Holiday-list.')
                    result_found = True
            if not result_found:
                print('This holiday does not exist in the draft. Make sure you have the name written correctly.')

    def __str__(self):
        revealed_list = map(lambda x: str(x), self.innerHolidays)
        return str(list(revealed_list))

    def addHoliday(self,nameinput,dateinput):
        try:
            format_date_object(dateinput)
        except:
            print('Your date must be in the format of \'yyyy-mm-dd\'')
        else:
            replaced_value = False
            for dict in self.innerHolidays: #get_holidayList():
                if dict.get_name() == nameinput and dict.get_date().year == format_date_object(dateinput).year:
                    #replaced_value = False
                    while not replaced_value:
                        replace_input = input('There\'s already a ' + nameinput + ' in ' + str(dict.get_date())[0:4] + ' would you like to replace it? [y/n]: ')
                        if replace_input.lower() == 'y':
                            self.innerHolidays.remove(dict)
                            self.innerHolidays.append(Holiday(nameinput,format_date_object(dateinput)))
                            print(nameinput + ' now exists at ' + dateinput + ' in the draft Holiday-list.\n')
                            replaced_value = True
                        elif replace_input.lower() == 'n':
                            print('\nNo Holiday has been added.')
                            replaced_value = True
                            break
                        else:
                            print('Input must be either \'y\' or \'n\'')
                            continue
            if replaced_value:
                print('Finished!\n')
            else:
                self.innerHolidays.append(Holiday(nameinput,format_date_object(dateinput)))
                print(nameinput + f'({dateinput[0:10]})' + ' has been added to your draft of Holidays!')

    def scrapeHolidays(self):
        full_list = []
        years = [2020,2021,2022,2023,2024]
        for anum in years:
            full_list = full_list + scrape_one_year(anum)
        for i in range(0,len(full_list)):
            self.innerHolidays.append(full_list[i])

#Menu Functions

def showMainMenu():
    for num in range(4,11):
        print(menu_lines[num-1].strip())

def showAddingMenu():
    for num in range(12,14):
        print(menu_lines[num-1].strip())

def showSubtractingMenu():
    for num in range(15,17):
        print(menu_lines[num-1].strip())

def showSavingMenu():
    for num in range(18,20):
        print(menu_lines[num-1].strip())

def showViewingMenu():
    for num in range(22,24):
        print(menu_lines[num-1].strip())

def showExitMenu():
    for num in range(25,29):
        print(menu_lines[num-1].strip())

#vieweing/weather functions

def create_weeklist_by_year(list1,year):
    for num in range(0,52):
        list1.append((dt(year,1,1)+datetime.timedelta(days=(7*num))))
    list1.append(dt(year+1,1,1))

bgdt2020 = []
bgdt2021 = []
bgdt2022 = []
bgdt2023 = []
bgdt2024 = []
create_weeklist_by_year(bgdt2020,2020)
create_weeklist_by_year(bgdt2021,2021)
create_weeklist_by_year(bgdt2022,2022)
create_weeklist_by_year(bgdt2023,2023)
create_weeklist_by_year(bgdt2024,2024)

def grabweeknum_by_year(beginlist,date):
    pos = 0
    cycles = len(beginlist)
    while cycles > 0:
        if date >= beginlist[pos] and date < beginlist[pos+1]:
            return pos+1
        else:
            pos = pos + 1
            cycles = cycles - 1
    print('an error occured')

def getweeknum(date):
    if date.year == 2020:
        return grabweeknum_by_year(bgdt2020,date)
    elif date.year == 2021:
        return grabweeknum_by_year(bgdt2021,date)
    elif date.year == 2022:
        return grabweeknum_by_year(bgdt2022,date)
    elif date.year == 2023:
        return grabweeknum_by_year(bgdt2023,date)
    elif date.year == 2024:
        return grabweeknum_by_year(bgdt2024,date)
    else:
        print('This date is out of range')

def return_date(holid):
    return holid.get_date()

def return_year(holid):
    return holid.year

def convert_date_to_week_position(holiday):
    today = dt.today()
    today_reduced = dt(today.year,today.month,today.day)
    if holiday.get_date() == today_reduced:
        return 0
    elif holiday.get_date() == today_reduced+datetime.timedelta(days=1):
        return 1
    elif holiday.get_date() == today_reduced+datetime.timedelta(days=2):
        return 2
    elif holiday.get_date() == today_reduced+datetime.timedelta(days=3):
        return 3
    elif holiday.get_date() == today_reduced+datetime.timedelta(days=4):
        return 4
    elif holiday.get_date() == today_reduced+datetime.timedelta(days=5):
        return 5
    elif holiday.get_date() == today_reduced+datetime.timedelta(days=6):
        return 6
    else:
        return 0

def show_coming_holidays_with_weather(innerList):
    today = dt.today()
    this_year_pool = []
    for holiday in innerList:
        if holiday.get_date().year == today.year:
            this_year_pool.append(holiday)
    this_week = list(filter(lambda x: getweeknum(x.get_date()) == getweeknum(today), this_year_pool))
    days_left_this_week = list(filter(lambda x: x.get_date() >= dt(today.year,today.month,today.day), this_week))
    for item in days_left_this_week:
        print(str(item) + ' - Temp: ' + str(avgTemp[convert_date_to_week_position(item)]))

def legal_menu_inp(inputx):
    try:
        int(inputx)
    except:
        print('Your input must be a number from 1 to 5')
        return False
    else:
        if int(inputx) >= 1 and int(inputx) <= 5:
            return True

def addingMenu(innerHolidayList):
    still_adding = True
    while still_adding:
        holiday_input = input('Holiday: ')
        date_input = input('Date: ')
        innerHolidayList.addHoliday(holiday_input,date_input)
        still_adding =  False
        while not still_adding:
            continuing = input('Would you like to add more? [y/n]')
            if continuing.lower() == 'y':
                still_adding = True
                break
            elif continuing.lower() == 'n':
                still_adding = False
                break
            else:
                print('Input must be either \'y\' or \'n\'')
                continue
        if still_adding:
            continue
        else:
            break
    print('Returning to Main Menu...\n')

def subtractingMenu(innerHolidayList):
    still_working = True
    while still_working:
        name_input = input('Holiday Name: ')
        date_input = input('Date: ')
        innerHolidayList.removeHoliday(name_input,date_input)
        legal_input = False
        while not legal_input:
            continuing = input('Would you like to subtract more? [y/n]: ')
            if continuing.lower() == 'y':
                still_subtracting = True
                legal_input = True
                break
            elif continuing.lower() == 'n':
                still_subtracting = False
                legal_input = True
                break
            else:
                print('Input must be either \'y\' or \'n\'')
                continue 
        if still_subtracting:
            continue
        else:
            break
    print('Returning to Main Menu...\n')


def main():
    holidays_draft = HolidayList()
    try:
        holidays_draft.scrapeHolidays()
    except:
        print('There is an issue with the web scraping. The internet may be down, or the APIs may be unreachable at the moment.')
    else:    
        for dict in seed['holidays']:
            holidays_draft.innerHolidays.append(Holiday(dict['name'],format_date_object(dict['date']))) 
    
        in_sub_menu = False
        while not in_sub_menu:
            showMainMenu()
            correct_input = False
            while not correct_input:
                menu_input = input('Enter the number for the menu you wish to use: ')
                if legal_menu_inp(menu_input):
                    correct_input = True
                    break
                else:
                    print('Your input must a be a number from 1 to 5.')
                    continue
        #Menu 1
            if int(menu_input) == 1:
                showAddingMenu()
                addingMenu(holidays_draft)
                continue
        #Menu 2
            elif int(menu_input) == 2:
                showSubtractingMenu()
                subtractingMenu(holidays_draft)
                continue
        #Menu 3
            elif int(menu_input) == 3:
                dictionary = []
                for holiday in holidays_draft.innerHolidays:
                    dictionary.append({'name':holiday.print_name(),'date':holiday.print_date()})
                showSavingMenu()
                legal_input = False
                while not legal_input:
                    save_input = input('Are you sure you want to save your changes? [y/n]: ')
                    if save_input.lower() == 'y':
                        json_object = json.dumps(dictionary)
                        with open('holidays_final.json','w') as outfile:
                            outfile.write(json_object)
                        #above code block taken from geeksforgeeks.com
                        break
                    elif save_input.lower() == 'n':
                        print('Cancelled\nHoliday list file save cancelled')
                        break
                    else:
                        print('The input must be either \'y\' or \'n\'')
                        continue
                continue
        #Menu 4
            elif int(menu_input) == 4:
                still_looking = True
                while still_looking:
                    showViewingMenu()
                    legal_input = False
                    while not legal_input:
                        year_input = input('Which year?: ')
                        try:
                            int(year_input)
                        except:
                            print('The input must be a numeric year from 2020 to 2024')
                            continue
                        else:
                            if int(year_input) in [2020,2021,2022,2023,2024]:
                                legal_input = True
                            else:
                                print('The available years are 2020 through 2024')
                                continue
                    year_pool = list(filter(lambda x: x.get_date().year == int(year_input), holidays_draft.innerHolidays))
                    legal_input = False
                    while not legal_input:
                        week_input = input('Which week? [leave blank for the current week]: ')
                        if week_input.strip() == '':
                            correct_input = False
                            while not correct_input:
                                weather_input = input('Would you like to see the weather for the remaining days of this week? [y/n]: ')
                                if weather_input.lower() == 'y':
                                    see_weather = True
                                    correct_input = True
                                    break
                                elif weather_input.lower() == 'n':
                                    see_weather = False
                                    correct_input = True
                                    break
                                else:
                                    print('The input must be \'y\' or \'n\', or blank')
                                    continue
                            if see_weather:
                                show_coming_holidays_with_weather(holidays_draft.innerHolidays)
                                break
                            else:
                                this_week = list(filter(lambda x: getweeknum(x.get_date()) == getweeknum(dt.today()), year_pool))
                                for holiday in this_week:
                                    print(holiday)
                                break
                        try:
                            int(week_input)
                        except:
                            print('Please enter a number from 1 to 52, or leave the input blank to acess this week')
                            continue
                        else:
                            if int(week_input) not in range(1,53):
                                print('Please enter a number from 1 to 52, or leave the input blank to acess this week')
                                continue
                            else:
                                this_week = list(filter(lambda x: getweeknum(x.get_date()) == int(week_input), year_pool))
                                for holiday in this_week:
                                    print(holiday)
                                break
                    continue_input = input('Is there anything else you\'d like to look at? [y/n]: ')
                    legal_input = False
                    end_view = False
                    while not legal_input:
                        if continue_input.lower() == 'y':
                            end_view = False
                            legal_input = True
                            break
                        elif continue_input.lower() == 'n':
                            end_view = True
                            legal_input = True
                            break
                        else:
                            print('The input must be either \'y\' or \'n\'')
                            continue
                    if end_view:
                        break
                    else:
                        continue
                continue 
        #Menu 5           
            elif int(menu_input) == 5:
                showExitMenu()
                legal_input = False
                while not legal_input:
                    exit_input = input('[y/n] :')
                    if exit_input == 'y':
                        session_over = True
                        legal_input = True
                        break
                    elif exit_input == 'n':
                        session_over = False
                        legal_input = True
                        break
                    else:
                        print('The input must be \'y\' or \'n\'')
                        continue
                if session_over:
                    break
                else:
                    continue                
        print('Goodbye!\n')

main()