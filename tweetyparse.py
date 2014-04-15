from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time

# Go to http://dev.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key = "3iOzO5TBSkUqT4M3JxlyQ"
consumer_secret = "DELUvDmjemX9UfR8SjoWs1faHm1pvlwjGpVcf7iw"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token = "1401999284-h6s8RHFqDZZDWRVpv9uPJ79FR6fCn9QtJOJLKrG"
access_token_secret = "WPGsF76j2LCmdsPTyGF1PMTGG9vtNfH7EyMpmE7t8Y"

TWEETS_PER_FILE = 10000
DATA_DIRECTORY = "/home/finn/phd/data/tweets/"
locs=[150.66,-34.13,151.34,-33.63,-97.18,32.49,-96.36,33.27] # should be Sydney & Dallas

class SimpleListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that outputs tweets to a file.
    Once a file contains a certain number of tweets, a new ones is started.
    """
    def __init__(self):
        super(SimpleListener,self).__init__()
        self.output = open(DATA_DIRECTORY+time.strftime('%Y%m%d%H%M%S')+".json","w")
        self.count = 0

    def on_data(self, data):
        self.count +=1
        if self.count > TWEETS_PER_FILE:
            self.new_output()
        self.output.write(data+"\n")
        return True

    def on_error(self, status):
        print status

    def new_output(self):
        self.output.close()
        self.output = open(DATA_DIRECTORY+time.strftime('%Y%m%d%H%M%S')+".json","w")
        self.count = 0

if __name__ == '__main__':
    l = SimpleListener()
    print "done"
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(locations=locs)
