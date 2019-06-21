import sys
import re
import math
import time
from nltk import PorterStemmer


stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

ps = PorterStemmer()

def scan_index(path, word):
    ''' Returns the posting list for the word
    '''
    inputbuffer = ''
    with open(path,'r') as inputfile:
        mapping = {}
        for line in inputfile:
            i_word = line.split('.')[0]
            if word == i_word:
                doc_freq_map = line.split('.')[1:]
                for mapset in doc_freq_map:
                    if len(mapset) > 2:
                        terms = mapset.split('_')
                        mapping[terms[0]] = terms[1]
                return mapping
        return None

def rank(doclist, words, postings):
    scoring = {}
    for doc in doclist:
        score = 0
        for word in words:
            score += math.log(1 + int(postings[word][doc])) * math.log(TOTAL_DOC / len(postings[word]))
        scoring[doc] = score
    s = [k for k in sorted(scoring, key=scoring.get, reverse=True)]
    global doc_map
    keys = doc_map.keys()
    count = 0
    for i in range(len(s)):
        if s[i] not in keys:
            continue
        out = doc_map[s[i]]
        if re.search('Wikipedia', out) != None:
            continue
        if count > 10:
            break
        print(out)
        count += 1




def process(postings):
    lst = {}
    words = postings.keys()
    for word in words:
        for doc in postings[word].keys():
            if doc not in lst.keys():
                lst[doc] = 1
            else:
                lst[doc] += 1
    req = len(words)
    lstfinal = []
    for elem in lst:
        if lst[elem] == req:
            lstfinal.append(elem)
    rank(lstfinal, words, postings)
    return

def query_func(index_path):
    global stopwords
    alphabet = range(0, 26)
    print("Ready")
    while True:
        query = input("Query: ")
        if query == 'q':
            return
        else:
            querystart = time.time()
            query = query.lower()
            tokens = query.split(" ")
            plist = {} 
            for word in tokens:
                if word in stopwords:
                    continue
                search_word = ps.stem(word)
                if len(search_word) < 2:
                    continue
                t1 = ord(search_word[0]) - 97
                t2 = ord(search_word[1]) - 97
                if t1 not in alphabet:
                    t1 = 26
                if t2 not in alphabet:
                    t2 = 26
                search_path = str(t1) + '_' + str(t2)
                temp = scan_index(index_path + '/' + search_path, search_word)
                if temp:
                    plist[search_word] = temp
            process(plist)
            queryend = time.time()
            print('Time Taken:', queryend-querystart)



def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

doc_map = {}
def load_doc_map():
    global doc_map
    with open(index_path+'/'+'doc_id_map', 'r') as inputfile:
        for line in inputfile:
            if len(line) > 2:
                docid = line.split(':')[0]
                reststart = len(docid)
                content = line[reststart+1:]
                doc_map[docid] = content



#     a = a[3:]
#     a = a[:-1]
#     permitrange = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
#     tokens = a.split('\', ')
#     x = 1
#     for st in tokens:
#         x += 1
#         w = st.split(':')
#         canadd = True
#         for i in w[0]:
#             if i not in permitrange:
#                 canadd = False
#         if not canadd:
#             continue
#         docid = str(int(w[0]))
#         # Change if not working
#         val = w[1]
#         doc_map[docid] = val
        
if __name__ == '__main__':
    tstart = time.time()
    index_path = str(sys.argv[1])
    load_doc_map()
    f = open('docnum', 'r')
    TOTAL_DOC = int(f.read())
    f.close()
    query_func(index_path)
        
    tend = time.time()
    print("End Time:", tend - tstart)

