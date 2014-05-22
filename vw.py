import math
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import string
from subprocess import call

class VWLineParser:
        def __init__(self):
                self.ns_features = {}
        def namespace(self,namespace):
                self.ns = namespace
                #print namespace
                return namespace
        def feature(self,featureID,featureValue):
                #print featureID,featureValue,self.ns
                s = self.ns_features.get(self.ns,set([]))
                s.add(featureID)
                self.ns_features[self.ns] = s
                #print self.ns_features
                return (featureID,featureValue)
        def target(self,target):
                return target
        
        
        

class VWReader:        
        def __init__(self,filename):
                self.f = open(filename,"r")

        def parse(self,parser):
                while True:
                        line = self.f.readline()
                        if not line:
                                break
                        line = line.split(" ")
                        parser.target(float(line[0]))
                        for other in line[1:]:
                                if "|" in other:
                                        ns = other.strip("|").strip()
                                        parser.namespace(ns)
                                elif ":" in other:
                                        other = other.split(":")
                                        parser.feature(int(other[0]),float(other[1]))
                self.f.close()
                        
                        
                

        
                

""" Converts the target of a VW file to -1,1. Label will be 1 if target > 0, -1 otherwise. Returns the name of the output file """ 
def convertTargetToClassLabel(filename,ofilename):
        f = open(filename,"r")
        o = open(ofilename,"w")
        while True:
                line = f.readline()
                if not line:
                        break
                s = line.index("|")
                target = float(line[0:s])
                if target > 0:
                        newtarget = 1
                else:
                        newtarget = -1
                line = str(newtarget)+" "+line[s:]
                o.write(line)
        f.close()
        o.close()
        return ofilename

""" creats sample of the input file containing all the positive examples and a random sample of the negative ones. This is a pretty dodgy sample but lets have a go. """
def sample(filename,ofile):
        # find rows in which the target is > 0
        f = open(filename,"r")
        o = open(ofile,"w")
        positive = []
        line_number = 0
        while True:
                line = f.readline()
                if not line:
                        break
                s = line.index("|")
                target = float(line[0:s])
                if target > 0:
                        positive.append(line_number)
                        o.write(line)
                line_number +=1
        f.close()
        cset = range(0,line_number)
        sample = np.random.choice(cset,size=len(positive),replace=False)
        sample.sort()
        print "positive examples",len(positive),len(sample)
        print sample,len(sample)
        f = open(filename,"r")
        line_number = 0
        sample_i = 0
        while sample_i < len(sample):
                wanted_line = sample[sample_i]
                line = f.readline()
                if not line:
                        break
                if line_number == wanted_line:
                        sample_i +=1
                        o.write(line)
                line_number +=1
        o.close()
        f.close()
        
        

""" Reads in a VW file generates a new one with only the specified featureIDs
Returns the mapping from ns to featureIDs requested"""
def featureMask(featureIDs, filename, maskedfile): #TODO fix bug where there will be no bar after the target if no features are found
        result={}
        f = open(filename,"r")
        o = open(maskedfile,"w")
        while True:
                line = f.readline()
                if not line:
                        break
                line = line.split(" ")
                target = line[0]
                oline = target
                last_namespace=None # the last name space written to the output file
                for x in line:
                        if x.startswith("|"):
                                current_namespace = x[1:].replace(" ","")
                        if ":" in x:
                                key_val = x.split(":")
                                key = int(key_val[0])
                                if key in featureIDs:
                                        ns_ids = result.get(current_namespace,set([]))
                                        ns_ids.add(key)
                                        result[current_namespace] = ns_ids
                                        if last_namespace != current_namespace:
                                                oline+=" "+"|"+current_namespace
                                                last_namespace = current_namespace
                                        oline += " "+x
                if not oline.endswith("\n"):
                        oline += "\n"
                o.write(oline)
        f.close()
        o.close()
        for key,value in result.iteritems():
                result[key] = list(value)
        return result


        

""" Reads in a feature file, which contains rows of the form featureID,featureName and returns a dictionary"""
def readFeatureFile(filename):
        result = {}
        f = open(filename,"r")
        while True:
                line = f.readline()
                if not line:
                        break
                line = line.split(",")
                key = int(line[0])
                result[key] = line[1]
        f.close()
        return result

""" takes a multi-dimensional array and returns VW format
The first column is assumed to be the target and remaining columns are features."""
def toVW(mdarray,mode="regr", namespace=False):
        vw_rows = []
        for row in mdarray:
            if mode == "class":
                if row[0] > 0:
                    target = 1
                else:
                    target = -1
            elif mode == "regr":
                target = row[0]
            else:
                raise ValueError("Unknown mode:"+mode)

            features = row[1:]
            s = str(target)+" |"
            num_features = len(features)
            for i in range(num_features):
                if namespace:
                        if i > 0:
                                s+=" |"
                        s+=letters(i,num_features)
                feature_name = i + 1
                feature = features[i]
                if feature != 0:
                    s += " "+str(feature_name)+":"+str(feature)
            vw_rows.append(s)
        return vw_rows


