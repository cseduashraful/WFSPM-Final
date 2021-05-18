import argparse
from utility.result_util import Results, Attrs
from utility.utils import str2bool
import os
import pickle
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

def pruningStat(stats, prefix, save, indx=0):
    def subtract(a, b):
        sub = [ai - bi for ai, bi in zip(a, b)]
        return sub
    def summation(a, b):
        sum = [ai + bi for ai, bi in zip(a, b)]
        return sum

    def func(pct, allvals):
        #print(pct)
        absolute = int(pct / 100. * np.sum(allvals))
        return "{:.1f}%\n({:d})".format(pct, absolute)

    totalP = stats.holder['wfspm'].generatedSeq
    frequents = stats.holder['wfspm'].frequents
    notFrequentButExtended = stats.holder['wfspm'].SatisfiedmaxpwsCounts
    prunedByMaxPWS = subtract(stats.holder['wfspm'].maxpwsCounts, stats.holder['wfspm'].SatisfiedmaxpwsCounts)
    earlyPruned = subtract(totalP,summation(frequents,summation(notFrequentButExtended,prunedByMaxPWS)))

    fig = plt.figure(1, figsize=(10, 4))
    chart1 = fig.add_subplot(121)
    chart1_labels = ['WSpanCond', 'MaxPWS (direct)']
    data1 = [earlyPruned[indx], prunedByMaxPWS[indx]]
    wedges, texts, autotexts = chart1.pie(data1, autopct=lambda pct: func(pct, data1),
                                      textprops=dict(color="w"))
    chart1.legend(wedges, chart1_labels, loc="upper center")

    chart1.set_title("(a) Direct MaxPWS Pruning "+prefix)

    chart2 = fig.add_subplot(122)
    chart2_labels = ['WSpanCond', 'MaxPWS (indirect)']
    data2 = [earlyPruned[indx], stats.holder['wspan'].generatedSeq[indx]-earlyPruned[indx]-frequents[indx]-notFrequentButExtended[indx]]
    wedges, texts, autotexts = chart2.pie(data2, autopct=lambda pct: func(pct, data2),
                                          textprops=dict(color="w"))
    chart2.legend(wedges, chart2_labels,loc="upper center")
    chart2.set_title("(b) Indirect MaxPWS Pruning "+prefix)

    fig.tight_layout()

    if save:
        plt.savefig("output/graphs/" + prefix + "_PruningComparison.eps")
    else:
        plt.show()

def pruningStat2(stats, prefix, save, indx=0):
    def subtract(a, b):
        sub = [ai - bi for ai, bi in zip(a, b)]
        return sub
    def summation(a, b):
        sum = [ai + bi for ai, bi in zip(a, b)]
        return sum

    def func(pct, allvals):
        absolute = int(pct / 100. * np.sum(allvals))
        gap1 = abs(allvals[0]-absolute)
        gap2 =  abs(allvals[1]-absolute)
        if gap1<gap2:
            absolute = allvals[0]
        else:
            absolute = allvals[1]
        return "{:.1f}%\n({:d})".format(pct, absolute)

    totalP = stats.holder['wfspm'].generatedSeq
    frequents = stats.holder['wfspm'].frequents
    notFrequentButExtended = stats.holder['wfspm'].SatisfiedmaxpwsCounts
    prunedByMaxPWS = subtract(stats.holder['wfspm'].maxpwsCounts, stats.holder['wfspm'].SatisfiedmaxpwsCounts)
    earlyPruned = subtract(totalP,summation(frequents,summation(notFrequentButExtended,prunedByMaxPWS)))

    fig = plt.figure(1, figsize=(5, 10))
    #gs1 = gridspec.GridSpec(5, 10)
    #gs1.update(wspace=0.025, hspace=0.05)  # set the spacing between axes.
    chart1 = fig.add_subplot(211)
    chart1_labels = ['WSpanCond', 'MaxPWS (direct)']
    data1 = [earlyPruned[indx], prunedByMaxPWS[indx]]
    wedges, texts, autotexts = chart1.pie(data1, autopct=lambda pct: func(pct, data1),
                                      textprops=dict(color="w"))
    chart1.legend(wedges, chart1_labels, loc="upper center")

    chart1.set_title("(i) Direct MaxPWS Pruning "+prefix)

    chart2 = fig.add_subplot(212)
    chart2_labels = ['WSpanCond', 'MaxPWS (indirect)']
    data2 = [earlyPruned[indx], stats.holder['wspan'].generatedSeq[indx]-earlyPruned[indx]-frequents[indx]-notFrequentButExtended[indx]]
    wedges, texts, autotexts = chart2.pie(data2, autopct=lambda pct: func(pct, data2),
                                          textprops=dict(color="w"))
    chart2.legend(wedges, chart2_labels,loc="upper center")
    chart2.set_title("(ii) Indirect MaxPWS Pruning "+prefix)

    fig.tight_layout()

    if save:
        plt.savefig("output/graphs/" + prefix + "_PruningComparison2.eps")
    else:
        plt.show()

