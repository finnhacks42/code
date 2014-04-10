import re

def representative(words, allwords):
    keys = words.keys()
    freqs = []
    total = float(sum(words.values()))
    for w in keys:
        freq = words.get(w)/total
        freqs.append(freq)
    freqs = zip(keys,freqs)
    freqs.sort(key = lambda t: -t[1])
    top = 1 # counts the number of words used to represent this category
    cumsum = 0 # counts the cumulative frequency of the words included so far
    for f in freqs:
        cumsum+=f[1]
        if (cumsum > 0.5 and top > 1) or cumsum > 0.7:
            break
        top +=1
    
    result = [x[0] for x in freqs[0:top]]
    return " ".join(result)

        
#representative(code_word_counts.get('132'),word_counts)
f = open("fixrawdata.txt","r")
f.readline()
count = 0
code_counts = {}
code_prem = {}
word_counts = {}
code_word_counts = {}
while True:
    line = f.readline()
    if not line:
        break
    line = line.split("\t")
    code = line[28].strip('"')
    prem = line[29].strip('"')
    prem = re.sub(r'[^A-Z ]+','',prem)
    prem = re.sub('\s+',' ',prem)
    cc = code_counts.get(code,0)
    code_counts[code]=cc+1
    cp = code_prem.get(code,[])
    cp.append(prem)
    code_prem[code]=cp
    cwc = code_word_counts.get(code,{})
    words = prem.split(" ")
    for w in words:
        if len(w)<2:
            continue
        wc = word_counts.get(w,0)
        wc2 = cwc.get(w,0)
        cwc[w] = wc2+1
        word_counts[w]=wc+1
    code_word_counts[code]=cwc
    count +=1


f.close()

codes = code_word_counts.keys()
codes.sort()

output = []
for c in codes:
    words = code_word_counts.get(c)
    rep = representative(words,word_counts)
    pair='"'+c+'"="'+rep+'"'
    output.append(pair)
    #print c,rep
print 'c('+",".join(output)+')'
    
 501,910,503,920,510,937,913,106,108,812 
