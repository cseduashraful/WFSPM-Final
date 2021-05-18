#!/usr/bin/python
# -*- coding: utf-8 -*-
#author: Tianming Lu
#adapted by: Nicolas Rangeon
#Weighted Adaptation (IUA, WSPAN, WFSPM) by: Md. Ashraful Islam

import argparse
from decimal import *
import pickle23


def getStat(fileName, prefix):
    f = open(fileName, "r")
    thrs = []
    algs = []
    res = {}
    if f.mode == "r":
        contents = f.readlines()
        for line in contents:
            tokens = line.split()
            if tokens[0]==prefix:
                #print(tokens)
                if tokens[1] not in algs:
                    algs.append(tokens[1])
                    res[tokens[1]] = {}
                if tokens[2] not in thrs:
                    thrs.append(tokens[2])

                vals = []
                for i in range (3,len(tokens)):
                    #print(tokens[i])
                    if tokens[i]!='#':
                        vals.append(Decimal(tokens[i]))
                res[tokens[1]][tokens[2]] = vals


    #print(algs)
    #print(thrs)
    #print(res)
    stats = [algs, thrs, res]
    return stats




if __name__ == '__main__':
    ap = argparse.ArgumentParser()

    ap.add_argument("-l", "--log", required=True, help="Dataset Path")
    ap.add_argument("-p", "--prefix", required=True, help="")


    args = vars(ap.parse_args())
    log = args['log']
    prefix = args['prefix']
    stats = getStat(log,prefix)
    outputfilePickle = "output/" +prefix+ ".pickle"
    with open(outputfilePickle, 'wb') as f:
        pickle.dump(stats, f)
    #print(stats)
    #print(stats[2]['wfspm']['0.09'])





