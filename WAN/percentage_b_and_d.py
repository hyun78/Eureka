# -*- coding : utf-8 -*-
# input comes as list of dictionaries

import json
from collections import OrderedDict
import sys
import os
import math

englishDic = {}

f = open("en.txt", 'r')
#f = open("./google-10000-english/20k.txt", 'r')
while True:
    line = f.readline().replace("\n", "")
    if not line: break
    englishDic[line] = 1
f.close()

stereotype = ['LINE', '(LITE)','LITE','(Lite)','(FREE)','(Free)','FREE','Free', '3D', 'HD','(Classic)', 'vs', 'VS']
stereotype_2 = ['FOR KAKAO']

def isnumoral(input):
    # 0~9
    if 48<=input and input<=57:
        return True
    # Capital letters
    if 65<=input and input<=90:
        return True
    # Little letters
    if 97<=input and input <=122:
        return True
    # ' .
    if input == 39 or input == 46:
        return True
    return False

def split_via_upper(string):
    res = []
    for c in string:
        if c.islower():
            if not res:
                res.append(c)
            else: res[-1] += c
        else:
            res.append(c)
    return res

def isEnglishWord(word):
    return word in englishDic.keys()

def read_json_file(filename):
   data = None
   with open(filename, encoding = "utf-8") as data_file:
      data = json.load(data_file, object_pairs_hook = OrderedDict)
   return data

def select_section(filepath, section_str):
    testfile_list = []
    for subdir, dirs, files in os.walk('./' + filepath):
        for file in files:
            if str(file[: min(len(section_str), len(file))]) == section_str:
                testfile_list.append('./' + filepath + '/' + str(file))
    return testfile_list

def clear_parser(filepath_list, stereotype = None ,stereotype_2 = None):
    #settings for stereotypes
    #stereotype = list(map(lambda x: x.upper(),stereotype))
    #stereotype_2 = list(map(lambda x: x.upper(), stereotype_2))

    #the result list
    list_title = []
    for filepath in filepath_list:
        for sets in read_json_file(filepath):
            title = sets['title']
            title_list = []
            temp = title.split(' ')
            for part in temp:
                res = split_via_upper(part)
                check = False
                for item in res:
                    if len(item) < 2:
                        check = True
                        break
                if not check:
                    #print(res)
                    for item in res:
                        title_list.append(item)
                else: title_list.append(part)

            # print (title_list)
            # title_list = list(map(lambda x: x.strip().encode("utf-8"),title_list))
            parsing = []
            for item in title_list:

                # remove inside of parenthesis
                if item.find('(') != -1 and item.rfind(')') != -1:
                    item = item.replace(item[item.find('('):item.rfind(')') + 1], '')

                # nothing to do with empty input - space typo case
                if len(item) == 0:
                    continue

                # remove additional information
                # remove the sub-title by recognizing special words
                item_encode = item.encode("utf-8")
                if not isnumoral(item_encode[-1]):
                    # print(item, item[-1])
                    if len(item_encode) <= 1:
                        break
                    # print (item_str)
                    item_str = item[:-1]
                    if not item_str.upper() in stereotype:
                        item_str = list(item_str)
                        for i in range(len(item_str))[::-1]:
                            if not isnumoral(item_encode[i]):
                                item_str.pop(i)
                        if len(item_str) > 0:
                            parsing.append(''.join(item_str).strip())
                    # but, Dr. , vs. etc '.' gives normal output
                    if item_encode[-1] != 46:
                        break

                # remove stereotypes, non-english words
                if len(item) > 0:
                    if not item.upper() in stereotype:
                        item = list(item)
                        for i in range(len(item))[::-1]:
                            #here, remove ' and . too
                            if item_encode[i]==39 or item_encode[i]==46 or not isnumoral(item_encode[i]):
                                item.pop(i)

                        if len(item) > 0:
                            parsing.append(''.join(item).strip())

            # Afterworks : remove 2-word stereotypes first,
            # and then remove the series name (ex. super action hero 3 -> super action hero)

            if len(parsing) > 0:
                if len(parsing) >= 3 and ' '.join(parsing[-2:]).upper() in stereotype_2:
                    parsing = parsing[:-2]
                if len(parsing[-1]) == 1 and 48 <= parsing[-1].encode("utf-8")[0] <= 57:
                    parsing.pop()
                # print (short_desc_parser(sets['short_desc']) if 'short_desc' in sets.keys() else None)
                list_title.append(parsing)
    return list_title

num = 50

def percentage_b_and_d(testfile_list, stereotype = None, stereotype_2 = None):
    global num
    list_title = clear_parser(testfile_list, stereotype, stereotype_2)
    B = D = 0
    for title in list_title:
        check = False
        for word in title:
            if len(word) == 1 or word.isdigit(): continue
            if not isEnglishWord(word.lower()):
                print(word)
                check = True
                break
        if check: B += 1
        else: D += 1

    ans1 = round(B / (B + D) * 100), round(D / (B + D) * 100)
    b, d = B / (B + D), D / (B + D)

    '''
    avg = 0.16
    B = 100 * avg * math.exp(b - avg)
    D = math.exp(d)
    '''

    ans2 = round(B)
    #ans2 = round(B / (B + D) * 100), round(D / (B + D) * 100)

    return ans1#, ans2


#print(vb.meaning("error"))

'''
print(vb.meaning("surfers"))
print(isEnglishWord("surfers"))
print(isEnglishWord("tiles"))
print(isEnglishWord("birds"))
print(isEnglishWord("cookie"))
'''

testfile_list = select_section('database_crawling', 'arcade')
print("b, d:", percentage_b_and_d(testfile_list, stereotype, stereotype_2))
testfile_list = select_section('database_crawling', 'social')
print("b, d:", percentage_b_and_d(testfile_list, stereotype, stereotype_2))
testfile_list = select_section('database_crawling', 'shopping')
print("b, d:", percentage_b_and_d(testfile_list, stereotype, stereotype_2))