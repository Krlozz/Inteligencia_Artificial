from scipy.spatial.distance import cosine

import math
import numpy as np

with open("words.txt", encoding='utf8') as f:
    words = dict()
    for i in range(50000):
        row = next(f).split()
        word = row[0]
        vector = np.array([float(x) for x in row[1:]])
        words[word] = vector


def distance(w1, w2):
    return cosine(w1, w2)


def closest_words(embedding):
    distances = {
        w: distance(embedding, words[w])
        for w in words
    }
    return sorted(distances, key=lambda w: distances[w])[:10]


def closest_word(embedding):
    return closest_words(embedding)[0]

#examples
# words["city"]
# distance(words["book"],words["breakfast"])
# closest_words(words["book"])[:10]
# closest_words(words["king"]-words["man"]+words["woman"])