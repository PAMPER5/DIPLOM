import nltk
import numpy as np

from nltk.tokenize import word_tokenize
from nltk.stem.snowball import RussianStemmer

stemmer = RussianStemmer()

def tokenize_russian(sentence):
    return word_tokenize(sentence, language='russian')

def stem(word):
    return stemmer.stem(word)

def bag_of_words(tokenized_sentence, all_words):
    tokenized_sentence = [stem(w) for w in tokenized_sentence]

    bag = np.zeros(len(all_words), dtype=np.float32)
    for idx, w in enumerate(all_words):
        if w in tokenized_sentence:
            bag[idx] = 1.0

    return bag
