# runs VW and does forward stepwise feature selection
# expects to be run from a directory containing a VWtrain file, a VWvalid file and a VWfeatures.txt file
import os
import vw
from subprocess import call

def findFile(ending,names):
    matches = [x for x in names if x.endswith(ending)]
    if len(matches) != 1:
        raise ValueError("Directory must contain exactly one file ending with "+ending+":"+",".join(matches))
    return matches[0]

def run(featureIDs):
    name = "_".join([str(x) for x in featureIDs])
    train_data = "train"+name+".tmp"
    model = "model"+name+".tmp"
    pred = "pred"+name+".tmp"
    
    vw.featureMask(featureIDs,train,train_data) # create a training data set with the specified subset of features
    call("rm -f /tmp/vw.cache",shell=True) # clear out the cache as the train data set has changed.
    train_call = "vw -d "+train_data+" --cache_file /tmp/vw.cache -f "+model+" --passes 50 --holdout_off --loss_function logistic 2> "+outname # train the model
    test_call = "vw -t -d "+valid+" --cache_file /tmp/vw.valid.cache -i "+model+" -p "+pred+" 2> "+testout # generate the prediction
    call(train_call,shell=True) 
    call(test_call,shell=True)
    vw.sigmoid_file(pred) # take the sigmoid of the predictions
    pred = vw.read(pred)
    div = vw.divergence(pred,actual) #evaluate the performance of the model
    print name,div
    return div


files = os.listdir(".")

# read in the features file and get a list of all the ids of the features in the data set
features = findFile("features.txt",files)
features = vw.readFeatureFile(features).keys() # the possible set of features we need to try.

# get the names of the training and validation data sets
train = findFile("train",files)
valid = findFile("valid",files)

# extract the target value from the validation file
call("python ~/code/extract_target.py "+valid,shell=True)
actual = vw.read(valid+'.target')

# convert the target value in the training file to -1,1
train = vw.convertTargetToClassLabel(train,"trainc")

# first up run vw with no features.

call("rm -f /tmp/vw.valid.cache",shell=True) # clear the test cache (test data does not change during feature selection so we do this only once)
outname = "train.out"
testout = "test.out"
best_set = []
run([]) # should run with all the features
for f in [1843,1845,6639,3318]:
    run([f])



