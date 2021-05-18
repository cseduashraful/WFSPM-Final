#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Tianming Lu
# adapted by: Nicolas Rangeon
# Weighted Adaptation (IUA, WSPAN, WFSPM) by: Md. Ashraful Islam

import argparse
import os
import time
import pickle
#from memory_profiler import memory_usage


import utility.utils as util
import utility.globals as glb
from algo.IUA import IUA
from algo.wSpan import wSpan
from algo.wfspm import wfspm


#python evaluation.py -d data/LEVIATHAN.txt -w data/weight_LEVIATHAN.txt
#python main.py -d data/kosarak.txt -w data/weight_kosarak.txt -a wfspm -t 0.006 >> mem_log.txt



def evaluate(sequences, weight_dict, maxW, thr, length, tsmw, algorithm, fileName, wfileName, stats):
    glb.fCount = 0
    glb.canCount = 0
    glb.pCount = 0
    glb.maxpwsCount = 0
    glb.SatisfiedmaxpwsCount = 0
    start_time = time.time()


    if algorithm == 'iua':
        model = IUA.train(sequences, weight_dict, lmaxW_dict, maxW, minSupport=thr, maxPatternLength=length, tsmw=tsmw)
    elif algorithm == 'wspan':
        model = wSpan.train(sequences, weight_dict, maxW, minSupport=thr, maxPatternLength=length, tsmw=tsmw)

    elif algorithm == 'wfspm':
        model = wfspm.train(sequences, weight_dict, lmaxW_dict, maxW, minSupport=thr, maxPatternLength=length,
                            tsmw=tsmw)
    else:
        raise Exception("Invalid algorithm. Valid options are wspan/iua/wfspm")
    result = model.freqSequences().collect()
    end_time = time.time()
    timespan = (end_time - start_time)
    head, tail = os.path.split(fileName)
    name, dot, ext = tail.partition('.')

    whead, wtail = os.path.split(wfileName)
    wname, dot, ext = wtail.partition('.')

    name = name + "-" + wname

    outputfile = "output/" + algorithm + "/" + name + "_" + str(thr) + ".txt"

    obj = open(outputfile, "w")
    for fs in result:
        obj.write('{}, {}, {}, {}, {}\n'.format(fs.sequence, fs.freq, fs.weight, fs.wsup, fs.pruncon))
    obj.write("Required time is {} seconds\n".format(timespan))
    obj.write("Candidate: {} frequent: {}".format(glb.canCount, glb.fCount))
    obj.close()

    outputfilePickle = "output/" + algorithm + "/pickle/" + name + "_" + str(thr) + ".pickle"
    with open(outputfilePickle, 'wb') as f:
        pickle.dump(result, f)

    row = name + "," + algorithm + "," + str(thr) + "," + str(length) + "," + str(round(timespan, 2)) + "," + str(
        glb.canCount) + "," + str(glb.fCount) + "\n"
    summaryFile = "output/summary.csv"
    obj = open(summaryFile, "a")
    obj.write(row)
    obj.close()

    stats.holder[algorithm].runtimes.append(timespan)
    stats.holder[algorithm].thrs.append(thr)
    stats.holder[algorithm].frequents.append(glb.fCount)
    stats.holder[algorithm].candidates.append(glb.canCount)
    stats.holder[algorithm].generatedSeq.append(glb.pCount)
    if algorithm=='wfspm':
        stats.holder[algorithm].maxpwsCounts.append(glb.maxpwsCount)
        stats.holder[algorithm].SatisfiedmaxpwsCounts.append(glb.SatisfiedmaxpwsCount)






if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--data", required=True, help="Dataset Path")
    ap.add_argument("-w", "--weight", required=True, help="Weight File Path")
    ap.add_argument("-l", "--length", required=False, default=100, type=int, help="Maximum Pattern Length")

    args = vars(ap.parse_args())
    fileName = args['data']
    wfileName = args['weight']
    length = args['length']




    weight_dict, maxW = util.read_weight(wfileName)

    sequences, lmaxW_dict = util.read_data(fileName, weight_dict)
    tsmw = util.getTSMW(lmaxW_dict)


    head, tail = os.path.split(fileName)
    name, dot, ext = tail.partition('.')

    whead, wtail = os.path.split(wfileName)
    wname, dot, ext = wtail.partition('.')



    for algorithm in glb.algs:
        candict = util.getCandict(weight_dict, algorithm)
        sequences = util.sortDatasetInCanonicalOrder(sequences, candict)
        for thr in glb.thrs:
            comment = f'd={name} w={wname} a={algorithm} t={thr}'
            print('started:'+comment)
            #if algorithm == 'iua' and thr == 0.0005:
            #    print('skipped')
            #else:
            #    evaluate(sequences, weight_dict, maxW, thr, length, tsmw, algorithm, fileName, wfileName, glb.stats)
            evaluate(sequences, weight_dict, maxW, thr, length, tsmw, algorithm, fileName, wfileName, glb.stats)
            print('finished:'+comment)

    glb.stats._print()
    outputfilePickle = "output/pickle/" + name + "_" + wname + ".pickle"
    with open(outputfilePickle, 'wb') as f:
        pickle.dump(glb.stats, f)





