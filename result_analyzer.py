import argparse
import pickle
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from utility.utils import str2bool
import utility.globals as glb

basedir = 'output/wfspm/pickle/'
maxPatternLength = 0

item_countVsFrequency_thrs = {}

colors = ['#8bb0ec', '#aa9ae8', '#6e22b4', '#ff6f00', '#fcbe37', '#cb4c3a', '#81d8d0', '#a3ba94', '#ea9a90', '#887960', '#f9c2cc', '#cce5e5','#8bbf8c', '#0e1a2f']

def printResultSet(result):
    for fs in result:
        print('{}, {}, {}, {}'.format(fs.sequence, fs.freq, fs.weight, fs.wsup))


def getDict():
    item_countVsFrequency = {}
    l = 1
    while l<=maxPatternLength:
        item_countVsFrequency[l] = 0
        l += 1
    return  item_countVsFrequency



def processResultSet(result):
    item_countVsFrequency = getDict()
    #print('dict received')
    for fs in result:
        l = 0
        for itemset in fs.sequence:
            for item in itemset:
                l += 1
        item_countVsFrequency[l] += 1
    return item_countVsFrequency

def setMaxPatternLength(result):
    ml = 0
    for fs in result:
        l = 0
        for itemset in fs.sequence:
            for item in itemset:
                l += 1
        if l>ml:
            ml = l
    return  ml
def drawGraph(thrs, dictionary, prefix, save):
    lengths = list(dictionary[thrs[0]].keys())
    print(lengths)
    labels = []
    for l in lengths:
        labels.append(str(l))
    x = np.arange(len(labels))  # the label locations
    fig, ax = plt.subplots()
    width=1

    #values = list(dictionary[thrs[0]].values())
    #rects1 = ax.bar(x, values, width, label='0.2', color='r')
    #values = list(dictionary[thrs[1]].values())
    #rects2 = ax.bar(x, values, width, label='0.25', color='g')

    ci = 0
    for thr in thrs:
        values = list(dictionary[thr].values())
        ax.bar(x, values, width, label=str(thr), color=colors[ci])
        ci += 1

    ax.set_xlabel('Sequence Length in Items')
    ax.set_ylabel('Number of Weighted Frequent Patterns')
    ax.set_title('Pattern Distribution '+prefix)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    fig.tight_layout()

    if save:
        plt.savefig("output/graphs/" + prefix + "_patternDistribution.eps")
    else:
        plt.show()



def drawGraph3d(thrs, dictionary, prefix, save):
    lengths = list(dictionary[thrs[0]].keys())
    print(lengths)
    labels = []
    indx =0
    thrlabels = []
    for thr in thrs:
        thrlabels.append(str(thr))
    zp = np.arange(len(thrlabels))
    zp = list(reversed(zp))
    print(zp)
    for l in lengths:
        labels.append(str(l))
    x = np.arange(len(labels))  # the label locations
    print(x)
    #fig, ax = plt.subplots()
    fig = plt.figure()
    ax = Axes3D(fig)
    width=1



    #values = list(dictionary[thrs[0]].values())
    #rects1 = ax.bar(x, values, width, label='0.2', color='r')
    #values = list(dictionary[thrs[1]].values())
    #rects2 = ax.bar(x, values, width, label='0.25', color='g')

    ci = 0
    z_max = len(thrs)
    zs = list(range(z_max, 0,-1))
    #ax.invert_xaxis()
    for thr in thrs:
        values = list(dictionary[thr].values())
        ax.bar(x, values, zs=zp[ci], zdir='y', label=str(thr), color=colors[ci])
        ci += 1

    #ax.invert_yaxis()
    ax.set_xlabel('Sequence Length in Items')
    ax.set_ylabel('Thresholds')
    ax.set_zlabel('Number of Patterns')
    ax.set_title('Pattern Distribution '+prefix)
    ax.set_xticks(x)
    a#x.set_yticks(thrs)

    ax.set_xticklabels(labels)
    #ax.legend()
    #fig.tight_layout()

    if save:
        plt.savefig("output/graphs/" + prefix + "_patternDistribution3d.eps")
    else:
        plt.show()

"""
# python result_analyzer.py -f synthetic-pos -g synthetic_pos-skewed -s True

"""




if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", required=True, help="file prefix")
    ap.add_argument("-g", "--graphPrefix", required=False, default="default", help="Graph Prefix")
    ap.add_argument("-s", "--save", required=False, type=str2bool, default=False,  help="Graph Prefix")

    args = vars(ap.parse_args())
    prefix = args['graphPrefix']
    save = args['save']
    thrs = []
    outputFilePrefix = ''

    filePrefix = args['file']
    if filePrefix == 'sign':
        thrs = glb.sign_thrs
        outputFilePrefix = 'SIGN-weight_SIGN_'
    elif filePrefix == 'leviathan':
        thrs = glb.leviathan_thrs
        outputFilePrefix = 'LEVIATHAN-weight_LEVIATHAN_'
    elif filePrefix == 'fifa':
        thrs = glb.fifa_thrs
        outputFilePrefix = 'FIFA-weight_FIFA_'
    elif filePrefix == 'kosarak':
        thrs = glb.kosarak_thrs
        outputFilePrefix = 'kosarak-weight_kosarak_'
    elif filePrefix == 'synthetic-pos':
        thrs = glb.synthetic_posskewed_thrs
        outputFilePrefix = 'synthetic-posskewed_'
    elif filePrefix == 'synthetic-neg':
        thrs = glb.synthetic_negskewed_thrs
        outputFilePrefix = 'synthetic-negskewed_'
    else:
        raise Exception("Invalid file prefix. Valid options are sign/leviathan/fifa/kosarak/synthetic-pos/synthetic-neg")

    for thr in thrs:
        fname = basedir+outputFilePrefix+str(thr)+".pickle"
        pickle_in = open(fname, "rb")
        resultset = pickle.load(pickle_in)
        #resultsets.append(resultset)
        if maxPatternLength == 0:
            maxPatternLength = setMaxPatternLength(resultset)
            print(maxPatternLength)
        k = processResultSet(resultset)
        resultset = None
        pickle_in = None
        if thr not in item_countVsFrequency_thrs.keys():
            item_countVsFrequency_thrs[thr] = k
        #print(k)
    #print(thrs[0])
    #drawGraph(thrs, item_countVsFrequency_thrs, prefix, save)


    #drawGraph3d(thrs, item_countVsFrequency_thrs, prefix, save)