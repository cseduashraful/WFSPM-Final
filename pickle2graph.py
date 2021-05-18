import argparse
from utility.utils import str2bool
import os
import pickle
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from decimal import Decimal

def sortedKeys(keys):
    l = len(keys)
    #print(keys)
    for i in range(0, l):
        for j in range(0,l-1-i):
            if Decimal(keys[j]) > Decimal(keys[j+1]):
                tmp = keys[j]
                keys[j] = keys[j+1]
                keys[j+1] = tmp
    #print(keys)
    return keys


def getthresholds(obj):
    keys = sortedKeys([x for x in obj.keys()])
    #print(keys)
    #keys = sortedKeys(obj.keys())
    ls = [Decimal(x.strip(' "')) for x in keys]
    return ls


def getlist(obj, index):
    ls = []
    keys = sortedKeys([x for x in obj.keys()])
    for key in keys:
        ls.append(obj[key][index])
    return ls

def balanceLength(tomod, ref):
    while(len(ref)>len(tomod)):
        tomod.insert(0,0)
    return tomod


def memdrawGraph2(thrs, iua, wfspm, prefix, save):
    fig, ax = plt.subplots()

    labels = []
    for thr in thrs:
        labels.append(str(thr))
    y = np.arange(len(labels))
    width=0.35

    #rects1 = ax.barh(y + width, wspan, width, label='WSpan', color='r')
    rects2 = ax.barh(y+width/2, iua, width, label='IUA', color='g')
    rects3 = ax.barh(y - width/2, wfspm, width, label='WFSPM', color='b')

    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    #ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Memory in KB')
    ax.set_title('Memory Requirement '+prefix)
    ax.legend()

    fig.tight_layout()

    if save:
        plt.savefig("output/graphs/" + prefix + "_memory.eps")
    else:
        plt.show()



def memdrawGraph(stats, prefix, save):
    thrs = sortedKeys(stats[1])

    wfspm = getlist(stats[2]['wfspm'], 2)
    iua = balanceLength(getlist(stats[2]['iua'], 2),wfspm)

    if 'wspan' in stats[0]:
        wspan = balanceLength(getlist(stats[2]['wspan'], 2), wfspm)

        fig, ax = plt.subplots()

        labels = []
        for thr in thrs:
            labels.append(str(thr))
        y = np.arange(len(labels))
        width=0.25

        rects1 = ax.barh(y + width, wspan, width, label='WSpan', color='r')
        rects2 = ax.barh(y, iua, width, label='IUA', color='g')
        rects3 = ax.barh(y - width, wfspm, width, label='WFSPM', color='b')

        ax.set_yticks(y)
        ax.set_yticklabels(labels)
        #ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel('Memory in KB')
        ax.set_title('Memory Requirement '+prefix)
        ax.legend()

        fig.tight_layout()

        if save:
            plt.savefig("output/graphs/" + prefix + "_memory.eps")
        else:
            plt.show()

    else:
        memdrawGraph2(thrs, iua, wfspm, prefix, save)


def searchSpace(stats, prefix, save):
    labels = []
    for thr in stats.thresholds:
        labels.append(str(thr))
    x = np.arange(len(labels))  # the label locations



    fig, ax = plt.subplots()
    if 'wspan' in stats.holder.keys():
        width = 0.25  # the width of the bars
        rects1 = ax.bar(x - width, stats.holder['wspan'].generatedSeq, width, label='WSpan', color='r')
        rects2 = ax.bar(x, stats.holder['iua'].generatedSeq, width, label='IUA', color='g')
        rects3 = ax.bar(x + width, stats.holder['wfspm'].generatedSeq, width, label='WFSPM', color='b')
    else:
        width = 0.35  # the width of the bars
        if len(stats.holder['iua'].generatedSeq)<len(stats.holder['wfspm'].generatedSeq):
            a = [0]
            a.extend(stats.holder['iua'].generatedSeq)
            print(stats.holder['iua'].generatedSeq)
            print(a)
            print(stats.holder['wfspm'].generatedSeq)
            stats.holder['iua'].generatedSeq = a
        rects2 = ax.bar(x - width/2, stats.holder['iua'].generatedSeq, width, label='IUA', color='g')
        rects3 = ax.bar(x + width/2, stats.holder['wfspm'].generatedSeq, width, label='WFSPM', color='b')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Generated Sequence Count')
    ax.set_title('Search Space '+prefix)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 4),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    #autolabel(rects1)
    #autolabel(rects2)
    #autolabel(rects3)

    fig.tight_layout()

    if save:
        plt.savefig("output/graphs/"+prefix+"_searchspace.eps")
    else:
        plt.show()



def thrVSruntime(stats, prefix, save):
    fig, ax = plt.subplots()
    #print(getthresholds(stats[2]['wspan']))
    #print(getlist(stats[2]['wspan'],3))
    if 'wspan' in stats[0]:
        ax.plot(getthresholds(stats[2]['wspan']),getlist(stats[2]['wspan'],3), label="WSpan", linestyle=":", color="r", marker='o')
    ax.plot(getthresholds(stats[2]['iua']), getlist(stats[2]['iua'],3), label="IUA", linestyle="--", color="g", marker='v')
    ax.plot(getthresholds(stats[2]['wfspm']), getlist(stats[2]['wfspm'],3), label="WFSPM", linestyle="-", color="b", marker='D')

    ax.legend()
    ax.grid()
    ax.set(xlabel='threshold', ylabel='time (seconds)',
           title='Execution Time '+prefix)

    plt.tight_layout()
    if save:
        plt.savefig("output/graphs/"+prefix+"_ExecutionTimeVsThresholds.eps")
    else:
        plt.show()


def pruningMeasurePrecision(stats, prefix, save):
    def divide(a, b):
        div = [ai / bi for ai, bi in zip(a, b)]
        return div

    iua = divide(getlist(stats[2]['iua'],0), getlist(stats[2]['iua'],1))
    wfspm = divide(getlist(stats[2]['wfspm'],0), getlist(stats[2]['wfspm'],1))

    fig, ax = plt.subplots()
    if 'wspan' in stats[0]:
        wspan = divide(getlist(stats[2]['wspan'],0), getlist(stats[2]['wspan'],1))
        ax.plot(getthresholds(stats[2]['wspan']), wspan, label="WSpan", linestyle=":", color="r", marker='o')
    ax.plot(getthresholds(stats[2]['iua']), iua, label="IUA", linestyle="--", color="g", marker='v')
    ax.plot(getthresholds(stats[2]['wfspm']), wfspm, label="WFSPM", linestyle="-", color="b", marker='D')

    ax.legend()
    ax.grid()
    ax.set(xlabel='threshold', ylabel='Pruning Measure Precision',
           title='Pruning Measure Precision '+prefix)

    plt.tight_layout()
    if save:
        plt.savefig("output/graphs/"+prefix+"_PrecisionVsThresholds.eps")
    else:
        plt.show()







"""
 python pickle2graph.py -p pickle_file_path -g prefix -s True/False
"""



if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--pickle", required=True, help="Pickle File Path")
    ap.add_argument("-g", "--graphPrefix", required=False, default="default", help="Graph Prefix")
    ap.add_argument("-s", "--save", required=False, type=str2bool, default=False,  help="Graph Prefix")

    args = vars(ap.parse_args())

    pickle_in = open(args['pickle'], "rb")
    stats = pickle.load(pickle_in)
    thrVSruntime(stats, args['graphPrefix'], args['save'])
    pruningMeasurePrecision(stats, args['graphPrefix'], args['save'])
    memdrawGraph(stats, args['graphPrefix'], args['save'])
    #print(stats)