#!/usr/bin/env python3
import os
import jctconv

os.chdir(os.path.dirname(os.path.abspath(__file__)))

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
    for idx, kun in enumerate(kuns):
        dot = kun.find('.')
        if dot != -1:
            kuns[idx] = kun[0:dot]

    # should we use this information (bound readings) somehow?
    kuns = [kun.replace('-', '') for kun in kuns]
    kuns = [kun.strip() for kun in kuns]
    kuns = set(kuns)
    kunyomis[kanji] = kuns

print('ONYOMI = ' + repr(onyomis))
print('KUNYOMI = ' + repr(kunyomis))
