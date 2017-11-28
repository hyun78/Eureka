from __future__ import division
from sklearn.cluster import KMeans
from numbers import Number
import sys, codecs, json
import numpy as np

def read_json_file(filename, object):
   with open(filename) as data_file:
      data = json.load(data_file, object_pairs_hook = object)
   return data

class autovivify_list(dict):
    '''Pickleable class to replicate the functionality of collections.defaultdict'''
    def __missing__(self, key):
        value = self[key] = []
        return value

    def __add__(self, x):
        '''Override addition for numeric types when self is empty'''
        if not self and isinstance(x, Number):
                return x
        raise ValueError

    def __sub__(self, x):
        '''Also provide subtraction method'''
        if not self and isinstance(x, Number):
                return -1 * x
        raise ValueError

def get_word_set(path):
    temp = read_json_file(path+'title.json', list)
    descs = read_json_file(path+'description.json', list)
    short_descs = read_json_file(path+ 'short_description.json', list)

    print(temp)
    print(descs)
    print(short_descs)

    titles = []
    for title in temp:
        for word in title.split(' '):
            titles.append(word)

    return set(titles + descs + short_descs)

def build(word_vector_file, word_set):
    word_list = []
    vector_list = []

    with codecs.open(word_vector_file, 'r', 'utf-8') as f:
        for c, r in enumerate(f):
            sr = r.split()
            try:
                word = sr[0]
                if word_set == None or word in word_set:
                    word_list.append(word)
                    vector = np.array([float(i) for i in sr[1:]])
                    vector_list.append(vector)
                    print(c)
            except: pass

    return word_list, np.array(vector_list)

def find_word_clusters(labels_array, cluster_labels):
    '''Read in the labels array and clusters label and return the set of words in each cluster'''
    cluster_to_words = autovivify_list()
    for c, i in enumerate(cluster_labels):
        cluster_to_words[ i ].append( labels_array[c] )
    return cluster_to_words

def clustering(section, cluster_cnt = 20):
    glove_file = "glove.6B.300d.txt"

    words, vectors = build(glove_file, get_word_set('database/'+section+'/'))
    kmeans_model = KMeans(init = 'k-means++', n_clusters = cluster_cnt, n_init = 10)
    kmeans_model.fit(vectors)

    cluster_labels = kmeans_model.labels_
    cluster_to_words = find_word_clusters(words, cluster_labels)

    with open('database/'+section+'/'+"clustered_file", "w") as f:
        for c in cluster_to_words:
            for word in cluster_to_words[c]:
                f.write(word + '\t')
            f.write('\n')

    cluster_dict = {}

    cluster = 0
    for c in cluster_to_words:
        for word in cluster_to_words[c]:
            cluster_dict.update({word : cluster})
        cluster += 1

    with open('database/'+section+'/'+"clustered_dictionary.json", "w") as f:
        json.dump(cluster_dict, f)


# for test
if __name__  == '__main__':
    clustering(section = 'GAME_ARCADE', cluster_cnt = 25)