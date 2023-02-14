import pickle
from nim import play

with open('modelo.pkl', 'rb') as archivo:
    ai = pickle.load(archivo)

play(ai, None)