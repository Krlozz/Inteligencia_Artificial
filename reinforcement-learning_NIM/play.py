import pickle
from nim import train, play

ai = train(1000000)

with open('modelo.pkl', 'wb') as archivo:
    pickle.dump(ai, archivo)