def pruningStat3(stats, prefix, save, indx=0):
    def subtract(a, b):
        sub = [ai - bi for ai, bi in zip(a, b)]
        return sub
    def summation(a, b):
        sum = [ai + bi for ai, bi in zip(a, b)]
        return sum

    def func(pct, allvals):
        absolute = int(pct / 100. * np.sum(allvals))
        gap1 = abs(allvals[0]-absolute)
        gap2 =  abs(allvals[1]-absolute)
        if gap1<gap2:
            absolute = allvals[0]
        else:
            absolute = allvals[1]
        return "{:.4f}%\n({:d})".format(pct, absolute)

    totalP = stats.holder['wfspm'].generatedSeq
    frequents = stats.holder['wfspm'].frequents
    notFrequentButExtended = stats.holder['wfspm'].SatisfiedmaxpwsCounts
    prunedByMaxPWS = subtract(stats.holder['wfspm'].maxpwsCounts, stats.holder['wfspm'].SatisfiedmaxpwsCounts)
    earlyPruned = subtract(totalP,summation(frequents,summation(notFrequentButExtended,prunedByMaxPWS)))

    fig = plt.figure(1, figsize=(5, 5))
    #gs1 = gridspec.GridSpec(5, 10)
    #gs1.update(wspace=0.025, hspace=0.05)  # set the spacing between axes.
    chart1 = fig.add_subplot(111)
    chart1_labels = ['WSpanCond', 'MaxPWS (direct)']
    data1 = [earlyPruned[indx], prunedByMaxPWS[indx]]
    wedges, texts, autotexts = chart1.pie(data1, autopct=lambda pct: func(pct, data1),
                                      textprops=dict(color="w"))
    chart1.legend(wedges, chart1_labels, loc="upper center")

    chart1.set_title("Direct MaxPWS Pruning "+prefix)

    fig.tight_layout()

    if save:
        plt.savefig("output/graphs/" + prefix + "_PruningComparison3.eps")
    else:
        plt.show()


def wfspmPruningDistribution(stats, prefix, save):
    def subtract(a, b):
        sub = [ai - bi for ai, bi in zip(a, b)]
        return sub
    def summation(a, b):
        sum = [ai + bi for ai, bi in zip(a, b)]
        return sum

    totalP = stats.holder['wfspm'].generatedSeq
    frequents = stats.holder['wfspm'].frequents
    notFrequentButExtended = stats.holder['wfspm'].SatisfiedmaxpwsCounts
    prunedByMaxPWS = subtract(stats.holder['wfspm'].maxpwsCounts, stats.holder['wfspm'].SatisfiedmaxpwsCounts)
    earlyPruned = subtract(totalP,summation(frequents,summation(notFrequentButExtended,prunedByMaxPWS)))

    recipe = ["Frequent",
              "NF_Extended",
              "MaxPWS_pruned",
              "Early_pruned"]
    ingredients = [x for x in recipe]
    #data_1 = [frequents[0], notFrequentButExtended[0], prunedByMaxPWS[0], earlyPruned[0]]
    #data_2 = [frequents[1], notFrequentButExtended[1], prunedByMaxPWS[1], earlyPruned[1]]
    #data_3 = [frequents[2], notFrequentButExtended[2], prunedByMaxPWS[2], earlyPruned[2]]
    #data_4 = [frequents[3], notFrequentButExtended[3], prunedByMaxPWS[3], earlyPruned[3]]
    #data_5 = [frequents[4], notFrequentButExtended[4], prunedByMaxPWS[4], earlyPruned[4]]
    #data_6 = [frequents[5], notFrequentButExtended[5], prunedByMaxPWS[5], earlyPruned[5]]

    data_1 = [frequents[0], notFrequentButExtended[0], prunedByMaxPWS[0]]
    data_2 = [frequents[1], notFrequentButExtended[1], prunedByMaxPWS[1]]
    data_3 = [frequents[2], notFrequentButExtended[2], prunedByMaxPWS[2]]
    data_4 = [frequents[3], notFrequentButExtended[3], prunedByMaxPWS[3]]
    data_5 = [frequents[4], notFrequentButExtended[4], prunedByMaxPWS[4]]
    data_6 = [frequents[5], notFrequentButExtended[5], prunedByMaxPWS[5]]


    fig = plt.figure(1, figsize=(12,8))
    chart1 = fig.add_subplot(231)

    chart1.pie(data_1)
    chart1.set_title("threshold: "+str(stats.thresholds[0]))

    chart2 = fig.add_subplot(232)
    chart2.pie(data_2)
    chart2.set_title("threshold: " + str(stats.thresholds[1]))

    chart3 = fig.add_subplot(233)
    chart3.pie(data_3)
    chart3.set_title("threshold: " + str(stats.thresholds[2]))

    chart4 = fig.add_subplot(234)
    chart4.pie(data_4)
    chart4.set_title("threshold: " + str(stats.thresholds[3]))

    chart5 = fig.add_subplot(235)
    chart5.pie(data_5)
    chart5.set_title("threshold: " + str(stats.thresholds[4]))

    chart6 = fig.add_subplot(236)
    chart6.pie(data_6)
    chart6.set_title("threshold: " + str(stats.thresholds[5]))



    plt.show()


