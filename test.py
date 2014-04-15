

class Test():
    def __init__(self):
        self.count = 1
    def hello(self):
        print self.count
        self.inc()

    def inc(self):
        self.count +=1

t = Test()
