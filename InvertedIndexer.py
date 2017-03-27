import os
import operator
import math
import matplotlib.pyplot as plt

# This is the file directory where the corpus is
directory = r'page/'

# get 2-gram list
def find_bigrams(list):
  bigram_list = []
  for i in range(len(list)-1):
      bigram_list.append((list[i] + ' ' + list[i + 1]))
  return bigram_list

# get 3-gram list
def find_trigrams(list):
  trigram_list = []
  for i in range(len(list)-2):
      trigram_list.append((list[i] + ' ' + list[i + 1] + ' ' + list[i + 2]))
  return trigram_list

# generate inverted index for N-grams
def indexer_Ngrams(directory, ngram):
    Map_index = {}
    filelist = os.listdir(directory)
    for file in filelist:
        path = directory + file
        doc = open(path, 'r')
        source_code = doc.read()
        doc.close()
        list = []
        split_list = source_code.split(r' ')

        # process /s
        for word in split_list:
            if word != r' ' and word != '':
                # print(each)
                list.append(word)

        if ngram == 1:
            path = r'index_unigram.txt'
            list = list
        if ngram == 2:
            path = r'index_bigram.txt'
            list = find_bigrams(list)
        if ngram == 3:
            path = r'index_trigram.txt'
            list = find_trigrams(list)

        for word in list:
            if word not in Map_index.keys():
                Map_index.update({word:dict()})
            if file not in Map_index.get(word).keys():
                Map_index.get(word).update({file:1})
            else:
                Map_index[word][file] += 1

    fx = open(path, 'w')
    for item in Map_index:
        fx.write(item +':'+ str(Map_index.get(item)) + '\n')
    fx.close()

    return Map_index

# calculate term frequency
def statics_tf(Map, ngram):
    Map_tf = {}
    for term in Map.keys():
        tf = 0
        for doc in Map.get(term).keys():
            tf = tf + Map.get(term).get(doc)
        Map_tf.update({term:tf})
    sorted_tf = sorted(Map_tf.items(), key=operator.itemgetter(1), reverse = True)
    if ngram == 1:
        path = r'term_frequency_unigram.txt'
    if ngram == 2:
        path = r'term_frequency_bigram.txt'
    if ngram == 3:
        path = r'term_frequency_trigram.txt'
    fx = open(path, 'w')
    for item in sorted_tf:
        fx.write(str(item) + '\n')
    fx.close()
    return Map_tf

# calculate doc frequency
def statics_df(Map, ngram):
    Map_df = {}
    for term in Map.keys():
        df = 0
        dl = []
        for doc in Map.get(term).keys():
            df = df + 1
            dl.append(doc)
        dl.append(str(df))
        Map_df.update({term:dl})
    sorted_df = sorted(Map_df.items(), key=operator.itemgetter(0))
    if ngram == 1:
        path = r'doc_frequency_unigram.txt'
    if ngram == 2:
        path = r'doc_frequency_bigram.txt'
    if ngram == 3:
        path = r'doc_frequency_trigram.txt'
    fx = open(path, 'w')
    for item in sorted_df:
        fx.write(str(item) + '\n')
    fx.close()
    return Map_df

# calculate tf-idf for unigram data to generate stoplist
def tf_idf(Map):
    result_list = []
    Map_tfidf = {}
    for term in Map.keys():
        df = 0
        tf = 0
        for doc in Map.get(term).keys():
            df = df + 1
            tf = tf + Map.get(term).get(doc)
        idf = math.log10(1000/df)
        result = idf*(1 + math.log10(tf))
        Map_tfidf.update({term: result})
        result_list.append(result)
    result_list.sort()
    tfidf = sorted(Map_tfidf.items(), key=operator.itemgetter(1), reverse = False)
    fx = open('tf-idf.txt', 'w')
    for item in tfidf:
        fx.write(str(item) + '\n')
    fx.close()
# draw tf-id plot
    plt.title('Plot of unigram tf-idf')
    plt.plot(result_list)
    plt.show()

# draw Zipfian plot
def draw_ziph(Map,gram):
    list = []
    for term in Map.keys():
        tf = 0
        for doc in Map.get(term).keys():
            tf = tf + Map.get(term).get(doc)
        list.append(math.log(tf, 10))
    list.sort(reverse = True)
    plt.title('Zipfian curves for ' + gram)
    plt.xlabel('Rank(1)')
    plt.ylabel('frequency(log10())')
    plt.plot(list)
    plt.show()



u = indexer_Ngrams(directory, 1)
# tf_idf(u)         #for generating stoplist
statics_tf(u, 1)
statics_df(u, 1)
# draw_ziph(u,'unigram')        # for Zipfian curve

b = indexer_Ngrams(directory, 2)
statics_tf(b, 2)
statics_df(b, 2)
# draw_ziph(b,'bigram')

t = indexer_Ngrams(directory, 3)
statics_tf(t, 3)
statics_df(t, 3)
# draw_ziph(t,'trigram')