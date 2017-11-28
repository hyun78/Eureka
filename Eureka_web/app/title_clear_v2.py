# -*- coding : utf-8 -*-
# input comes as list of dictionaries

import json
from collections import OrderedDict
from nltk.tag import pos_tag
from nltk.corpus import words
import functools
import re
import os

def read_json_file(filename):
   data = None
   with open(filename, encoding="utf-8") as data_file:
      data = json.load(data_file, object_pairs_hook=OrderedDict)
   return data


def isal(strin):
    if len(strin)==0: return False
    al = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    strin = list(strin)
    strin[0] = strin[0] in al
    return functools.reduce(lambda x,y: x and (y in al),strin)

stereotype = ['','LINE', '(LITE)','LITE','(Lite)','(FREE)','(Free)','FREE','3D', 'HD','(Classic)','2D', 'VHD', 'PRO', 'AR', 'A', 'THE', 'OF', 'BY', 'ON', 'AN', 'AND', 'FOR', 'KAKAO']
#Pro? (iGun Pro)
stereotype_2 = ['FOR KAKAO']
dict_statistics = {}
cnt_statistics = {}

filename = "./arcade.json"

def select_section(filepath, section_str):
    testfile_list = []
    for subdir, dirs, files in os.walk('./'+filepath):
        for file in files:
            if str(file[:min(len(section_str),len(file))]) == section_str:
                testfile_list.append('./'+filepath+'/'+str(file))
    return testfile_list

def short_desc_parser(str_desc):
    only_alphabet = re.sub('[^a-zA-Z]+', ' ', str_desc).split()
    stereotype_desc = ['A', 'AN', "THE", 'OR', 'BUT','SO', 'AND', 'FROM', 'TO',
                       'YOUR', 'IN', 'ON', 'THIS', 'THAT', 'IT', 'HIS', 'HER', 'IS', 'FOR', 'AT', 'OF','ITS','THEIR', 'THEM', 'BY']
    only_alphabet = [item for item in only_alphabet if item.upper() not in stereotype_desc]
    return only_alphabet

#input : filepath, adversal stereotypes, adversal stereotypes_2 for stereotypes consist of 2 words.
#output : list of strings, that indicates the parsed title of app

def clear_parser(filepath_list, maxlen = 2, stereotype = None ,stereotype_2 = None):
    #settings for stereotypes
    stereotype = list(map(lambda x: x.upper(),stereotype))
    stereotype_2 = list(map(lambda x: x.upper(), stereotype_2))

    #the result list
    list_title = []
    for filepath in filepath_list:
        for sets in read_json_file(filepath):
            title = sets['title']
            title_list = re.findall(r"[\w']+", title) #title names are separated in list

            # print (title_list)
            # title_list = list(map(lambda x: x.strip().encode("utf-8"),title_list))
            parsing = []
            item_num=0
            for item in title_list:
                if item.upper() in stereotype:
                    continue
                elif isal(item[:-1]) and len(item)>1:
                    item_num +=1
                    if item_num == maxlen + 1:
                        break
                    parsing.append(item if isal(item[-1]) else item[:-1])
            if item_num < maxlen+1:
                if len(parsing)!=0:
                    #parsing.append('|||||')
                    #parsing.append(sets['title'])
                    list_title.append(' '.join(parsing))

    return list_title



#for test
#l_title = clear_parser(testfile_list,stereotype,stereotype_2)

def sectiondata_save_json(datafiles_dir, savefile_name,stereotype, stereotype_2):
    testfile_list = select_section(datafiles_dir, 'arcade')
    total_dict = clear_parser(testfile_list,2,stereotype,stereotype_2)
    with open(savefile_name+'.json', 'w') as fp:
        json.dump(total_dict, fp)

#for test
if __name__=='__main__':
    datafiles_dir='database_crawling'
    sectiondata_save_json(datafiles_dir, 'cp_data_arcade', stereotype, stereotype_2)
