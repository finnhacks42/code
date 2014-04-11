#vw -k -l .5 --l2 0 -d ctrain --cache_file /tmp/vw.cache  -f model1 --invert_hash model1.read  --passes 100
# run vw for a range of different l1 and l2 values - saving all outputs. Then I can write the code to evaluate the results later ...

from optparse import OptionParser
from subprocess import call


def run(train,test,l1,l2,run,mode,mode_name,name):
    
    model_name = name+mode_name+str(run)+".mod"
    pred_name = name+mode_name+str(run)+".pred"
    outname = name+mode_name+str(run)+".out"
    testout = name+mode_name+str(run)+".tout"
    
    train_call = "vw -l .5 --l2 "+str(l2)+" --l1 "+str(l1)+" -d "+train+" --cache_file /tmp/vw.cache -f "+model_name+" --passes 50 --holdout_off "+mode+" 2> "+outname
    test_call = "vw -t -d "+test+" --cache_file /tmp/vw.valid.cache -i "+model_name+" -p "+pred_name+" 2> "+testout 
   
    call(train_call,shell=True)
    print train_call
    call(test_call,shell=True)
    print test_call

parser = OptionParser()
parser.add_option("-m","--mode",dest = "mode",help="mode arguament to vw ie '-q a:'")
parser.add_option("-t","--test",action="store_true",dest = "test",help="run only for a single value for l1 and l2 - useful for testing")
parser.set_defaults(test=False,mode="")
(options,args) = parser.parse_args()
print options,type(options)
print args


train = args[0]
test = args[1]
mode = options.mode
is_test = options.test

if is_test:
    l1_list = [0]
    l2_list = [0]
else:
    l1_list = [0,.000001,.00001,.0001,.001,.01,.1]
    l2_list = [0,.000001,.00001,.0001,.001,.01,.1]
    
mode_name = mode.replace(" ","").replace("-","").replace(":","")
name = train.replace("train","")
o = open("reg"+name+mode_name,"w")
i = 1
prep_call = "rm -f /tmp/vw.cache"
prep_call2 = "rm -f /tmp/vw.valid.cache"
call(prep_call,shell=True)
call(prep_call2,shell=True)
for l1 in l1_list:
    for l2 in l2_list:
        run(train,test,l1,l2,i,mode,mode_name,name)
        o.write(str(i)+","+str(l1)+","+str(l2)+"\n")
        i +=1
o.close()
