import string

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

import scipy.sparse as sparse
import numpy as np
import json
import os


# code from BIT Python (I am one of the teachers there)
def create_bag_of_words(text, idxs=None):
    text = text.lower()

    # partition into sentences and words
    sentences = sent_tokenize(text)
    words = []
    for sentence in sentences:
        sentence_words = word_tokenize(sentence)
        words.extend(sentence_words)

    # remove stop words
    stop_words = set(stopwords.words("english"))
    words = [word for word in words if word not in stop_words]

    # remove punctuation
    punctuation = set(string.punctuation)
    punctuation.add("...")
    words = [word for word in words if word not in punctuation]

    # change words to their stems
    stemmer = SnowballStemmer('english')
    words = [stemmer.stem(word) for word in words]

    # remove too short stems
    words = [word for word in words if len(word) >= 3]

    if idxs is not None:
        vec = np.zeros(len(idxs))
        for word in words:
            vec[idxs[word]] += 1
        return vec
    else:
        raise ValueError('Mapping word -> index has not been passed')


def cosine(q, A):
    return A.transpose().dot(q)


def process_query(query, low_rank=True, k=20):
    if low_rank:
        A = np.load('data/Alow.npy')
        svd_comp = np.load('data/Alowcomp.npy')
    else:
        A = sparse.load_npz('data/A.npz')

    idfs = np.load('data/idfs.npy')

    with open('data/idxs.json', 'r') as json_file:
        idxs = json.load(json_file)

    q = create_bag_of_words(query, idxs=idxs)
    # it is not neccessary, because it multiplies all the results by the constant for same
    # entry, so the sorted order is not being changed
    q = q * idfs
    q = q / np.linalg.norm(q)

    if low_rank:
        sim = A.dot(svd_comp.dot(q))
    else:
        sim = cosine(q, A)

    indices = np.argpartition(sim, sim.shape[0] - k)[-k:]
    return indices[np.argsort(sim[indices])][::-1]


def documents_iterator(indices):
    DATA_DIR = 'data'
    with open(os.path.join(DATA_DIR, 'docs.json'), 'r') as json_file:
        docs = json.load(json_file)

    links = []
    for i in indices:
        links.append(docs[i])
    return links
