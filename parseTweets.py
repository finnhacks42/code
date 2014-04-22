import urllib
import json
import simplekml as kml

data = open("/home/finn/phd/data/tweets/20140416082242.json","r")

output = kml.Kml()

i = 0
tweets = data.readlines()
#print len(tweets)
for t in tweets:
        t = t.strip().replace("\n","")
        if len(t) > 0:
                tweet = json.loads(t)
                coords = tweet["coordinates"]
                if coords:
                        coords = coords["coordinates"]
                        text = tweet["text"]#tweet["place"]["full_name"]
                        output.newpoint(name=text,coords = [coords])
                        #pm = kml.Placemark(kml.name(text),kml.Point(kml.coordinates(coords[1],coords[0])))
                        #i += 1
                        if i > 10:
                                break
              
                        

data.close()
output.save("tweet_locs.kml")
