from decimal import *
import utility.globals as glb
import argparse

def zerolistmaker(n):
    listofzeros = [0] * n
    return listofzeros


def getMax(a, b):
        if a>b:
                return a
        return b


def printSequences(sequences):
        for sequence in sequences:
                print(sequence)


def findLasteOccurrenceWFSPM(laste, s, weight_dict, PLACE_HOLDER):
        indices = []
        unique_items = []
        leftVec = []

        indx = 0

        if PLACE_HOLDER in s[0]:
                indices.append(indx)
                for item in s[0][1:]:
                        if item not in unique_items:
                                unique_items.append(item)
                                leftVec.append(len(s) - 1)
        for itemset in s:
                is_prefix = True
                for item in laste:
                        if item not in itemset:
                                is_prefix = False
                                break
                if is_prefix == True and len(laste) > 0:
                        index = itemset.index(laste[-1])
                        if index < len(itemset) - 1:
                                for item in itemset[index + 1:]:
                                        if item not in unique_items:
                                                unique_items.append(item)
                                                leftVec.append(len(s) - 1 - indx)

                        indices.append(indx)
                indx = indx + 1
        return indices, unique_items, leftVec


def findLasteOccurrence(laste, s, PLACE_HOLDER):
        indices = []
        unique_items = []
        indx = 0
        for itemset in s:
                is_prefix = True
                for item in laste:
                        if item not in itemset:
                                is_prefix = False
                                break
                if is_prefix == True and len(laste) > 0:
                        index = itemset.index(laste[-1])
                        if index < len(itemset) - 1:
                                for item in itemset[index + 1:]:
                                        if item not in unique_items:
                                                unique_items.append(item)
                                        
                        indices.append(indx)
                indx =  indx + 1

        if PLACE_HOLDER in s[0]:
                 for item in s[0][1:]:
                        if item not in unique_items:
                                unique_items.append(item)
        
        return indices, unique_items






def sortItemsetSetInCanocicalOrder(itemset, candict):
        i = 0
        l = len(itemset)
        while i < l:
                j = 0
                while j < l-i-1:
                        item1 = itemset[j]
                        item2 = itemset[j+1]
                        if candict[item1] > candict[item2]:
                                tmp = itemset[j]
                                itemset[j] = itemset[j+1]
                                itemset[j+1] = tmp
                        j = j+1
                i = i+1
        return itemset



def sortSequenceInCanocicalOrder(sequence, candict):
        i = 0
        for itemset in sequence:
                itemset = sortItemsetSetInCanocicalOrder(itemset, candict)
                sequence[i] = itemset
                i = i+1
        return sequence

def sortDatasetInCanonicalOrder(dataset, candict):
        i = 0
        for seq_t in dataset:
                sequence, sid, lmaxW = seq_t
                sequence = sortSequenceInCanocicalOrder(sequence, candict)
                dataset[i] = (sequence, sid, lmaxW)
                i = i+1
        return dataset


def getLmaxW(s, weight_dict):
        lmaxW = -1
        for itemset in s:
                for item in itemset:
                        if item != '_':
                                if weight_dict[item] > lmaxW:
                                        lmaxW = weight_dict[item]
        return lmaxW

def getStringFromList(lst, separator):
        string = ''
        for ls in lst:
                string =  string + str(ls) + separator
        return string

def getItemsetWeight(itemset, weight_dict):
        cnt = 0
        weight = 0
        for item in itemset:
            weight = weight + weight_dict[item]
            cnt = cnt + 1
        return weight/cnt

def getWeight(pattern, weight_dict):
        weight = 0
        cnt = 0
        for itemset in pattern.sequence:
            #print(itemset)
            weight =  weight + getItemsetWeight(itemset, weight_dict)
            cnt =  cnt + 1
        return weight/cnt

def getWeightWFSPM(pattern, weight_dict):
        weight = 0
        cnt = 0
        for itemset in pattern.sequence:
            #print(itemset)
            weight =  weight + getItemsetWeight(itemset, weight_dict)
            cnt =  cnt + 1
        return weight/cnt, weight, cnt

def read_weight(fileName):
        weight_dict = {}
        maxW = -1
        f = open(fileName, "r")
        if f.mode == "r":
                contents = f.readlines()
                for line in contents:
                        tokens = line.split()
                        w = Decimal(tokens[2])
                        if maxW < w:
                            maxW = w
                        weight_dict.update({tokens[0]: w})
                #print(weight_dict)
                #print("MaxW is {}".format(maxW))
                return weight_dict, maxW


def read_data(fileName, weight_dict):
        sequences = []
        lmaxW_dict = {}
        sid = -1
        f = open(fileName, "r")
        p = 400000
        i = 0
        if f.mode == "r":
                contents = f.readlines()
                for line in contents:
                        i =i + 1
                        if i>=p:
                                break
                        sequence = []
                        sid = sid + 1
                        lmaxW = -1
                        #print(line)
                        tokens = line.split()
                        itemset = []
                        
                        for token in tokens:
                                #print(token)
                                if token == "-2":
                                        sequenceTuple = (sequence, sid, lmaxW)
                                        sequences.append(sequenceTuple)
                                        #sequences.append(sequence)
                                        lmaxW_dict.update({sid:lmaxW})
                                elif token == "-1":
                                        sequence.append(itemset)
                                        itemset = []
                                else:
                                        itemset.append(token)
                                        #print(weight_dict[token])
                                        if weight_dict[token] > lmaxW:
                                                lmaxW = weight_dict[token]
                #print(sequences)
                return sequences, lmaxW_dict

def getTSMW(lmaxW_dict):
        tsmw = 0
        for k,v in lmaxW_dict.items():
                tsmw += v
        return tsmw


def getCandict(weight_dict, algo):
        #for wspan and wfub set algo = 1 else set algo = 2
        candict = {}
        if algo == 'iua' or algo == 'wspan':
                indx = 0
                for k,v in weight_dict.items():
                        candict.update({k:indx})
                        indx = indx+1
        else:
                weight_list = sorted(weight_dict.items(), key = lambda x : x[1], reverse=True)
                #print(weight_list)
                indx = 0
                for k,v in weight_list:
                        candict.update({k:indx})
                        indx = indx+1
        return candict

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')