import re
from operator import itemgetter

# returns a list of key,values tuples, sorted by value
def sort_dict_by_value(d,reverse=False):
    ''' proposed in PEP 265, using  the itemgetter '''
    return sorted(d.iteritems(), key=itemgetter(1), reverse=True)

def delete_words(words, text):
    p_to_remove = [re.compile(r'\b%s\b' % word, re.I) for word in words]
    for p in p_to_remove:
        text = p.sub("",text)
    text = re.sub("\s{2,100}"," ",text).strip()
    return text

def abreviate(abrevs, text):
    for r in abrevs:
        if r in text:
            text = text.replace(r,rp.get(r))
    text = re.sub("\s{2,100}"," ",text).strip()
    return text



f = open("fixrawdata.txt","r")
missing = "null" #encode any missing or illegal values with this


rp = {"PROPERTY":"PROP","RESIDENCE":"RES","HABITATION":"HAB","IDENTITY":"ID","OUT TOWN":"OT","BURGLARY MOTOR VEHICLE":"BMV","B M V":"BMV","AGGRAVATED":"AGG","ATTED":"ATT","ATTEMPT":"ATT","FAMILY VIOLENCE":"FV","CLASS A":"MA","CRIMIANL":"CRIM","CRIMINAL":"CRIM","MISCHEIF":"MISCH","MISCHIEF":"MISCH","BURGLARY":"BURG","F L I D":"FLID"}
simple = ["SHOPLIFT","PHONE"]
words_to_remove =  ["FV","OF","A"]



cats = {}

count = 0
while count < 10:
    line = f.readline()
    if not line:
        break
    line = line.split("\t")
    
    descrip = re.sub("[().\/]*","",line[4]).strip('"')
    descrip = delete_words(["OF","A"],descrip)
    descrip = abreviate(rp,descrip)
    descrip = delete_words(["FV"],descrip)
    
    for s in simple:
        if s in descrip:
            descrip = s
    
    score = cats.get(descrip)
    if score == None:
        score = 0
    cats[descrip] = score + 1
    
        
result = sort_dict_by_value(cats,True)
cum = 0
for i in range(100):
    cat = result[i][0]
    count = result[i][1]
    cum += count
    print cat,count*100/2249596,cum*100/2249596

        
 
    



