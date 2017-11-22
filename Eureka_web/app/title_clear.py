# -*- coding : utf-8 -*-
# input comes as list of dictionaries

import json
from collections import OrderedDict
from nltk.tag import pos_tag
from nltk.corpus import words
import re
import os

englishDic = dict.fromkeys(words.words(), None)

def isEnglishWord(word):
    try:
        x = englishDic[word]
        return True
    except KeyError:
        return False

def getPos(name):
    ##temp error pass
    name = name.lower()
    name = ''.join(e for e in name if e.isalnum() or e == ' ')
    res =  pos_tag(name.split())
    ret_val = [pos if isEnglishWord(stri) else 'NNP' for stri, pos in res]
    return str(ret_val[0])

#print(getPos('run'))

def read_json_file(filename):
   data = None
   with open(filename, encoding="utf-8") as data_file:
      data = json.load(data_file, object_pairs_hook=OrderedDict)
   return data

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

stereotype = ['LINE', '(LITE)','LITE','(Lite)','(FREE)','(Free)','FREE','Free', '3D', 'HD','(Classic)','VR','2D','HD','2HD', 'Pro','AR']
stereotype = stereotype + list(range(1900,2019))

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

def clear_parser(filepath_list, stereotype = None ,stereotype_2 = None):
    #settings for stereotypes
    stereotype = list(map(lambda x: str(x).upper(),stereotype))
    stereotype_2 = list(map(lambda x: str(x).upper(), stereotype_2))

    #the result list
    list_title = []
    for filepath in filepath_list:
        for sets in read_json_file(filepath):
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
                            #if item_encode[i]==39 or item_encode[i]==46 or not isnumoral(item_encode[i]):
                            #    item.pop(i)
                            if isnumoral(item_encode[i]):
                                item =''

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
                list_title.append({'title' : ' '.join(parsing)})
                #
                #{'title': ' '.join(parsing), 'downloads': sets['downloads_min'], 'rating': sets['rating'],
                #    'short_desc': short_desc_parser(sets['short_desc']) if 'short_desc' in sets.keys() else None}

            #else:
                #"""
                #list_title.append(
                #    {'title': 'Adversal_input', 'downloads': sets['downloads_min'], 'rating': sets['rating'],
                #     'short_desc': short_desc_parser(sets['short_desc']) if 'short_desc' in sets.keys() else None})
                #"""
    return list_title



def make_stat(list_title):
    for keys in list_title:

        if keys['short_desc'] == None:
            continue
        add_on = list(map(lambda x: x.lower(), keys['short_desc']))

        title_listwise = keys['title'].lower().split(' ')
        #sometimes title or add_on is not defined
        if title_listwise == ['']:
            continue
        pos_seq = '_'.join(list(map(getPos,title_listwise))).lower()
        print (title_listwise, pos_seq, add_on)
        desc_first = True
        for desc_word in add_on:
            if not desc_word in dict_statistics.keys():
                dict_statistics[desc_word] = {}
                for i in range(len(title_listwise)):
                    position = ''
                    if i == 0:
                        position = 'pre'
                    elif i == len(title_listwise) - 1:
                        position = 'suf'
                    else:
                        position = 'mid'
                    dict_index = position + '_' + title_listwise[i] #SUF_run
                    dict_statistics[desc_word][dict_index] = {}
                    ## pos_local : local cnt and pos_global : global cnt left.
                    # V_local
                    # dict_stat['chase']['SUF_run'] = {'VMNN_local': 10, 'VMNN_global':20}
            for i in range(len(title_listwise)):
                position = ''
                if i == 0:
                    position = 'pre'
                elif i == len(title_listwise) - 1:
                    position = 'suf'
                else:
                    position = 'mid'
                cnt_index = (desc_word + '_' + position + '_' + title_listwise[i]).lower()
                #cnt_statistics - local
                #cnt_statistics[chase_SUF_run] = {'pos_seqs': cnt}
                if cnt_index not in cnt_statistics.keys():
                    cnt_statistics[cnt_index] = {}
                if pos_seq not in cnt_statistics[cnt_index].keys():
                    cnt_statistics[cnt_index][pos_seq] = 0
                cnt_statistics[cnt_index][pos_seq] = cnt_statistics[cnt_index][pos_seq]+1

                # cnt_statistics - global
                # cnt_statistics[SUF_run] = {'pos_seqs': cnt}
                if desc_first:
                    cnt_index = (position + '_' + title_listwise[i]).lower()
                    if cnt_index not in cnt_statistics.keys():
                        cnt_statistics[cnt_index] = {}
                    if pos_seq not in cnt_statistics[cnt_index].keys():
                        cnt_statistics[cnt_index][pos_seq] = 0
                    cnt_statistics[cnt_index][pos_seq] = cnt_statistics[cnt_index][pos_seq] + 1
            desc_first = False

    for desc_word in dict_statistics.keys():
        for pattern_key in dict_statistics[desc_word].keys():
            desc_word = desc_word.lower()
            pattern_key = pattern_key.lower()
            print (desc_word, pattern_key)
            local_pos_seqs = cnt_statistics[desc_word + '_' + pattern_key].keys()
            global_pos_seqs = cnt_statistics[pattern_key].keys()
            for local_pos in local_pos_seqs:
                print (local_pos)
                local_pos_index = local_pos + '_local'
                dict_statistics[desc_word][pattern_key][local_pos_index] = cnt_statistics[desc_word+'_'+pattern_key][local_pos]
            for global_pos in global_pos_seqs:
                global_pos_index = global_pos + '_global'
                dict_statistics[desc_word][pattern_key][global_pos_index] = cnt_statistics[pattern_key][global_pos]

    return dict_statistics
#for test
#l_title = clear_parser(testfile_list,stereotype,stereotype_2)

def sectiondata_save_json(datafiles_dir, savefile_name,stereotype, stereotype_2):
    testfile_list = select_section(datafiles_dir, 'arcade')
    total_dict = clear_parser(testfile_list,stereotype,stereotype_2)
    make_stat(total_dict)
    with open(savefile_name+'.json', 'w') as fp:
        json.dump(make_stat(total_dict), fp)

#for test
if __name__=='__main__':
    datafiles_dir='database_crawling'
    #testfile_list = select_section(datafiles_dir, 'arcade')
    #print(len(clear_parser(testfile_list,stereotype,stereotype_2)))
    #print(clear_parser(testfile_list,stereotype,stereotype_2))
    sectiondata_save_json(datafiles_dir, 'data_arcade', stereotype, stereotype_2)
