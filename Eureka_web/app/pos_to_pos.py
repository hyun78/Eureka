from nltk.corpus import wordnet as wn

def lcs(str1, str2):
    n = len(str1)
    m = len(str2)
    dp = [[0 for i in range(m + 1)] for j in range(n + 1)]
    for i in range(n):
        for j in range(m):
            dp[i + 1][j + 1] = max(dp[i][j + 1], dp[i + 1][j])
            if str1[i] == str2[j]:
                dp[i + 1][j + 1] = dp[i][j] + 1
    return dp[n][m]

def verb_to_noun(verb):
    verb = verb.lower()
    synsets = []
    res = set()

    for lemma in wn.lemmas(verb):
        for related_form in lemma.derivationally_related_forms():
            for synset in wn.synsets(related_form.name(), pos=wn.NOUN):
                synsets.append(synset)

    names = []
    comp_len = min(len(verb), 2)
    for synset in synsets:
        for lemma in synset.lemmas():
            for name in lemma.name().split('_'):
                names.append(name.lower())
    for name in names:
        if name[0] != verb[0]: continue
        if lcs(name, verb) >= comp_len:
        #if name[:comp_len] == verb[:comp_len]:
            res.add(name)

    return sorted(list(res))

def adv_to_adj(adv):
    adv = adv.lower()
    res = set()
    for lemma in wn.lemmas(adv):
        try:
            posword = lemma.pertainyms()[0].name()
            res.add(posword)
        except: pass
    return sorted(list(res))

if __name__ == '__main__':
    advs = ['Financially', 'Willfully', 'Abruptly', 'Endlessly',
             'Firmly', 'Delightfully', 'Quickly', 'Lightly', 'Eternally',
             'Delicately', 'Wearily', 'Sorrowfully', 'Beautifully', 'Truthfully', 'Fast', 'Fatally']

    verbs = ['go', 'infest', 'do', 'sing', 'run', 'select', 'die', 'report', 'tell', 'kill']

    advs.sort()
    verbs.sort()

    print("adv -> adj")
    for adv in advs: print(str(adv) + "\t->", adv_to_adj(adv))
    print()

    print("verb -> noun")
    for verb in verbs: print(str(verb) + "\t->", verb_to_noun(verb))