""" Write out data to VW from a numpy array.
The first column will be treated as the target. Additional columns as features.
Takes a map from namespace to feature names."""
def writeTestData(mdarray,ns_features,ofile):
    o = open(ofile,"w")
    # create a list of featureIDs for each column
    namespaces = ns_features.keys()
    featureNames = []
    nsBoundaries = [0]
    for ns in namespaces:
        names = ns_features.get(ns)
        nsBoundaries.append(len(names)+nsBoundaries[-1])
        featureNames.extend(names)
    if len(featureNames) != mdarray.shape[1]-1:
        raise ValueError("Input array has inconsistant number of feature-columns {} with with namespace to feature-map {}".format(mdarray.shape[1]-1,len(featureNames)))
    
    for row in mdarray:
        target = row[0]
        features = row[1:]
        ns_indx=0
        boundary = nsBoundaries[ns_indx]
        s = str(target)
        
        for i in range(len(features)):
            fname = featureNames[i]
            if i == boundary:
                ns = namespaces[ns_indx]
                s +=" |{}".format(ns)
                ns_indx +=1
                boundary = nsBoundaries[ns_indx]
            feature = features[i]
            if feature != 0:
                s+= " {}:{}".format(fname,features[i])
        o.write(s+"\n")
    o.close()

""" Creates a feature mask file by running vw on dummy data """
def create_mask_file(ns_features,mask_name):
    l = sum([len(x) for x in ns_features.values()]) 
    data = np.ones((1,l+1))
    train_filename = "train_mask_data"
    writeTestData(data,ns_features,train_filename)
    traincall = "vw -d {} -f {} --loss_function logistic --readable_model {} 2> {}".format(train_filename,mask_name,mask_name+"read","tmpout2")
    #print traincall
    call(traincall,shell=True)
    call("rm -f {} {}".format(train_filename,"tmpout"),shell=True)

""" Converts any number to a unique character sequence. Effectively base 26 with each letter opperating as a number """
def letters(number,maxnumber):
        digits = int(math.ceil(math.log(maxnumber+1,26)))
        k = number
        letters = ""
        for d in range(digits,0,-1):
                indx,k = divmod(k,pow(26,d-1))
                letter = string.ascii_lowercase[indx]
                letters+=letter
        return letters
        
        
        

def saveToVW(filename,mdarray,mode="regr",namespace=False):
        lines = toVW(mdarray,mode,namespace)
        f = open(filename,"w")
        for line in lines:
                f.write(line+"\n")
        f.close()
        
    
    

def read(f):
    targets = open(f,"r")
    result = []
    while (True):
        line = targets.readline()
        if not line:
            break
        p = float(line)
        result.append(p)
    targets.close()
    return result

""" Applies the sigmoid function to all the entries in the specified file"""
def sigmoid_file(fname,oname):
        f = open(fname,"r")
        tmp = open(oname,"w")
        for line in f.readlines():
                y = 1.0/(1+np.exp(-1.0*float(line)))
                if y >= 1 or y <= 0:
                        raise ValueError("Y cannot be outside the range (0,1) but is {}".format(y))
                tmp.write(str(y)+"\n")
        f.close()
        tmp.close()

def sigmoid(pred):
        a = np.array(pred)
        return 1.0/(1+np.exp(-a))

def neg_log_sigmoid(fname,oname):
        f = open(fname,"r")
        o = open(oname,"w")
        while True:
                line = f.readline()
                if not line:
                        break
                y = log(1.0+np.exp(-1.0*float(line)))
                o.write(str(y)+"\n")
        f.close()
        o.close()
                
        

def binomial_file(fname,oname):
        f = open(fname,"r")
        o = open(oname,"w")
        for line in f.readlines():
                risk = float(line)
                if risk > 0.5:
                        o.write("1\n")
                else:
                        o.write("-1\n")
        o.close()
        f.close()


class PAIGroup():
    def __init__(self,group):
        self.num_areas = int(group[-1])
        self.actual = group[-2]
        self.pred = group[0:-2]

    def __str__(self):
        return "Actual:"+self.actual+" Pred:"+str(self.pred)+" areas:"+str(self.num_areas)

def parsePAI():
    params = " ".join(sys.argv[1:]).split("]")
    pai_groups = []
    for p in params:
        g = p.replace("[","").replace(" ","")
        if len(g) > 0:
            g = g.split(",")
            if len(g) < 3:
                raise ValueError("Unexpected number of inputs:"+str(len(g))+","+str(g))
            pai_groups.append(PAIGroup(g))
    return pai_groups


# generates a baseline prediction, with a prediction for each day/area that is equal to the average number of events in that area over the training set
def write_baseline(train_actual,num_areas,pred_length,filename):
        # input in train actual is assumed to be target for {(a1...a_num_areas)period1; (a1...a_num_areas)period2 ... numPeriods}
        num_times = len(train_actual)/num_areas
        total = np.array([0]*num_areas)
        for period in range(num_times):
                a = period*num_areas
                b = a+num_areas
                train_slice = np.array(train_actual[a:b])
                total = total+train_slice
        total = total/float(num_times)
        # total is now the total for each area
        num_pred_times = pred_length/num_areas
        o = open(filename,"w")
        for p in range(num_pred_times):
                for area in total:
                        o.write(str(area)+"\n")
        o.close()
                             

