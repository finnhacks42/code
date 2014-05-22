# creates a vw model that is a mask containing only the desired features
import vw
import numpy as np
from subprocess import call
       
# write out a training file with only the desired features, do linear regression.
# I suspect I require only that the weights are not 0.
ns_features = {"crimea1":[1845]}

def create_mask_file(ns_features,mask_name):
    l = sum([len(x) for x in ns_features.values()]) 
    data = np.ones((1,l+1))
    vw.writeTestData(data,ns_features,"train_tmp")
    call("vw -d train_tmp -f "+mask_name+" 2> tmp",shell=True)
    call("rm -f train_tmp tmp",shell=True)
    
    
            
create_mask_file(ns_features,"mask.mod")




# run vw to create a model file

