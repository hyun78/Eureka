import random
from syllabipy.sonoripy import SonoriPy
from wan import *

def order(type1, type2):
    type1 = type1.lower()
    type2 = type2.lower()

    t1 = 'noun'
    t2 = 'adjective'
    t3 = 'adverb'
    t4 = 'verb'

    return (type1 == t1 or type1 == t2) and type2 == t1

def descriptive(keywords, associations):
    res = []
    n = len(associations)

    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            for s1 in associations[i]:
                for s2 in associations[j]:
                    if order(s1['pos'], s2['pos']):
                        res.append((s1['item'] + s2['item']).upper())
    return res


def morpheme(keywords, associations):
    res = []
    n = len(associations)

    for i in range(n):
        for j in range(n):
            if i == j: continue
            for s1 in associations[i]:
                for s2 in associations[j]:
                    if order(s1['pos'], s2['pos']):
                        syl1 = SonoriPy(s1['item'])
                        syl2 = SonoriPy(s2['item'])
                        r1 = ""
                        for t1 in syl1:
                            r1 += t1
                            if len(r1) > 5: break
                            r2 = ""
                            for t2 in syl2:
                                r2 += t2
                                if len(r2) > 5: break
                                res.append((r1 + r2).upper())
    return res

def test():
    associated_words_set = search_WAN(['fresh', 'water', 'white', 'cool'])

    keywords = []
    associations = []
    for list in associated_words_set:
        #key = list['text']
        #pos = get_pos(key)
        #keywords.append({'pos' : pos, 'item' : key})
        associations.append(list['items'])
    res1 = descriptive(keywords, associations)
    print(res1)
    res2 = morpheme(keywords, associations)
    print(res2)
    return


test()