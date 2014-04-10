# this script looks a how the average numbers of crime changes as you go forward from a given crime

# we start with our sqlite3 db.

import sqlite3
from datetime import date
from datetime import timedelta
from datetime import datetime as dt
import math

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

DATE_FORMAT = '%Y-%m-%d'
LIGHT_CRIME = ['14','24','16','13','43']
DAYS_FORWARD= 730


conn = sqlite3.connect('crime.db')
c = conn.cursor()
# lets just look at reporting area 4043



# query the database and save results into a dictionary keyed by date and reporting area
events = {}
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
        
print "Completed database query"


def calculate_given_freq(area, crime_dates, days_forward, min_date,max_date):
    last_date = max_date - timedelta(days = days_forward)
    ndays = (last_date - min_date).days
    
    crime_days = 0 # records on how many days a crime occured upto last_date, where last_date is the last date in the dataset - days_forward days
    crime_counts = 0 # records the actual number of crimes upto last_date
    next_days = [0]*days_forward
    for date in crime_dates:
        if date < last_date:
            crime_days +=1
            key = makeKey(date,area)
            crime_counts += events[key]
            for day in range(1,days_forward+1):
                lookupdate = date+timedelta(days = day) # go day days forward from the day on which the crime occured
                lookupkey = makeKey(lookupdate,area)
                count = events.get(lookupkey,0)
                next_days[day - 1] += count
    #print "ndays",ndays,"crime_days",crime_days,"crime counts",crime_counts
    #print next_days
    if crime_days > 0:
        next_days = [x/float(crime_days) for x in next_days]
    #print next_days
    background = crime_counts/float(ndays)
    next_days = [x - background for x in next_days]
    #print next_days
    return next_days

results = {}
for area,dates in area_to_date.iteritems():
    nextdays = calculate_given_freq(area,dates,DAYS_FORWARD,min_date,max_date)
    results[area] = nextdays

totals = [0]*DAYS_FORWARD
for nextdays in results.values():
    for i in range(len(totals)):
        totals[i] += nextdays[i]

totals = [x/len(results.values()) for x in totals]

print totals
            

    

# for each reporting area, find all the days on which a crime of desired category occured (up to D days from end)

# reporting area -> list day1,day2,...



conn.close()
print "DONE"
