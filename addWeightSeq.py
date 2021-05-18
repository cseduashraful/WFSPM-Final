# imports
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import stats
from scipy.stats import skewnorm
import argparse
import os
import pickle

class Item_freq_pair:
    def __init__(self, item, freq):
        self.item = item
        self.freq = freq
        self.weight = -1

    def addToList(self, lst):
        found = 0
        for obj in lst:
            if self.item == obj.item:
                found = 1
                obj.freq = obj.freq + 1
                # print(obj)
                break

        if found == 0:
            lst.append(self)
            # print(self)

        return lst

    def addWeight(self, weight):
        self.weight = weight

    def __str__(self):
        return "(" + self.item + "," + str(self.freq) + ")"


def print_item_freq_list(lst):
    for obj in lst:
        print("{} {}".format(obj.item, obj.freq))


def get_frequency(fileName):
    sequences = []
    f = open(fileName, "r")
    lst = []

    if f.mode == "r":
        contents = f.readlines()
        l=len(contents)
        print("Calculating item frequency\nNumber of sequences: {}".format(l))
        i =0
        p = 1
        for line in contents:
            i = i+1
            if(p<=(i/l)*100):
                print("{}% ".format(p))
                p = p + 1
            sequence = []
            # print(line)
            tokens = line.split()
            itemset = []

            for token in tokens:
                # print(token)
                if token == "-2":
                    sequences.append(sequence)
                elif token == "-1":
                    sequence.append(itemset)
                    itemset = []
                else:
                    itemset.append(token)
                    obj = Item_freq_pair(token, 1)
                    obj.addToList(lst)
                    # print_item_freq_list(lst)
        # print(sequences)
        sorted_list = sorted(lst, key=lambda p: p.freq)
        return sorted_list


def getAvg(lst):
    cnt = 0
    s = 0
    for item in lst:
        s = s + item
        cnt = cnt + 1
    return s / cnt


def getTotalItemCount(lst):
    cnt = 0
    for obj in lst:
        cnt = cnt + obj.freq
    return cnt


def getAvgWeightFrom(start_index, end_index, freq, side, sorted_weights, rnd):
    fromi = 0
    toi = 0
    s =0
    if side == 1:
        nsi = start_index + freq
        fromi=start_index
        toi=nsi-1
        while start_index < nsi:
            s = s + sorted_weights[start_index]
            start_index = start_index + 1
        start_index = nsi
    else:
        nei = end_index - freq
        toi = end_index
        fromi=nei+1
        while end_index > nei:
            s = s + sorted_weights[end_index]
            end_index = end_index - 1
        end_index = nei

    weight = round(s / freq, rnd)
    i = fromi
    while i<=toi:
        sorted_weights[i] = weight
        i = i + 1

    return weight, start_index, end_index


def assignWeight(lst, sorted_weights, rnd):
    weights = []
    wlist = []
    side = 1
    start_index = 0
    end_index = len(sorted_weights) - 1
    l = len(lst)
    print("lst length: {}".format(l))
    i = 0
    p = 1
    print("i = ")
    for obj in lst:
        #lst[i] = 0 #clear mem
        print(i, end =" ")
        i = i+1
        weight, start_index, end_index = getAvgWeightFrom(start_index, end_index, obj.freq, side, sorted_weights,rnd)

        side = side * -1
        #for i in range(0, obj.freq):
        #k = obj.freq
        #weights.append((weight,k))

        obj.addWeight(weight)
        wlist.append(obj)
    return wlist, sorted_weights


def generateWeight(fileName, distribution):
    #print("here1")
    if distribution == "normal":
        mu = float(input("mean: "))
        sigma = float(input("standard deviation: "))
        #tmp_weights = np.random.normal(mu, sigma, getTotalItemCount(lst))
    elif distribution == "skewnorm":
        mu = float(input("loc: "))
        sigma = float(input("skewness: "))
        scale = float(input("scale: "))
        #tmp_weights = skewnorm.rvs(a=sigma, loc=mu, scale=scale, size=getTotalItemCount(lst))
    else:
        exit(1)
    #print("here2")

    # tmp_weights = np.random.normal(mu, sigma, getTotalItemCount(lst))

    rnd = int(input("Round upto: "))

    lst = get_frequency(fileName)
    print_item_freq_list(lst)

    if distribution == "normal":
        weights = np.random.normal(mu, sigma, getTotalItemCount(lst))
    elif distribution == "skewnorm":
        weights = skewnorm.rvs(a=sigma, loc=mu, scale=scale, size=getTotalItemCount(lst))
    else:
        exit(1)

    weights = sorted(weights, reverse=False)
    wlist, weights = assignWeight(lst, weights, rnd)

    ##    for obj in lst:
    ##        wvalues = np.random.normal(mu, sigma, obj.freq)
    ##        weight = getAvg(wvalues)
    ##        weight = round(weight, 2)
    ##        for i in range(0, obj.freq):
    ##            weights.append(weight)
    ##        obj.addWeight(weight)
    ##        wlist.append(obj)
    return wlist, weights


def writeToFile(lst, wfileName):
    weightOutputFileObject = open(wfileName, "w")
    for obj in lst:
        weightOutputFileObject.write("{} {} {}\n".format(obj.item, obj.freq, obj.weight))
    weightOutputFileObject.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", required=True, help="Dataset Path")
    ap.add_argument("-d", "--distribution", required=True, help="distribution", choices=['normal', 'skewnorm'])

    args = vars(ap.parse_args())
    fileName = args['path']
    print("{}".format(fileName))
    distribution = args['distribution']
    print("{}".format(distribution))

    head, tail = os.path.split(fileName)
    name, dot, ext = tail.partition('.')
    wfileName = head + "/weight_" + name + "_" + distribution + dot + ext
    print(wfileName)
    draw = False


    while True:
        wlist, weights = generateWeight(fileName, distribution)
        # Draw Distribution
        if draw == True:

            print("preparing distribution graphs ", end="\n")
        #weightlist = []
        #for tuple in weights:
        #    w,f = tuple
        #    for i in range(0,f):
        #        weightlist.append(w)
            n, x, _ = plt.hist(weights, bins=20, histtype=u'step')
            bin_centers = 0.5 * (x[1:] + x[:-1])
            plt.plot(bin_centers, n)
            plt.ylabel('Frequency')
            #plt.show()
            plt.savefig("data/temp.eps")
        else:
            outputfilePickle = "data/weights" + ".pickle"
            with open(outputfilePickle, 'wb') as f:
                pickle.dump(weights, f)



        satisfied = 1#int(input("satified? -->"))
        print(satisfied)
        if satisfied == 1:
            writeToFile(wlist, wfileName)
            break
