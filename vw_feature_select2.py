# runs VW and does forward stepwise feature selection
# expects to be run from a directory containing a VWtrain file, a VWvalid file and a VWfeatures.txt file
import os
import vw
from subprocess import call
import copy

def findFile(ending,names):
    matches = [x for x in names if x.endswith(ending)]
    if len(matches) != 1:
        raise ValueError("Directory must contain exactly one file ending with "+ending+":"+",".join(matches))
    return matches[0]

""" Run VW with a given set of features, and name to apply to the models, etc"""
def run(ns_features,name):
    model = "model{}".format(name)
    pred = "pred{}".format(name)
    mask = "mask{}".format(name)
 
    
    vw.create_mask_file(ns_features,mask)
    #vw.featureMask(featureIDs,train,train_data) # create a training data set with the specified subset of features

    train_call = "vw --loss_function logistic --holdout_off --passes 10 --cache_file {} --feature_mask {} -f {} --readable_model {} -d {} 2> {}".format(TRAIN_CACHE,mask,model,model+"read",TRAIN_FILE,outname)
    print train_call
    test_call = "vw -t --cache_file {} -i {} -p {} -d {} 2> {}".format(TEST_CACHE,model,pred,TEST_FILE,testout)
    
   # train_call = "vw -d "+train_data+" --cache_file /tmp/vw.cache -f "+model+" --passes 50 --holdout_off --loss_function logistic 2> "+outname # train the model
   # test_call = "vw -t -d "+valid+" --cache_file /tmp/vw.valid.cache -i "+model+" -p "+pred+" 2> "+testout # generate the prediction
    call(train_call,shell=True)
    print test_call
    call(test_call,shell=True)
   
    #vw.sigmoid_file(pred,) # take the sigmoid of the predictions
    #print "REAIDING IN PREDICTIONS"
    pred = vw.read(pred)
    #print "CALCULATING DIVERGENCE"
    div = vw.divergence2(pred,ACTUAL) #evaluate the performance of the model
    #print "CALCULATING PAI"
    pred = vw.sigmoid(pred)
    area = vw.meanPaiArea(pred,ACTUAL,1011) #WARNING NUMBER OF AREAS IS HARDCODED...WARNING
    print ns_features,div,area
    SUMMARY_FILE.write("{},{},{},{}\n".format(":".join([str(x) for x in ns_features]),name,div,area))
    return area

def addTo(subset,f):
    result = copy.deepcopy(subset)
    # if its already added skip
    key = f.keys()[0]
    value = f[key][0]
    s = result.get(key,[])
    if value in s:
        return False
    s.append(value)
    result[key] = s
    return result                                                                                                                        
                                                                                                                             
TRAIN_CACHE = "/tmp/vw.cache"
TEST_CACHE = "/tmp/vw.valid.cache"
SUMMARY_FILE = open("summary","w")
  
files = os.listdir(".")

# get the names of the training and validation data sets
train = findFile("train",files)
TEST_FILE = findFile("valid",files)

# read in the features file and get a list of all the ids of the features in the data set
#features = findFile("features.txt",files)
#features = vw.readFeatureFile(features).keys() # the possible set of features we need to try. Doesn't work at the momment as namespace not there
reader = vw.VWReader(train)
parser = vw.VWLineParser()
reader.parse(parser)

features = []
for key,values in parser.ns_features.iteritems():
    # separate entry for each feature
    for feature in values:
        features.append({key:[feature]})

        

# extract the target value from the validation file
call("python ~/code/extract_target.py "+TEST_FILE,shell=True)
ACTUAL = vw.read(TEST_FILE+'.target')

# convert the target value in the training file to -1,1
TRAIN_FILE  = vw.convertTargetToClassLabel(train,"VW1kcltrain")

# first up run vw with no features.

#TODO debug why this stops after 2 loops ...

call("rm -f {}".format(TEST_CACHE),shell=True) # clear the test cache (test data does not change during feature selection so we do this only once)
call("rm -f {}".format(TRAIN_CACHE),shell=True) # clear out the cache as the (train data does not change, only feature mask)

outname = "train.out"
testout = "test.out"


    
#run([]) # should run with all the features
max_area = 0
subset = {} # the set of the best variables so far
indx = 1
variable_count = 1
while True:
    best = 0 # the best area with the current number of variables
    bestf = None # the best feature to add to the current subset
    for f in features:
        #add f to the existing combination
        combined = addTo(subset,f)
        if combined: # return false only if feature is already in subset
            area = run(combined,indx)
            if area > best:
                best = area
                bestf = f
            indx +=1
    print "Best Result with {} variables. Features {} plus {}, area {}. Best area any num vars {}".format(variable_count,subset,bestf,best,max_area)
    if best <= max_area:
        break
    max_area = best
    subset = addTo(subset,bestf)
    
    # bestf is the best feature so far
    
#run({"crimea1":[1845]},1)
SUMMARY_FILE.close()
