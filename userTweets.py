import json
import os
import time
import simplekml as kml
from collections import OrderedDict


        

'''Extracts tweets with coordinates from the file with the specified name and adds the records to the input dictionary '''
def extract_journeys(users,filename):
	data = open(filename,"r")
	tweets = data.readlines()

	for t in tweets:
		t = t.strip().replace("\n","")
		if len(t) > 0:
			tweet = json.loads(t)
			coords = tweet["coordinates"]
			if coords:
				coords = coords["coordinates"]
				if coords[0] > 148:
					coords = "%.3f"%coords[0]+","+"%.3f"%coords[1]
					user = tweet["user"]["id"]
					text = tweet["text"]
					# default object is a list of texts and a list of coordinates
					prev_coords = users.get(user,[[],[]])
					prev_coords[0].append(coords)
					prev_coords[1].append(text)
					users[user] = prev_coords
		
		
	data.close()

''' writes out the journey of a user '''
def writeJourney(output,locations):
       output.write(":".join(locations)+"\n")
       


files = os.listdir("/home/finn/phd/data/tweets")
files.sort()
users = {}
files_done = 0
for fname in files:
	stats = os.stat(fname)
	now = time.time()
	since_changed = now - stats.st_mtime
	if since_changed > 600 and fname.endswith(".json"):
		extract_journeys(users,fname)
		print "done",fname
		files_done +=1
		#if files_done > 2:
		#	break


output = open("journeys.csv","w")
for user,userdata in users.iteritems():
        locations = list(OrderedDict.fromkeys(userdata[0]))
        size = len(locations)
        if size > 2:
                writeJourney(output,locations)

output.close()
                
	
	#if size > 10:
	#	for i in range(len(userdata[0])):
	#		coords =[(userdata[0][i].split(","))]
			#print userdata[1][i]
			#print coords
	#		output.newpoint(description=userdata[1][i],coords = coords)

#output.save("/home/finn/phd/data/tweets/journeys.kml")
		


