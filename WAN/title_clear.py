# -*- coding : utf-8 -*-
# input comes as list of dictionaries

import json
from collections import OrderedDict

def read_json_file(filename):
   data = None
   with open(filename, encoding="utf-8") as data_file:
      data = json.load(data_file, object_pairs_hook=OrderedDict)
   return data

def isnumoral(input):
    if 48<=input and input<=57:
        return True
    if 65<=input and input<=90:
        return True
    if 97<=input and input <=122:
        return True
    return False

stereotype = ['LINE', '(LITE)','LITE','(Lite)','(FREE)','(Free)','FREE','Free', '3D', 'HD','(Classic)']
stereotype_2 = ['FOR KAKAO']

filename = "./arcade.json"

#input : filepath, adversal stereotypes, adversal stereotypes_2 for stereotypes consist of 2 words.
#output : list of strings, that indicates the parsed title of app

def clear_parser(filepath, stereotype = None ,stereotype_2 = None):
    #settings for stereotypes
    stereotype = list(map(lambda x: x.upper(),stereotype))
    stereotype_2 = list(map(lambda x: x.upper(), stereotype_2))

    #the result list
    list_title = []
    for sets in read_json_file(filename):
        title = sets['title']
        title_list = title.split(' ')
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
            # remove the sub-title by recognizing speacial words
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
                        if not isnumoral(item_encode[i]):
                            item.pop(i)
                    if len(item) > 0:
                        parsing.append(''.join(item).strip())
        if len(parsing) > 0:
            if len(parsing) >= 3 and ' '.join(parsing[-2:]).upper() in stereotype_2:
                parsing = parsing[:-2]
            if len(parsing[-1]) == 1 and 48 <= parsing[-1].encode("utf-8")[0] <= 57:
                parsing.pop()
            list_title.append(' '.join(parsing))
    return list_title

#for test
print(len(clear_parser(filename,stereotype,stereotype_2)))
print(clear_parser(filename,stereotype,stereotype_2))