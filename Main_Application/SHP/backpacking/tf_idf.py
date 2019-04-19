from math import log10

stop_words = set("""
a
about
above
after
again
against
all
am
an
and
any
are
aren't
as
at
be
because
been
before
being
below
between
both
but
by
can't
cannot
could
couldn't
did
didn't
do
does
doesn't
doing
don't
down
during
each
few
for
from
further
had
hadn't
has
hasn't
have
haven't
having
he
he'd
he'll
he's
her
here
here's
hers
herself
him
himself
his
how
how's
i
i'd
i'll
i'm
i've
if
in
into
is
isn't
it
it's
its
itself
let's
me
more
most
mustn't
my
myself
no
nor
not
of
off
on
once
only
or
other
ought
our
ours
""".split())


def preprocess(doc):
    words = doc.lower().split()
    res = filter(lambda x: x not in stop_words, words)
    return list(res)


def mapWords(wordA, wordSet):
    wordDictA = dict.fromkeys(wordSet, 0)
    for word in wordA:
        wordDictA[word] += 1
    return wordDictA


def tf(wordDict, wordLength):
    tfDict = {}
    if wordLength:
        for word, count in wordDict.items():
            tfDict[word] = count / float(wordLength)
    return tfDict


def idf(docDicts):
    idfDict = dict.fromkeys(docDicts[0].keys(), 0)
    for doc in docDicts:
        for word, val in doc.items():
            if val:
                idfDict[word] += 1

    for word, val in idfDict.items():
        if (val == 0):
            continue
        idfDict[word] = log10(len(docDicts) / float(val))

    return idfDict


def tf_idf(tf_res, idf_res):
    res = {}
    for word, val in tf_res.items():
        res[word] = val * idf_res[word]
    return res


def tf_idf_process(docA, docB):
    wordA = preprocess(docA)
    wordB = preprocess(docB)
    wordSet = set(wordA).union(set(wordB))
    wordDictA = mapWords(wordA, wordSet)
    wordDictB = mapWords(wordB, wordSet)
    tfA = tf(wordDictA, len(wordA))
    tfB = tf(wordDictB, len(wordB))
    idfs = idf([wordDictA, wordDictB])
    resA = tf_idf(tfA, idfs)
    resB = tf_idf(tfB, idfs)
    return resA, resB