# this script looks a how the average numbers of crime changes as you go forward from a given crime

# we start with our sqlite3 db.

import sqlite3
from datetime import date
from datetime import timedelta
from datetime import datetime as dt
import math
import bisect

# returns a list of all the days between start and end inclusive
def listDays(start,end):
    delta = end - start
    result = [0]*(delta.days + 1)
    for i in range(delta.days + 1):
        day = start + timedelta(days = i)
        result[i] = day
    return result

def makeKey(date,area):
    return str(date)+"|"+str(area)   

def calc_frequency(area,all_dates): #all_dates must be a sorted list, from frist to last, of all the dates to consider (without gaps)
    total_crime = 0
    crime_days = area_to_date[area] # a sorted list of the days on which crime did occur
    by_days_since = {} # maps from number of days since last crime to a list of the numbers of crimes
    
    days_counted = 0
    
    for date in all_dates:
        last_crime_indx = bisect.bisect_left(crime_days,date) - 1
        # I want to find the day previous to this date in the list. If this day is in the list then 0.
        if last_crime_indx >= 0: # if this is not the first day on which crime occured in this area
            key = makeKey(date,area)
            crime_count = events.get(key,0) # number of crimes occuring on that day
            #if crime_count > 0: # such that we are calculating the frequency with which at some crime occurs on day D given some at D - d
            #    crime_count = 1 
            total_crime += crime_count
            days_counted += 1
            last_date = crime_days[last_crime_indx]
            days_since = (date - last_date).days
            tmp = by_days_since.get(days_since,[])
            tmp.append(crime_count)
            by_days_since[days_since] = tmp
            
           
            
    background = total_crime/float(days_counted) #average number of crimes per day in this area
   
    # returns a count of the number of crimes by days_since, a count of the number of days by days since and the average number of crimes per day in this area
    return [by_days_since,background] 

DATE_FORMAT = '%Y-%m-%d'
LIGHT_CRIME = ['43']#['08','01','02','03','04']#['05']#['14','24','16','13','43']



conn = sqlite3.connect('crime.db')
c = conn.cursor()
# lets just look at reporting area 4043



# query the database and save results into a dictionary keyed by date and reporting area
events = {} # maps date-area to the number of events within the category LIGHT_CRIME that occured on that day and in that area.
area_to_date = {} # maps reporting areas to a list of dates on which crimes occured
max_date = dt.strptime('1970-01-01',DATE_FORMAT)
min_date = dt.strptime('2050-01-01',DATE_FORMAT)
query = c.execute("SELECT rep_date,substr(ucr1,1,2) as category, reportingarea, count(1) as total FROM crime where rep_date < '2008-01-01' and rep_date > '2000-01-01' group by rep_date,category,reportingarea")
for result in query:
    date = dt.strptime(result[0],DATE_FORMAT)
    category = result[1]
    area = result[2]
    count = result[3]
    if category in LIGHT_CRIME:
        key = makeKey(date,area)
        crimes = events.get(key,0)
        events[key] = crimes + count
        dates = area_to_date.get(area,[])
        dates.append(date)
        area_to_date[area] = dates
        if date > max_date:
            max_date = date
        if date < min_date:
            min_date = date
for datelist in area_to_date.values():
    datelist.sort()

#"Completed database query"
all_dates = listDays(min_date,max_date)

results = {}
head = ["reportingarea","days_since","num_crimes","background"]
print "\t".join(head)
for area in area_to_date:
    freqs = calc_frequency(area,all_dates)
    background = freqs[1]
    if background > 0:
        for days_since, crimes_lst in freqs[0].iteritems():
            for num_crimes in crimes_lst:
                output = [area,days_since,num_crimes,background]
                output = [str(x) for x in output]
                print "\t".join(output)
            
            


    
            
                    







conn.close()

