# we want a row for every day for every beat combination.
# then we want some features for those rows.

# first set of features will be dependent only on the beat
# for example, number of crimes in that beat overall
# average responce time to that beat

# second set will be dependent only on the date
# example - day of week

# third set will be dependent on the beat and the date
# example - number of crimes in that beat yesterday
# number of crimes yesterday weighted by distance - linear or quadratic


# want to work on the data that has been cleaned to some extent - so 2007 removed
# do we want to drop outliers - for example, ignore beats with fewer than 200 total crimies reported - below this looks like mis-encoded data

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

# assumes a dictionary crimeCounts that maps the ucr crime code to a count of the number of times types of that crime where seen.
def getSum(crimeCounts, lstOfCrimesOfInterest):
    total = 0
    for l in lstOfCrimesOfInterest:
        total += crimeCounts.get(l,0)
    return total

def toKey(beat,day):
    return str(beat)+":"+day.strftime(DATE_FORMAT)

def distance(lat,lon,centroid):
    try:
        return math.sqrt(pow(float(lat) - centroid[0],2)+pow(float(lon) - centroid[1],2))
    except ValueError: # what if there is no valid lat or lon at the moment return a very large number so the measurment will effectivly be ignored.
        return 10000000
    

DATE_FORMAT = '%Y-%m-%d'
LIGHT_CRIME = ['06','14','43','42','07']
TARGET_CRIME = '05'
OUTPUT_FILENAME = "features.txt" 

conn = sqlite3.connect('crime.db')
c = conn.cursor()

# create a list of days and a list of beats.
beats = c.execute('''SELECT beat,count(1) as seen from crime where rep_date < '2007-01-01' group by beat having seen > 200''')
beats = [b[0] for b in beats]
beats.sort()
print "NUMBER OF BEATS:",len(beats)

# get the centroids for beats, TODO weight by confidence
loc_query = c.execute('''SELECT beat,avg(lat),avg(lon) from crime where rep_date < '2007-01-01' and geo_conf > .8 group by beat''')
locations = {}
for loc in loc_query:
    beat = loc[0]
    lat = loc[1]
    lon = loc[2]
    locations[beat] = (lat,lon)

date_range = c.execute("SELECT min(rep_date), max(rep_date) from crime where rep_date < '2007-01-01'").fetchone()
days = listDays(dt.strptime(date_range[0],DATE_FORMAT),dt.strptime(date_range[1],DATE_FORMAT))
print "NUMBER OF DAYS:",len(days)
print "EXPECTED INSTANCES:",len(days)*len(beats)

# cache crimes by the day on which they occur
crime_by_day_query = c.execute("SELECT rep_date, substr(ucr1,1,2) as category, lat, lon from crime where rep_date < '2007-01-01'")
crime_by_day = {} # maps a day to a list of crimes
for crime in crime_by_day_query:
    day = crime[0]
    category = crime[1]
    lat = crime[2]
    lon = crime[3]
    events = crime_by_day.get(day)
    if not events:
        crime_by_day[day] = [(category,lat,lon)]
    else:
        events.append((category,lat,lon))


# cache the crime per beat per day to make it faster, beat+day -> count (later this could be beat+day -> {burglary:1,mischeif:2...})
crime_by_beat = {}
crime_counts = c.execute("SELECT beat,rep_date,substr(ucr1,1,2) as category from crime where rep_date < '2007-01-01'")

for crime in crime_counts:
    beat = crime[0]
    rep_date = crime[1]
    crime_type = crime[2]
    key = str(beat)+":"+rep_date
    counts = crime_by_beat.get(key)
    if not counts:
        counts = {crime_type:1}
        crime_by_beat[key] = counts
    else:
        type_count = counts.get(crime_type,0)
        counts[crime_type] = type_count + 1

# cache the background crime by beat
background_crime = c.execute("SELECT beat,count(1)from crime where rep_date < '2006-01-01' group by beat")
background = {}
for crime in background_crime:
    beat = crime[0]
    count = crime[1]
    background[beat] = count



o = open(OUTPUT_FILENAME,"w")
header = ["day","beat","target","day_of_week","day_of_month","background"]
header.extend(["target"+str(x) for x in range(1,8)])
header.extend(["light"+str(x) for x in range(1,8)])
header.extend(["nearby_t_linear"+str(x) for x in range(1,8)])
header.extend(["nearby_t_quad"+str(x) for x in range(1,8)])
header.extend(["nearby_l_linear"+str(x) for x in range(1,8)])
header.extend(["nearby_l_quad"+str(x) for x in range(1,8)])
o.write("\t".join(header)+"\n")
crime_free = set([])
# now we need to build a feature for each of those combinations
instances = 0
for beat in beats:
    for day_indx in range(7,len(days)):
        day = days[day_indx]
        # target variable is amount of crime of type burglary in this beat on this day
        key = toKey(beat,day)
        target = crime_by_beat.get(key)
        if not target: # no crime at all for this beat/day
            target = 0
        else: # get crime of particular type for this beat/day
            target = target.get(TARGET_CRIME,0)
 
        # features based only on day
        day_of_week = day.weekday()
        day_of_month = day.day

        
        # features based only on beat
        total_background = background.get(beat,0)
        
        # features based on both beat and day
        # crime in this beat in the last 7 days
        # for now, for each day back we will record light and target crime
        recent_target_crime = [0]*7
        recent_light_crime = [0]*7
        recent_nearby_target_linear = [0]*7
        recent_nearby_target_quad = [0]*7
        recent_nearby_light_linear = [0]*7
        recent_nearby_light_quad = [0]*7
        beat_centroid = locations[beat]
        for days_back in range(1,8):
            # in this beat
            prev_day = days[(day_indx - days_back)]
            key = toKey(beat,prev_day)
            prev_day_crime = crime_by_beat.get(key)
            if prev_day_crime:
              recent_target_crime[days_back-1] = prev_day_crime.get(TARGET_CRIME,0)
              recent_light_crime[days_back-1] = getSum(prev_day_crime,LIGHT_CRIME)

             # crime weighted by distance from beat centroid, both linear and quadratic decay.
            days_crime = crime_by_day.get(prev_day.strftime(DATE_FORMAT))
            if days_crime:
                for c in days_crime:
                    dist =  distance(c[1],c[2],beat_centroid)
                    if c[0] == TARGET_CRIME:
                        recent_nearby_target_linear[days_back-1] += 1/dist
                        recent_nearby_target_quad[days_back-1] += 1/pow(dist,2)
                    if c[0] in LIGHT_CRIME:
                        recent_nearby_light_linear[days_back-1] += 1/dist
                        recent_nearby_light_quad[days_back-1] += 1/pow(dist,2)
                        
            else:
                crime_free.add(prev_day)
                    
        
                       
        output = [day.strftime(DATE_FORMAT),beat,target,day_of_week,day_of_month,total_background]
        output.extend(recent_target_crime)
        output.extend(recent_light_crime)
        output.extend(recent_nearby_target_linear)
        output.extend(recent_nearby_target_quad)
        output.extend(recent_nearby_light_linear)
        output.extend(recent_nearby_light_quad)
        o.write("\t".join([str(x) for x in output])+"\n")
        

o.close()
conn.close()
print "no crimes on:",crime_free
