import  argparse
import utility.utils as util

sequenceCount = 0

seqLens = []
avgSeqLen = 0

itemsetLens = []
avgItemsetLen = 0

itemOccurrences = []
avgItemOccurrence = 0

itemSupports = []
avgItemSupport = 0

#weight file properties
MaxW = 0
avgLMaxW =  0
weights = []
avgWeight = 0

#graphs
#size wise sequence count vs sequence size

#weight_range vs occureence (alread draw)

#python dstat.py -d data/synthetic.txt -w data/posskewed.txt
item_support = {}
item_occurrence = {}



if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--data", required=True, help="Dataset Path")
    ap.add_argument("-w", "--weight", required=True, help="")
    args = vars(ap.parse_args())
    fileName = args['data']
    wfileName = args['weight']


    weight_dict, MaxW = util.read_weight(wfileName)
    sequences, lmaxW_dict = util.read_data(fileName, weight_dict)
    maxItemsetCount = 0

    for seqTuple in sequences:
        sequence, sid, lmaxW = seqTuple
#        print(sid)
        sequenceCount += 1
        length = len(sequence)
        avgLMaxW += lmaxW
        for itemset in sequence:
            itemsetLens.append(len(itemset))

            for item in itemset:
                if item not in item_occurrence:
                    item_occurrence[item] = 1
                    item_support[item] = [sid]
                else:
                    item_occurrence[item] += 1
                    if sid not in item_support[item]:
                        item_support[item].append(sid)



        seqLens.append(length)
        if length>maxItemsetCount:
            maxItemsetCount = length

        avgSeqLen += length
        #print('{}:{}:{}'.format(sid,lmaxW,sequence))


    avgSeqLen = avgSeqLen / sequenceCount
    avgItemsetLen = sum(itemsetLens)/len(itemsetLens)
    tsmw = avgLMaxW
    avgLMaxW = tsmw/sequenceCount

    w=0
    occ=0
    sup = 0
    uniqueItems = 0
    for k,v in item_occurrence.items():
        uniqueItems += 1
        sup += len(item_support[item])
        w += weight_dict[k]*v
        occ += v
    avgItemWeight = w/occ
    avgItemSupport = sup/uniqueItems


    print('Number of sequences: {}'.format(sequenceCount))
    print('average number of itemsets per transaction: {}'.format(avgSeqLen))
    print('Maximum number of itemset in a single sequence: {}'.format(maxItemsetCount))
    print('average itemset length: {}'.format(avgItemsetLen))
    print('Unique Items: {}'.format(uniqueItems))

    print("MaxW: {}".format(MaxW))
    print("tsmw: {}".format(tsmw))
    print("Average LMaxW: {}".format(avgLMaxW))
    print("Average item weight: {}".format(avgItemWeight))
    print("Average item support: {}".format(avgItemSupport))

