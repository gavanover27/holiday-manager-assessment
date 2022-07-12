# Notes to Self
        # Need to add if then statement to addmenu to check for datetime datatype
        # Same thing for removeMenu
        # Remove isn't working properly
        # In the addHoliday() need to add if then to ensure there are no duplicates
import datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
from config import holidayloc
from config import currentYear
from config import saveloc

# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
@dataclass
class Holiday:
    name: str
    date: datetime
    #def __init__(self, name, date):
        #self._name = name
        #self._date = date
    
    def __str__ (self):
        return (f'{self.name} ({self.date})')
        #return ('%s (%s)' %(self._name, self._date))
    
    #@property
    #def name(self):
        #return self._name
    
    #@property
    #def date(self):
        #return self._date

    #@name.setter
    #def name(self, new_name):
        #self._name = new_name
    
    #@date.setter
    #def date(self, new_date):
        #self._date = new_date
           
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
@dataclass
class HolidayList:
    innerHolidays: list

    def addHoliday(self, holidayObj):
        # Make sure holidayObj is an Holiday Object by checking the type
        if type(holidayObj) == Holiday:
            alreadyInTheList = self.findHoliday(holidayObj.name, holidayObj.date)
            if alreadyInTheList == 'not found':
        # Use innerHolidays.append(holidayObj) to add holiday
                self.innerHolidays.append(holidayObj)
        # print to the user that you added a holiday
                print(f'Success:\n{holidayObj} has been added to the holiday list!')
            else:
                print(f"Error:\n{holidayObj.name} can't be added because it's already in the system.")
        else:
            print('Sorry that does not work.')
    
    def findHoliday(self, HolidayName, Date):
        # Find Holiday in innerHolidays
        for holiday in self.innerHolidays:
        # Return Holiday
            if holiday.name == HolidayName and holiday.date == Date:
                return holiday
            else:
                inTheList = 'not found'
                return inTheList

    def removeHoliday(self, HolidayName, Date):
        # Find Holiday in innerHolidays by searching the name and date combination.
        holiday = self.findHoliday(HolidayName, Date)
        # remove the Holiday from innerHolidays
        if holiday == 'not found':
            print("That holiday can't be removed because it was never added.")
        else:
            self.innerHolidays.remove(holiday)
        # inform user you deleted the holiday
            print(f'Success:\n{HolidayName} has been removed from the holiday list.')

    def read_json(self, filelocation):
        # Read in things from json file location
        with open(filelocation, 'r') as jsonfile:
            holiData = json.load(jsonfile)['holidays']
            for i in range(len(holiData)):
                name = holiData[i]['name']
                date = holiData[i]['date']
                properDate = datetime.datetime.strptime(date, '%Y-%m-%d')
        # Use addHoliday function to add holidays to inner list.
                holidayFromJSON = Holiday(name, properDate)
                self.innerHolidays.append(holidayFromJSON)

    def save_to_json(self, filelocation):
        # list_dict_holidays = [holidayobject.__dict__ for holidayobject in self.innerHolidays]
        holiday_dict = {}
        list_dict_holidays = []
        for holiday in self.innerHolidays:
            date_str = datetime.datetime.strftime(holiday.date, '%Y-%m-%d')
            holiday_dict = {'name': holiday.name, 'date': date_str}
            list_dict_holidays.append(holiday_dict)
        # Write out json file to selected file.
        with open(saveloc,'w') as JSONfile:
            json.dump(list_dict_holidays, JSONfile, indent = 2)
        
    def scrapeHolidays(self):
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. 
        #For example https://www.timeanddate.com/holidays/us/2022?hol=33554809
        for i in range(currentYear-2, currentYear+3):
            url = ("https://www.timeanddate.com/holidays/us/{}?hol=33554809")
            url = url.format(i)

            def getHTML(url):
                response = requests.get(url, verify=False)
                return response.text
                
            html = getHTML(url)
                        
            soup = BeautifulSoup(html,'html.parser')

            table = soup.find('table', attrs = {'class': 'table table--left table--inner-borders-rows table--full-width table--sticky table--holidaycountry'})
            for row in table.find_all('tr', class_ = 'showrow'):
                name = row.find_all('td')[1].text
                date =  row.find('th', attrs = {'class':'nw'}).text
                fullDate = f'{i} {date}'
                properDate = datetime.datetime.strptime(fullDate, '%Y %b %d')
                dateObject = Holiday(name, properDate)
                self.addHoliday(dateObject)

        # Check to see if name and date of holiday is in innerHolidays array
        # Add non-duplicates to innerHolidays
        # Handle any exceptions.     

    def numHolidays(self):
        # Return the total number of holidays in innerHolidays
        numOfHolidays = len(self.innerHolidays)
        return numOfHolidays
    
    def filter_holidays_by_week(self, year, week_number):
        holidays = []
        #if(not(isinstance(week_number, int))):
            #raise ValueError()
        #if(not(isinstance(year, int))):
            #raise ValueError()
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        holidays = list(filter(lambda holiday: holiday.date.isocalendar()[0] == year and holiday.date.isocalendar()[1] == week_number, self.innerHolidays))
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays
        return holidays

    def displayHolidaysInWeek(self, holidayList):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        if holidayList != []:
            for holiday in holidayList:
                print(holiday)
        else:
            print('There are no holidays during that week.')
        # * Remember to use the holiday __str__ method.

    #def getWeather(weekNum):
        # Convert weekNum to range between two days
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information and return weather string.

    def viewCurrentWeek():
        # Use the Datetime Module to look up current week and year
        today = datetime.datetime.today()
        currentWeekNumber = today.isocalendar()[1]
        currentYear = today.isocalendar()[1]
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results

