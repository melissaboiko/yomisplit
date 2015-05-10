'''Given a kanji token and its reading, try to split the reading by kanji.

TODO: suport for Unicode composing.
'''

import re

from yomisplit.yomi import ONYOMI, KUNYOMI

'''Japanese 'voicing' or daku transformations classes, including the /h/ sounds
(which changes to /b/) and the 'half-daku' (/h/ -> /p/).'''
DAKUON = {
'か' : '[かが]',
'き' : '[きぎ]',
'く' : '[くぐ]',
'け' : '[けげ]',
'こ' : '[こご]',
'さ' : '[さざ]',
'し' : '[しじ]',
'す' : '[すず]',
'せ' : '[せぜ]',
'そ' : '[そぞ]',
'た' : '[ただ]',
'ち' : '[ちぢ]',
'つ' : '[つづ]',
'て' : '[てで]',
'と' : '[とど]',
'は' : '[はばぱ]',
'ひ' : '[ひびぴ]',
'ふ' : '[ふぶぷ]',
'へ' : '[へべぺ]',
'ほ' : '[ほぼぽ]',
}

def japanese_matchreg(hiragana):
    '''Builds regexp to match hiragana strings according to Japanese phonology.

    The returned regexp tests whether another hiragana string is 'the same' as
    the one provided, including in this category derivations from Japanese
    morpho-phonological processes: sequential 'voicing' (rendaku) as well as
    gemination (sokuon).
    
    That is, it adds 'dakuten, 'handakuten, and small-tsu', so that:
        (TODO: doctest)
        
    '''
    matchreg = ''

    first = hiragana[0]
    if first in DAKUON.keys():
        matchreg += DAKUON[first]
    else:
        matchreg += first

    matchreg += hiragana[1:-1] # skips last

    if len(hiragana) > 1:
        last = hiragana[-1]
        # sokuon processing
        if last in ['つ', 'ち']:
            matchreg += '[%sっ]?' % last
        else:
            matchreg += last

    return(matchreg)

def japanese_match(hiragana1, hiragana2):
    '''True if the two hiragana strings may be derived by Japanese phonology.

    Tests whether the two hiragana strings are 'the same', including in this
    category derivations from Japanese morpho-phonological processes:
    sequential 'voicing' (rendaku) as well as gemination (sokuon).

    That is, it adds 'dakuten', 'handakuten', and 'small-tsu', so that:
        (TODO: doctest)

    Wrapper on japanese_matchreg.
    '''
    matchreg = japanese_matchreg(hiragana1)
    return(re.match(matchreg, hiragana2))
            

def yomi_matchreg(kanjistring):
    """Builds regexp that matches possible known readings of kanjistring.

    Use the regexp to match a reading later, in hiragana.  The resulting match
    will include named groups, one for each kanji.
    """
    matchreg = ''
    for kanji in kanjistring:
        matchreg += '(?P<%s>' % kanji

        found=False
        if kanji in ONYOMI.keys():
            found=True
            onregs = [japanese_matchreg(on) for on in ONYOMI[kanji]]
            matchreg += '|'.join(onregs)
        if kanji in KUNYOMI.keys():
            if found:
                matchreg += '|'
            else:
                found=True
            kunregs = [japanese_matchreg(kun) for kun in KUNYOMI[kanji]]
            matchreg += '|'.join(kunregs)
        if not found:
            raise(ValueError("No reading found for kanji: '%s'" % kanji))

        matchreg += ')'
    return matchreg

def canonical_reading(kanji, foundreading):
    """From a found reading for a kanji, find its canonical form and type.

    E.g.:
        >>> canonical_reading('花', 'ばな')
        ('はな', 'Kun')
    """


    if kanji in ONYOMI.keys():
        for creading in ONYOMI[kanji]:
            if japanese_match(creading, foundreading):
                return(creading, 'On')
    if kanji in KUNYOMI.keys():
        for creading in KUNYOMI[kanji]:
            if japanese_match(creading, foundreading):
                return(creading, 'Kun')
    else:
        raise(ValueError("Kanji not found: %s" % kanji))

    raise(ValueError("Reading '%s' not found for kanji %s" %
                     (foundreading, kanji))) 


def yomidict(kanji, reading):
    m = re.match(yomi_matchreg(kanji), reading)
    if (not m):
        raise(ValueError("Reading '%s' not found for kanji '%s'" %
                         (reading, kanji)))
    return(m.groupdict())

def yomisplit(kanjiword, reading):
    pass
