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
        associations[i].append(keywords[i])

    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            for s1 in associations[i]:
                for s2 in associations[j]:
                    if order(s1['pos'], s2['pos']):
                        name = (s1['item'] + s2['item']).lower()
                        res.append([name, s1['item'], s2['item']])
    return res


def morpheme(keywords, associations):
    res = []
    n = len(associations)

    for i in range(n):
        associations[i].append(keywords[i])

    for i in range(n):
        for j in range(n):
            if i == j: continue
            for s1 in associations[i]:
                x1 = s1['item']
                for s2 in associations[j]:
                    x2 = s2['item']
                    if len(x2) > 5: continue
                    if order(s1['pos'], s2['pos']):
                        syl1 = SonoriPy(s1['item'])
                        syl2 = SonoriPy(s2['item'])
                        r1 = ""
                        for t1 in syl1:
                            r1 += t1
                            if len(r1) > 5: break
                            #if len(r1) < 3: continue
                            #res.append([(r1 + x2).lower(), x1, x2])
                            #continue
                            r2 = ""
                            for t2 in syl2:
                                r2 += t2
                                if len(r2) > 5: break
                                x1 = s1['item'].lower()
                                x2 = s2['item'].lower()
                                res.append([(r1 + r2).lower(), x1, x2 ])
    return res

def prefix_suffix(keywords, associations):
    res = []
    n = len(associations)

    for i in range(n):
        associations[i].append(keywords[i])

    for i in range(n):
        for j in range(n):
            #if i == j: continue
            for s1 in associations[i]:
                x1 = s1['item']
                for s2 in associations[j]:
                    x2 = s2['item']
                    #if len(x2) > 5: break
                    if s2['pos'] != 'noun': continue
                    l1 = len(x1)
                    l2 = len(x2)
                    for common in range(2, min(l1, l2) + 1):
                        for r1 in range(0, max(0, l1 - common)):
                            if x1[r1] in "aeoui": continue
                            '''max(0, min(l2 - common, 3))'''
                            for r2 in range(0, 2):
                                if x1[r1:r1+common] == x2[r2:r2+common]:
                                    name = (x1[:r1] + x2[r2:]).lower()
                                    if name == x1.lower() or name == x2.lower():
                                        continue
                                    res.append([name, x1, x2])
    return res

def test():
    associated_words_set = search_WAN(['flower', 'tree'])

    keywords = []
    associations = []
    for list in associated_words_set:
        key = list['text']
        pos = get_pos(key)
        keywords.append({'pos' : pos, 'item' : key})
        associations.append(list['items'])


    res1 = descriptive(keywords, associations)
    res2 = morpheme(keywords, associations)
    res3 = prefix_suffix(keywords, associations)

    for i in range(30):#for x in res:
        x = random.choice(res3)
        print(x[0] + "  = " + x[1] + "  + " + x[2])

    return

test()
