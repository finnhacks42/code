# now we are getting to the bit where we actually say words are the same...

#one could be a subset of another word
#could be another word with all the vowels removed
#could be a concatenation of two other words in the list
#could be a spelling mistake - is there a library for this?
#could be missing a letter, have an additional letter, a swapped letter, a wrong letter

import enchant #spell checking library
import re

def vowel_deletions():
    for w in words:
        no_vowels = re.sub(r"[AEIOU]*","",w)
        if len(no_vowels) > 2:
            for w2 in words:
                if w2 == no_vowels and w2 != w:
                    print w,w2



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

# where d maps values to lst of tuples (v,vscore), pick the new v as the one with the highest score
def pick_best(dct):
    d = {}
    for key,tpls in dct.iteritems():
        top_score = 0
        top_value = None
        for t in tpls:
            if t[1] > top_score:
                top_score = t[1]
                top_value = t[0]
        d[key] = top_value
    return d

# check the dictionary for paterns of the type a -> b -> c ->... ->z and replaces them with a - > z
def dechain(dct):
    #TODO
    return dct
    
            
def find_merge_splits():
    #test if a word is two other words joined together ...
    splits = {}#maps word to a list of possible splits for that word
    merges = {}#maps pairs of words to possible merges of those pairs
    for w in word_dict.keys():
        for w2 in word_dict.keys():
            l = len(w2)
            if w2 != w and l > 3 and l < len(w) - 3 and w.startswith(w2):
                end = w[l:]
                if end in word_dict:
                    scores = [word_dict[w],word_dict[w2],word_dict[end]]
                    split = w2+" "+end
                    if min(scores) == scores[0]:
                        existing_splits = splits.get(w)
                        if not existing_splits:
                            existing_splits = []
                            tpl = (split,min(scores[1:]))
                        existing_splits.append(tpl)
                        splits[w] = existing_splits
                    else: # it is better to merge these two
                        existing_merges = merges.get(split)
                        if not existing_merges:
                            existing_merges=[]
                        existing_merges.append((w,scores[0]))
                        merges[split]=existing_merges
    splits = dechain(pick_best(splits))
    merges = dechain(pick_best(merges))
    return (splits,merges)

def shortening(words,word_dict):
    result = {}
    wordlist = [w[0] for w in words]
    wordlist.sort()
    current = wordlist[0]
    lst = [current]
    for i in range(1,len(wordlist)):
        w = wordlist[i]
        if len(current) > 2 and w.startswith(current):
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
                print bestword,lst
                        
                    
            lst = [current]
    return result

def correct(words,word_dict,fix_dict):
    for word in fix_dict.keys():
        del word_dict[word]

    words2 = []
    for key,value in word_dict.iteritems():
        wobject = (key,value)
        words2.append(wobject)
    return (words2,word_dict)
   
            

    
#for words that are where w1 is a prefix of length 3 of w2, check how similar the words on either side are ...

word_stuff = readwords()
words = word_stuff[0] # a list of tuples with word/score
word_dict = word_stuff[1] # a dictionary from word to score

merge_and_split = find_merge_splits()
splits = merge_and_split[0]
merges = merge_and_split[1]

print len(words)
print len(word_dict)
# do the splitting first before we apply the shortening
word_stuff = correct(words,word_dict,splits)
words = word_stuff[0] # a list of tuples with word/score
word_dict = word_stuff[1] # a dictionary from word to score


shortening(words,word_dict)






                                           
                
                
            





            

