import numpy as np
import vw
from subprocess import call
import sys

def run(run):
    model_name = name+mode_name+str(run)+".mod"
    pred_name = name+mode_name+str(run)+".pred"  
    train_pred_call = "vw -t -d "+train+" --cache_file /tmp/vw.cache -i "+model_name+" -p "+train_pred +" 2>"+trainout
    call(train_pred_call,shell=True) 
    p_train = vw.read(train_pred)
    p_test = vw.read(pred_name)
    rmse_train = vw.rmse(p_train,actual_train)
    pai_train = vw.meanPaiArea(p_train,actual_train,num_areas)
    rmse_test = vw.rmse(p_test,actual_test)
    pai_test = vw.meanPaiArea(p_test,actual_test,num_areas)
    return [rmse_train,pai_train,rmse_test,pai_test]


# model goes from 1 - 49, going through l1 and then l2
#l1_list = [0,.000001,.00001,.0001,.001,.01,.1]
#l2_list = [0,.000001,.00001,.0001,.001,.01,.1]


# we are going to create a new result file model, l1,l2,train_rmse,train_pai,test_rmse,test_pai

name = sys.argv[1]
mode_name=sys.argv[2]
num_areas = int(sys.argv[3])

train = name+"train"
test = name+"valid"
actual_train = vw.read(train+".target")
actual_test = vw.read(test+".target")

# clear the cashe
call("rm -f /tmp/vw.cache",shell=True)

# run the model on the test data
trainout = "tmp.out"
train_pred = "train.pred"

output_name = name+mode_name+".result2"
o = open(output_name,"w")

result_file = open(name+mode_name+".result")
for line in result_file.readlines():
    line = line.split(",")
    i = int(line[0])
    l1 = float(line[1])
    l2 = float(line[2])

    result = run(i)
    result = [str(x) for x in result]
    o.write(str(i)+","+str(l1)+","+str(l2)+","+",".join(result)+"\n")
    print i
    i+=1
result_file.close()
o.close()

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
       
        
