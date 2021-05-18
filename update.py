import pickle

pickle_in = open("output/pickle/kosarak_weight_kosarak.pickle", "rb")
stats = pickle.load(pickle_in)

#stats._print()
stats.holder['wfspm'].runtimes[0] =102993.527905941
#stats._print()
outputfilePickle = "output/pickle/kosarak_weight_kosarak2.pickle"
with open(outputfilePickle, 'wb') as f:
    pickle.dump(stats, f)