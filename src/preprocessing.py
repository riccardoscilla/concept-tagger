def read_corpus(corpus_file):
    return [line.strip().split() for line in open(corpus_file, 'r')]

def read_corpus_conll(corpus_file, fs="\t"):
    featn = None  # number of features for consistency check
    sents = []  # list to hold words list sequences
    words = []  # list to hold feature tuples

    for line in open(corpus_file):
        line = line.strip()
        if len(line.strip()) > 0:
            feats = tuple(line.strip().split(fs))
            if not featn:
                featn = len(feats)
            elif featn != len(feats) and len(feats) != 0:
                raise ValueError("Unexpected number of columns {} ({})".format(len(feats), featn))

            words.append(feats[:2])
		
        else:
            if len(words) > 0:
                sents.append(words)
                words = []
    return sents

import re

def parse_iob(t):
    m = re.match(r'^([^-]*)-(.*)$', t)
    return m.groups() if m else (t, None)

def get_chunks(corpus_file, fs="\t", otag="O"):
    sents = read_corpus_conll(corpus_file, fs=fs)
    return set([parse_iob(token[-1])[1] for sent in sents for token in sent if token[-1] != otag])

def get_column(corpus, column=-1):
    return [[word[column] for word in sent] for sent in corpus]

def compute_frequency_list(corpus):
    frequencies = {}
    for sent in corpus:
        for token in sent:
            frequencies[token] = frequencies.setdefault(token, 0) + 1
    return frequencies

def cutoff(corpus, tf_min=2, tf_max=float('inf')):
    frequencies = compute_frequency_list(corpus)
    trn_in = set([token for token, frequency in frequencies.items() if tf_max >= frequency >= tf_min])
    trn_out = set([token for token, frequency in frequencies.items() if tf_min > frequency >= 0])
    return trn_in, trn_out

def corpus_replace_oov(corpus, lexicon, unk='<unk>'):
    return [[token if token in lexicon else unk for token in sent] for sent in corpus]
