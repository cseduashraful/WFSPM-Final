#!/usr/bin/python
# -*- coding: utf-8 -*-
#author: Tianming Lu
#adapted by: Nicolas Rangeon
#Weighted Adaptation (IUA, WSPAN, WFSPM) by: Md. Ashraful Islam

import argparse
import os
from decimal import *
import time
import pickle
import resource



import utility.utils as util
import utility.globals as glb
from algo.IUA import IUA
from algo.wSpan import wSpan
from algo.wfspm import wfspm


#python main.py -d data/SIGN.txt -w data/weight_SIGN.txt -a iua -t 0.6



if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    """""
    ap.add_argument("-d", "--data", required=True, help="Dataset Path")
    ap.add_argument("-w", "--weight", required=True, help="")
    ap.add_argument("-t", "--threshold", required=True, help="Threshold %")
    ap.add_argument("-a", "--algorithm", required=True, help="wspan or iua or wfspm")
    ap.add_argument("-l", "--length", required=False, default=100, type=int, help="maximum pattern length")
    """""

    #Debug block
    ap.add_argument("-d", "--data", required=False, default="data/SIGN.txt", help="Dataset Path")
    ap.add_argument("-w", "--weight", required=False, default="data/weight_SIGN.txt", help="")
    ap.add_argument("-t", "--threshold", required=False, default=0.4, help="Threshold %")
    ap.add_argument("-a", "--algorithm", required=False, default="wfspm", help="wspan or iua or wfspm")
    ap.add_argument("-l", "--length", required=False, default=100, type=int, help="maximum pattern length")
    #ap.add_argument("-p", "--pickle", required=False, default="None", help="pickle")


    args = vars(ap.parse_args())
    fileName = args['data']
    wfileName = args['weight']
    thr = Decimal(args['threshold'])
    length = args['length']
    #print(length)

    algorithm = args['algorithm']

    start_time = time.time()


        
    weight_dict, maxW = util.read_weight(wfileName)
    candict = util.getCandict(weight_dict, algorithm)
    sequences, lmaxW_dict = util.read_data(fileName, weight_dict)
    tsmw = util.getTSMW(lmaxW_dict)
    sequences = util.sortDatasetInCanonicalOrder(sequences, candict)

    if algorithm == 'iua':
            model = IUA.train(sequences, weight_dict, lmaxW_dict, maxW, minSupport=thr, maxPatternLength=length, tsmw=tsmw)
    elif algorithm == 'wspan':
            model = wSpan.train(sequences, weight_dict, maxW, minSupport=thr, maxPatternLength=length, tsmw=tsmw)

    elif algorithm == 'wfspm':
            model = wfspm.train(sequences, weight_dict, lmaxW_dict, maxW, minSupport=thr, maxPatternLength=length, tsmw=tsmw)
    else:
        raise Exception("Invalid algorithm. Valid options are wspan/iua/wfspm")

    result = model.freqSequences().collect()
    end_time = time.time()
    timespan = (end_time - start_time)
    #for fs in result:
    #        print('{}, {}, {}, {}, {}'.format(fs.sequence,fs.freq, fs.weight, fs.wsup, fs.pruncon))
    #print("Required time is {} seconds".format(timespan))
    #print("Candidate: {} frequent: {}".format(glb.canCount,glb.fCount))

    head, tail = os.path.split(fileName)
    name,dot, ext = tail.partition('.')

    whead, wtail = os.path.split(wfileName)
    wname,dot,ext = wtail.partition('.')

    name = name+"-"+wname

    outputfile = "output/"+algorithm+"/"+name+"_"+str(thr)+".txt"
    outputfilePickle = "output/"+algorithm+"/pickle/"+name+"_"+str(thr)+".pickle"
    #print(outputfilePickle)
    obj = open(outputfile, "w")
    for fs in result:
            obj.write('{}, {}, {}, {}, {}\n'.format(fs.sequence,fs.freq, fs.weight, fs.wsup, fs.pruncon))
    obj.write("Required time is {} seconds\n".format(timespan))
    obj.write("Candidate: {} frequent: {}".format(glb.canCount,glb.fCount))
    obj.close()
    with open(outputfilePickle, 'wb') as f:
        pickle.dump(result, f)

    row = name +","+algorithm+","+str(thr)+","+str(length)+"," +str(round(timespan,2))+","+str(glb.canCount)+","+str(glb.fCount)+"\n"
    summaryFile = "output/summary.csv"
    obj = open(summaryFile,"a")
    obj.write(row)
    obj.close()
    reqMem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    #print('{} {} {} {} {} {} {}'.format(name, algorithm, thr, glb.fCount, glb.canCount, reqMem, timespan))

    if algorithm=='wfspm':
        print('{} {} {} {} {} {} {} {} # {} {}'.format(name, algorithm, thr, glb.fCount, glb.canCount, reqMem, timespan, glb.pCount, glb.maxpwsCount, glb.SatisfiedmaxpwsCount))
    else:
        print('{} {} {} {} {} {} {} {}'.format(name, algorithm, thr, glb.fCount, glb.canCount, reqMem, timespan, glb.pCount))
