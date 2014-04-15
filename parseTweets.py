import urllib
import json

data = open("/home/finn/phd/data/tweets/20140415142553.json","r")

tweets = data.readlines()
print len(tweets)
for t in tweets:
        t = t.strip().replace("\n","")
        if len(t) > 0:
                try:
                        tweet = json.loads(t)
                       # print tweet["coordinates"]
                        print tweet["place"]["full_name"]
                        
                        
                except:
                        pass
                        

data.close()