def pai(pred,actual,num_areas):
    # return a list of the average cumsum of the actual crime, ordered by the predicted area
    # "                the standard error of the above
    if len(pred) != len(actual):
        raise ValueError("Predicted and Actual lengths are not equal:"+str(len(pred))+"!="+str(len(actual)))
    num_times = len(pred)/num_areas
    print "Areas:{}, Times:{}".format(num_areas,num_times)
    # create an empty numpy array
    result = np.zeros((num_times,num_areas+1))
    for ts in range(num_times):
        a = ts * num_areas
        b = a + num_areas
        z = zip(pred[a:b],actual[a:b])
        z.sort(key = lambda x: x[0], reverse=True) # sort by pred, largest to smallest
        cum = np.cumsum([x[1] for x in z])
        result[ts,1:] = cum
    return result

def meanPaiArea(pred,actual,num_areas):
    pais = pai(pred,actual,num_areas)
    m = np.mean(pais,axis=0)
    m = m/max(m[-1],1)
    a = area(m)
    return a
        
    
        
def area(y):
    return sum(y)/float(len(y))
    

def roc(pred, actual):
    paired = zip(pred,actual)
    paired.sort(key = lambda x: x[0],reverse=True)
    result = [p[1] for p in paired]
    c = np.cumsum(result)
    total = float(c[-1])
    normalized = [i/total for i in c]
    return area(normalized)

# returns an indication of the classification error. Pred is assumed to be a probability of counts > 1. Actual is number of counts
def class_err(pred,actual):
        if len(pred) != len(actual):
                raise ValueError("Predicted and actual lengths differ:"+str(len(pred))+" vs "+str(len(actual)))
        correct = 0
        for i in range(len(pred)):
                pclass1 = pred[i] > 0.5
                aclass1 = actual[i] > 0
                if pclass1 == aclass1:
                        correct +=1
        return 1 - float(correct)/len(pred)

# returns an the divergence measure of classification error. Pred is assumed to be a probability of counts > 1. Actual is number of counts
def divergence(pred,actual):
        if len(pred) != len(actual):
                raise ValueError("Predicted and actual lengths differ:"+str(len(pred))+" vs "+str(len(actual)))
        divergence = 0
        for i in range(len(pred)):
                if actual[i] > 0:
                        divergence += -2*math.log(pred[i])
                else:
                        divergence += -2*math.log(1-pred[i])
        return divergence/float(len(pred))

""" Assumes the predictions are the linear combinations of the explanitory variables """
def divergence2(pred,actual):
        if len(pred) != len(actual):
                raise ValueError("Predicted and actual lengths differ:"+str(len(pred))+" vs "+str(len(actual)))
        divergence = 0
        for i in range(len(pred)):
                t = pred[i]
                lterm = math.log(1+math.exp(-t))
                if actual[i] > 0:
                        divergence += 2*lterm
                else:
                        divergence += 2*(t+lterm)
        return divergence/float(len(pred))

def divergence3(pred,actual):
        if len(pred) != len(actual):
                raise ValueError("Predicted and actual lengths differ:"+str(len(pred))+" vs "+str(len(actual)))
        divergence = 0
        for i in range(len(pred)):
                t = pred[i]
                s = 1.0/(1+math.exp(-t))
                if actual[i] > 0:
                        divergence += -2*math.log(s)
                else:
                        divergence += -2*math.log(1-s)
        return divergence/float(len(pred))
        
        

def rmse(pred, actual):
    if len(pred) != len(actual):
                raise ValueError("Predicted and actual lengths differ:"+str(len(pred))+" vs "+str(len(actual)))
    total = 0
    for i in range(len(pred)):
        diff = pow(pred[i]-actual[i],2)
        total += diff
    mse = total/len(pred)
    return math.sqrt(mse)

# excpects a data frame with each row containing information on the performance of a vw model.
# columns 3-6 are assumed to be train-rmse, train-pai, test-rmse, test-pai
def plot_regularization(subset,xlabel,xcol,title):
    x = subset[:,xcol]
    figure, ax_array = plt.subplots(2,sharex=True)
    ax_array[0].semilogx(x,(subset[:,3]),label="train")
    ax_array[0].semilogx(x,(subset[:,5]),label="test")
    ax_array[1].semilogx(x,1-subset[:,4],label="train")
    ax_array[1].semilogx(x,1-subset[:,6],label="test")
    ax_array[0].set_ylabel("rmse")
    ax_array[1].set_ylabel("1 - area-under-pai")
    ax_array[0].set_title(title)
    ax_array[1].set_xlabel(xlabel)
    ax_array[0].legend(loc=2, borderaxespad=0.)
    plt.savefig(title+".png")
    plt.show()






    
    
