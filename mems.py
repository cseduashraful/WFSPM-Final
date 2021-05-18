import matplotlib.pyplot as plt
import numpy as np

"""
Add expected runconfigs in mem.sh and extract result from mem_log.txt to create list in this file. Sample mem.sh runconfig commands are given below:

python main.py -d data/FIFA.txt -w data/weight_FIFA.txt -a wfspm -t 0.125 >> mem_log.txt
python main.py -d data/FIFA.txt -w data/weight_FIFA.txt -a wfspm -t 0.175 >> mem_log.txt
python main.py -d data/FIFA.txt -w data/weight_FIFA.txt -a wfspm -t 0.225 >> mem_log.txt
python main.py -d data/FIFA.txt -w data/weight_FIFA.txt -a wfspm -t 0.275 >> mem_log.txt

Then make changes to drawGraph function call and run this file to generate memory graphs
"""

#Sign
#sign_thrs = [0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65]
#sign_iua_mem = [24372, 21108, 20688, 19884, 19784, 19624, 19700, 19524, 19448, 19148]
#sign_wspan_mem = [24116, 21184, 20572, 19980, 19788, 19768, 19488, 19308, 19484, 19480]
#sign_wfspm_mem = [28832, 25900, 25244, 24808, 24740, 23976, 23572, 23404, 22916, 22320]
sign_thrs = [0.05, 0.10, 0.15, 0.20, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
sign_wfspm_mem = [571352,81244,35676,27488,24636,24040,23652,23620,23112,22760]
sign_iua_mem = [616840, 83640,34048,24320,20916,20544,19700,19592,19640,19544]
sign_wspan_mem = [616860,83552,33984,24152,21012,20432,19840,19540,19592,19464]



#leviathan_thrs = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55]
#leviathan_iua_mem = [70592, 68488, 67140, 65836, 65912, 63296, 63252, 63240, 61072, 61072, 60988]
#leviathan_wspan_mem = [68512, 67144, 66276, 65068, 64992, 64004, 63816, 61860, 61836, 61820, 61860]
#leviathan_wfspm_mem = [153448, 143328, 135708, 135664, 125168, 125276, 112656, 112568, 112572, 95340, 95288]


leviathan_thrs = [0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19]
leviathan_wfspm_mem = [192664,101348,98388,96564,94120,94316,93944,90708,90796,90600]
leviathan_iua_mem = [194844,76492,70432,69532,68276,68352,67112,67224,66960,65424]
leviathan_wspan_mem = [194488,74300,68008,67192,66884,66248, 66120,66024,64892,65044]

fifa_thrs = [0.1, 0.125, 0.15, 0.175, 0.2, 0.225, 0.25, 0.275, 0.3]
fifa_wfspm_mem = [198184, 190560, 184840, 182656, 178308, 174972, 174544, 170888, 165976]
fifa_iua_mem = [177616, 159552, 155660, 154848, 153840, 153096, 151796, 151484, 149592]
fifa_wspan_mem = [177724, 158976, 156568, 155872, 154688, 154204, 154148, 152780, 152932]

#kosarak_thrs = [ 0.002,  0.003,  0.004,  0.005,  0.006,  0.007,  0.008,  0.009,  0.010,  0.011]
#kosarak_wfspm_mem = [3423120, 3036568, 3032524, 2983136, 2910000, 2909756, 2909804, 2909728, 2830304, 2547948]
#kosarak_iua_mem = [1754164, 1750368, 1749804, 1749404, 1747700, 1745328, 1744756, 1744652, 1744632, 1744264]


kosarak_thrs = [0.0014,  0.0016, 0.0018, 0.0020, 0.0022, 0.0024, 0.0026, 0.0028, 0.0030, 0.0032]
kosarak_wfspm_mem = [2249776, 2229776, (2229776+2217024)/2, 2217024, (2217024 + 2211556)/2, 2211556, (2211556+ 2210812)/2, 2210812,(2210812+ 2210272)/2, 2210272]
kosarak_iua_mem = [2218876, 2018876,(2018876+1754060)/2, 1754060, (1754060 + 1752244)/2,1752244, (1752244+ 1751000)/2,1751000, (1751000+ 1750172)/2,1750172]


synthetic_posskewed_thrs = [0.0004, 0.0005, 0.0006, 0.0007, 0.0008, 0.0009, 0.0010, 0.0011]
synthetic_posskewed_wfspm_mem = [10238932, 2306672, 1366220, 1241872, 1148240, 1119564, 722304, 493128]
synthetic_posskewed_iua_mem = [0, 2472428, 1996360, 1295772, 1174656, 1140688, 726468, 597628]

synthetic_negskewed_thrs = [0.0005, 0.0006, 0.0007, 0.0008, 0.0009, 0.0010, 0.0011, 0.0012, 0.0013]
synthetic_negskewed_wfspm_mem = [10586128, 8968084, 1476136, 1354628, 1255128, 1175040, 1134328, 1118316, 726776]
synthetic_negskewed_iua_mem = [0, 9939964,2108280,  1983004, 1319348, 1206372, 1158500, 1142056, 733456]



def drawGraph2(thrs, iua, wfspm, prefix, save):
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



def drawGraph(thrs, wspan, iua, wfspm, prefix, save):
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


#drawGraph(sign_thrs, sign_wspan_mem,sign_iua_mem, sign_wfspm_mem, "SIGN", True)
#drawGraph(leviathan_thrs, leviathan_wspan_mem,leviathan_iua_mem, leviathan_wfspm_mem, "LEVIATHAN", True)
#drawGraph(fifa_thrs, fifa_wspan_mem,fifa_iua_mem, fifa_wfspm_mem, "FIFA", True)
#drawGraph2(kosarak_thrs,kosarak_iua_mem, kosarak_wfspm_mem, "kosarak", True)
#drawGraph2(synthetic_posskewed_thrs,synthetic_posskewed_iua_mem, synthetic_posskewed_wfspm_mem, "synthetic_pos-skewed", True)
#drawGraph2(synthetic_negskewed_thrs,synthetic_negskewed_iua_mem, synthetic_negskewed_wfspm_mem, "synthetic_neg-skewed", True)
