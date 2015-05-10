#!/usr/bin/env python3
import os
import re
import sys
import jctconv

os.chdir(os.path.dirname(os.path.abspath(__file__)))

i_class = '[いきしちにひみり]'
e_class = '[えけせてねへめれ]'
u_class = '[うくすつぬふむる]'
u_to_i = {
    'う': 'い',
    'く': 'き',
    'す': 'し',
    'つ': 'ち',
    'ぬ': 'に',
    'ふ': 'ひ',
    'む': 'み',
    'る': 'り',
}



onyomis = {}
onyomi_tsv = open('onyomi.tsv', 'r')
for line in onyomi_tsv:
    fields = line.strip().split("\t")
    kanji = fields[0]

    if len(fields) < 2:
        onyomis[kanji] = []
        continue
        
    ons = fields[1].split()
    ons = [jctconv.kata2hira(on) for on in ons]
    # should we use this information (bound readings) somehow?
    ons = [on.replace('-', '') for on in ons]
    ons = [on.strip() for on in ons]
    ons = set(ons)
    onyomis[kanji] = ons

kunyomis = {}
kunyomi_tsv = open('kunyomi.tsv', 'r')
for line in kunyomi_tsv:
    fields = line.strip().split("\t")
    kanji = fields[0]

    if len(fields) < 2:
        kunyomis[kanji] = []
        continue

    kuns = fields[1].split()

    # 'たべ.る' → 'たべ'
    # 'はな.し' → 'はな', 'はなし' (because of "hidden okurigana")
    # 'い.きる' → 'い', 'いき'
    # 'はな.す' → 'はな', 'はなし'
    for idx, kun in enumerate(kuns):
        dot = kun.find('.')
        if dot != -1:
            base = kun[0:dot]
            kuns[idx] = base

            # alternative-lenght (old-style) bases that 'hide' more kana
            # e.g. 挙る is あ.げる
            # but in 挙句 it's あげ
            i = -2
            while kun[i] != '.':
                base = kun[0:i+1]
                kuns.append(base.replace('.', ''))
                i -= 1

            lastchar = kun[-1]
            if re.match(i_class, lastchar):
                kuns.append(kun.replace('.', ''))
            elif re.match(u_class, lastchar):
                # godan is always a possibility
                kun2 = kun[:-1] + u_to_i[lastchar]
                kuns.append(kun2.replace('.', ''))

                # perhaps it may be ichidan?
                if (kun[-1] == 'る' and
                    (re.match(e_class, kun[-2]) or re.match(i_class, kun[-2]))):
                    kun3 = kun[:-1]
                    kuns.append(kun3.replace('.', ''))
                    # sys.stderr.write(kanji + ": " + kun3 + "\n")

    # should we use this information (bound readings) somehow?
    kuns = [kun.replace('-', '') for kun in kuns]
    kuns = [kun.strip() for kun in kuns]
    kuns = set(kuns)
    kunyomis[kanji] = kuns

print('ONYOMI = ' + repr(onyomis))
print('KUNYOMI = ' + repr(kunyomis))
