#vw -k -l .5 --l2 0 -d ctrain --cache_file /tmp/vw.cache  -f model1 --invert_hash model1.read  --passes 100
# run vw for a range of different l1 and l2 values - saving all outputs. Then I can write the code to evaluate the results later ...

from optparse import OptionParser
from subprocess import call
import vw
import os
from time import strftime
import numpy as np



def run(train,test,l1,l2,run,mode,mode_name,name):   
    model_name = name+mode_name+str(run)+".mod"
    pred_name = name+mode_name+str(run)+".pred"
    outname = name+mode_name+str(run)+".out"
    testout = name+mode_name+str(run)+".tout"
    train_pred = name+"train_pred"
    trainout = name+"train_test.out"
    train_call = "vw -l .5 --l2 "+str(l2)+" --l1 "+str(l1)+" -d "+train+" --cache_file /tmp/vw.cache -f "+model_name+" --passes 50 --holdout_off "+mode+" 2> "+outname
    train_pred_call = "vw -t -d "+train+" --cache_file /tmp/vw.cache -i "+model_name+" -p "+train_pred +" 2>"+trainout
    test_call = "vw -t -d "+test+" --cache_file /tmp/vw.valid.cache -i "+model_name+" -p "+pred_name+" 2> "+testout 
   
    call(train_call,shell=True)
    print train_call
    call(train_pred_call,shell=True)
    print train_pred_call
    call(test_call,shell=True)
    print test_call
    p_train = vw.read(train_pred)
    p_test = vw.read(pred_name)
   
    rmse_train = vw.rmse(p_train,actual_train)
    pai_train = vw.meanPaiArea(p_train,actual_train,num_areas)
    rmse_test = vw.rmse(p_test,actual_test)
    pai_test = vw.meanPaiArea(p_test,actual_test,num_areas)
    return [rmse_train,pai_train,rmse_test,pai_test]
    
    
    

parser = OptionParser()
parser.add_option("-m","--mode",dest = "mode",help="mode arguament to vw ie '-q a:'")
parser.add_option("-t","--test",action="store_true",dest = "test",help="run only for a single value for l1 and l2 - useful for testing")
parser.set_defaults(test=False,mode="")
(options,args) = parser.parse_args()
print options,type(options)
print args


train = args[0]
test = args[1]
num_areas = int(args[2])
mode = options.mode
is_test = options.test

if is_test:
    l1_list = [0]
    l2_list = [0]
else:
    l1_list = [0,0.0000000000001,.000000001,.00000001,.0000001,.000001,.00001,.0001]
    l2_list = [0,0.0000000000001,.00000001,.0000001,.000001,.00001,.0001,.001]

# read in the actual_train and actual_test
actual_train = vw.read(train+".target")
actual_test = vw.read(test+".target")
    
mode_name = mode.replace(" ","").replace("-","").replace(":","")

name = train.replace("train","")
datetime = strftime("%Y%m%d%H%M")
directory = name+datetime
os.mkdir(directory)
name = directory+"/"+name
output_name = name+mode_name+".result"
o = open(output_name,"w")
i = 1
prep_call = "rm -f /tmp/vw.cache"
prep_call2 = "rm -f /tmp/vw.valid.cache"
call(prep_call,shell=True)
call(prep_call2,shell=True)
for l1 in l1_list:
    for l2 in l2_list:
        result = run(train,test,l1,l2,i,mode,mode_name,name)
        
        result = [str(x) for x in result]
        o.write(str(i)+","+str(l1)+","+str(l2)+","+",".join(result)+"\n")
        i +=1
o.close()
# plot the rmse and pai curves for the training and the test set as a function of l1 and l2
result = open(output_name,"r")
lines = result.readlines()
data = np.zeros((len(lines),7))
row = 0
for line in lines:
    line = line.strip().split(",")
    data[row,:] = line
    row +=1
l2 = data[data[:,1]==0]
l1 = data[data[:,2]==0]

vw.plot_regularization(l1,"l1",1,name+mode_name+"-"+"lasso")
vw.plot_regularization(l2,"l2",2,name+mode_name+"-"+"ridge")