# Create functions for each page of the menu
def addMenu():
    print("Add a Holiday\n============")
    name = input('Holiday: ')
    date = input('Date (YYYY-MM-YY): ')
    # betterDate = datetime.datetime.strptime(date, '%Y-%m-%d')
    #year, month, day = date.split('-')
    isValidDate = True
    try:
        holiDate = datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        isValidDate = False
    if(isValidDate):
        holidayobj = Holiday(name, holiDate)
        return holidayobj
    else:
        print('Error:\nThat is not a valid date.')

def removeMenu():
    print("Remove a Holiday\n================")
    name = input('Holiday: ')
    date = input('Date (YYYY-MM-YY): ')
    #betterDate = datetime.datetime.strptime(date, '%Y-%m-%d')
    #year, month, day = date.split('-')
    isValidDate = True
    try:
        holiDate = datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        isValidDate = False
    if(isValidDate):
        return name, holiDate
    else:
        print('Error:\nThat is not a valid date.')

def savemenu():
    print('Saving Holiday List\n===============')
    willYouSave = input('Are you sure you want to save your changes? [y/n]: ').lower()
    if willYouSave == 'n':
        print('Cancelled:\nHoliday list file save cancelled.')
    if willYouSave == 'y':
        print('Success:\nYour changes have been saved.')
    else:
        print('Invalid choice.')
    return willYouSave

def viewmenu():
    print('View Holidays')
    wrong_input = True
    while(wrong_input):
        try:
            year = int(input('Which year?: '))
            week = (input('Which week? #[1-52, Leave blank for the current week]: '))

            if week != "":
                if(int(week)<= 52 and int(week)>=1):
                    wrong_input = False
                    week = int(week)
                else: print('Input outside of expected ranges, please try again.')
            elif week == '':
                week = datetime.now().isocalendar()[1]
                print(week)
                wrong_input = False
            return year, week
        except:
            print("Input an integer, not a string.")

def exitmenu():
    print('Exit\n=====')
    exitChoice = input('Are you sure you want to exit? [y/n]: ').lower()
    if exitChoice == 'y':
        print('Goodbye!')
        return exitChoice
    elif exitChoice not in ['y', 'n']:
        print('That is not a valid choice!')
    else:
        return exitChoice

def main():
    global hlist
    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    hlist = HolidayList([])
    # 2. Load JSON file via HolidayList read_json function
    hlist.read_json(holidayloc)
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    hlist.scrapeHolidays()
    # 4. Create while loop for user to keep adding or working with the Calender
    print(f'Holiday Management\nThere are {hlist.numHolidays()} holidays stored in the system')
    keepWorking = True
    while keepWorking:
    # 5. Display User Menu (Print the menu)
        print(f'Holiday Menu\n===========\n1. Add a Holiday\n2. Remove a Holiday\n3. Save Holiday list\n4. View Holidays\n5. Exit')
        # 6. Take user input for their action based on Menu and check the user input for errors
        choice = input('Choose an option: ')
        if choice == '1':
            newholidayobj = addMenu()
            hlist.addHoliday(newholidayobj)
        if choice == '2':
            name, date = removeMenu()
            hlist.removeHoliday(name, date)
        elif choice == '3':
            saveChoice = savemenu()
            if saveChoice == 'y':
                hlist.save_to_json(holidayloc)
        elif choice == '4':
            year, week = viewmenu()
            holidaysInWeek = hlist.filter_holidays_by_week(year, week)
            hlist.displayHolidaysInWeek(holidaysInWeek)
        elif choice == '5':
            shallWeExit = exitmenu()
            if shallWeExit == 'y':
                keepWorking = False
        else:
            print('Not a valid choice.')
    # 7. Run appropriate method from the HolidayList object depending on what the user input is
    # 8. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 

if __name__ == "__main__":
    main()


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.





