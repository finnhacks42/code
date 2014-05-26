from subprocess import call
import sys
import os
import vw


directory = sys.argv[1]
files = os.listdir(directory)

train = directory+"/"+vw.findFile("train",files)
valid = directory+"/"+vw.findFile("valid",files)

num_areas = int(input("How many areas:? "))
featureID = int(input("Baseline feature id? "))

ns_features = vw.extract_ns_features(train)
ns_baseline = vw.ns_features_for_featureID(ns_features,featureID)


# baseline ... # Create a fake data set with the same namespaces and featureID, train a model ... and we are done.
vw.create_linear_model_file(ns_baseline,"baseline_model")


# convert the training data to binary
TRAIN_FILE  = vw.convertTargetToClassLabel(train,"train_data_logistic")


print "CLEARING CACHE"
call("rm -f /tmp/*",shell=True)

train_call = "vw --loss_function logistic --passes 50 --cache_file /tmp/vw_train -f model --readable_model model.read --holdout_off -d {} ".format(TRAIN_FILE)
test_call = "vw -t --cache_file /tmp/vw.valid -i model -p pred -d {}".format(valid)
baseline_call = "vw -t --cache_file /tmp/vw.valid -i baseline_model -p baseline_pred -d {}".format(valid)

call(train_call,shell=True)
call(test_call,shell=True)
call(baseline_call,shell=True)

spred = vw.sigmoid_file("pred","s_pred")
call("python ~/code/pai.py [s_pred, baseline_pred, {}, {}]".format(valid+".target",num_areas),shell=True)