def pruningMeasurePrecision(stats, prefix, save):
    def divide(a, b):
        div = [ai / bi for ai, bi in zip(a, b)]
        return div


    iua = divide(stats.holder['iua'].frequents, stats.holder['iua'].candidates)
    wfspm = divide(stats.holder['wfspm'].frequents, stats.holder['wfspm'].candidates)
    print(stats.holder['wfspm'].frequents)
    print(stats.holder['wfspm'].candidates)

    fig, ax = plt.subplots()
    if 'wspan' in stats.holder.keys():
        wspan = divide(stats.holder['wspan'].frequents, stats.holder['wspan'].candidates)
        ax.plot(stats.holder['wspan'].thrs, wspan, label="WSpan", linestyle=":", color="r", marker='o')
    ax.plot(stats.holder['iua'].thrs, iua, label="IUA", linestyle="--", color="g", marker='v')
    ax.plot(stats.holder['wfspm'].thrs, wfspm, label="WFSPM", linestyle="-", color="b", marker='D')

    ax.legend()
    ax.grid()
    ax.set(xlabel='threshold', ylabel='Pruning Measure Precision',
           title='Pruning Measure Precision '+prefix)

    plt.tight_layout()
    if save:
        plt.savefig("output/graphs/"+prefix+"_PrecisionVsThresholds.eps")
    else:
        plt.show()



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
    if 'wspan' in stats.holder.keys():
        ax.plot(stats.holder['wspan'].thrs, stats.holder['wspan'].runtimes, label="WSpan", linestyle=":", color="r", marker='o')
    ax.plot(stats.holder['iua'].thrs, stats.holder['iua'].runtimes, label="IUA", linestyle="--", color="g", marker='v')
    ax.plot(stats.holder['wfspm'].thrs, stats.holder['wfspm'].runtimes, label="WFSPM", linestyle="-", color="b", marker='D')

    ax.legend()
    ax.grid()
    ax.set(xlabel='threshold', ylabel='time (seconds)',
           title='Execution Time '+prefix)

    plt.tight_layout()
    if save:
        plt.savefig("output/graphs/"+prefix+"_ExecutionTimeVsThresholds.eps")
    else:
        plt.show()

"""
 python graph.py -p pickle_file_path -g prefix -s True/False
"""


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--pickle", required=True, help="Pickle File Path")
    ap.add_argument("-g", "--graphPrefix", required=False, default="default", help="Graph Prefix")
    ap.add_argument("-s", "--save", required=False, type=str2bool, default=False,  help="Graph Prefix")

    args = vars(ap.parse_args())

    pickle_in = open(args['pickle'], "rb")
    stats = pickle.load(pickle_in)

    stats._print()

    if 'wspan' in stats.holder.keys():
        #pruningStat(stats, args['graphPrefix'], args['save'])
        pruningStat2(stats, args['graphPrefix'], args['save'])
    else:
        pruningStat3(stats, args['graphPrefix'], args['save'])
    thrVSruntime(stats, args['graphPrefix'], args['save'])
    searchSpace(stats, args['graphPrefix'], args['save'])
    pruningMeasurePrecision(stats, args['graphPrefix'], args['save'])
