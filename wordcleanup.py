from operator import itemgetter
import re

# group words based on various types of similarities
# being a substring, number of subtractions/translations, similarity to partner words
def readwords():
    f = open("1000words.txt")
    words = []
    wdict = {}
    for line in f.readlines():
        line = line.strip().split("|")
        word = (line[0],line[1])
        words.append(word)
        wdict[line[0]]=line[1]
    f.close()
    return (words,wdict)

def shortening(words,word_dict,minlength):
    result = {}
    wordlist = [w[0] for w in words]
    wordlist.sort()
    current = wordlist[0]
    lst = [current]
    for i in range(1,len(wordlist)):
        w = wordlist[i]
        if len(current) >= minlength and w.startswith(current):
            lst.append(w)
            #print current,len(current)
        else:
            current = w
            if len(lst) > 1:
                #find highest scoring word in list as 'canonical' form
                maxscore = 0
                bestword = None
                for word in lst:
                    score = word_dict[word]
                    if score > maxscore:
                        maxscore = score
                        bestword = word
                for word in lst:
                    if word != bestword:
                        result[word]=bestword
                #print bestword,lst
                        
                    
            lst = [current]
    return result

def sort_dict_by_value(d,reverse=False):
    ''' proposed in PEP 265, using  the itemgetter '''
    return sorted(d.iteritems(), key=itemgetter(1), reverse=True)

def print_data(lst,numelements):
    cumper = 0
    for i in range(100):
        text = lst[i]
        per = text[1]*100/float(numelements)
        cumper += per
        print text[0]+"|"+str(per),cumper

def delete(text,strs):
    for s in strs:
        text = text.replace(s,"")
    return text

# only delete these if there is a word boundary on either side
def delete_words(text, words):
    for w in words:
        text = re.sub(r"\b\s?%s\b"%w,r"",text)
    return text

# for each word in the text check if it has a replacement specified in the dictionary
def word_replace(text_words,dct):
    for indx, word in enumerate(text_words):
        rpl = dct.get(word)
        if rpl:
            text_words[indx] = rpl
            
    

wordstuff = readwords()
shorts_map = shortening(wordstuff[0],wordstuff[1],4)

aslashb = re.compile("[A-Z]/[A-Z]")
TEXT_FIELD = 4
f = open("fixrawdata.txt","r")

textcounts = {}
wordcounts = {}
count = 0
f.readline()
while count < 100:
    #count +=1
    line = f.readline()
    if not line:
        break
    line = line.split("\t")
    text = line[TEXT_FIELD].strip('"')
    

    if True:    
        text = delete(text,[".",")","(",","])
        text = re.sub(r"\b([A-Z]{1})/([A-Z]{1})\b",r"\1\2",text) #if it looks like A/B then make it AB
        text = text.replace("/"," ")
        text = text.replace(":"," ")
        text = text.replace(";"," ")
        text = delete_words(text,["FV","W","OF","A","TO","BY","ON","WITH","OR","THE","FOR"])
        text = re.sub(r"-+",r" ",text)
        text = re.sub(r"\b[A-Z]{1}\b","",text)
        text = re.sub(r"\s+",r" ",text)
        text = text.strip()
        if "POS " in text:
            print text
        
        text_words = text.split(" ")
        word_replace(text_words,shorts_map)
        text = " ".join(text_words)
            
        
        tc = textcounts.get(text)
        if tc == None:
            tc = 0
        textcounts[text] = tc + 1
        words = text.split(" ")
        for w in words:
            wc = wordcounts.get(w)
            if wc == None:
                wc = 0
            wordcounts[w] = wc + 1
        #count +=1

        
texts = sort_dict_by_value(textcounts,True)
words = sort_dict_by_value(wordcounts,True)

numtexts = sum(textcounts.values())
numwords = sum(wordcounts.values())

print_data(texts,numtexts)
#print_data(words,numwords)

    



f.close()
