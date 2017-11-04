from nltk.tag import pos_tag
from nltk.corpus import words

englishDic = dict.fromkeys(words.words(), None)

def isEnglishWord(word):
    try:
        x = englishDic[word]
        return True
    except KeyError:
        return False

def getPos(name):
    name = ''.join(e for e in name if e.isalnum() or e == ' ')
    res =  pos_tag(name.split())
    return [(str, pos) if isEnglishWord(str) else (str, 'NNP') for str, pos in res]

while True:
    str = input()
    print(getPos(str))
    print(getPos(str.lower()))