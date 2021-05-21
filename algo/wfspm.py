import utility.utils as util
import utility.globals as glb


class wfspm:

    def __init__(self, sequences, weight_dict, lmaxw_dict, maxW, minSupport=0.1, maxPatternLength=10, tsmw=1):

        # minSupport = minSupport * len(sequences)
        self.PLACE_HOLDER = '_'

        freqSequences = self._prefixSpan(
            self.SequencePattern([], None, maxPatternLength, self.PLACE_HOLDER),
            sequences, weight_dict, lmaxw_dict, maxW, minSupport, maxPatternLength, tsmw)

        self.freqSeqs = wfspm.FreqSequences(freqSequences)

    @staticmethod
    def train(sequences, weight_dict, lmaxw_dict, maxW, minSupport=0.1, maxPatternLength=10, tsmw=1):
        return wfspm(sequences, weight_dict, lmaxw_dict, maxW, minSupport, maxPatternLength, tsmw)

    def freqSequences(self):
        return self.freqSeqs

    class FreqSequences:
        def __init__(self, fs):
            self.fs = fs

        def collect(self):
            return self.fs

    class SequencePattern:
        def __init__(self, sequence, support, maxPatternLength, place_holder):
            self.place_holder = place_holder
            self.sequence = []
            for s in sequence:
                self.sequence.append(list(s))
            self.freq = support
            self.weight = 0
            self.wsup = 0
            self.pruncon = 0

        def append(self, p):
            if p.sequence[0][0] == self.place_holder:
                first_e = p.sequence[0]
                first_e.remove(self.place_holder)
                self.sequence[-1].extend(first_e)
                self.sequence.extend(p.sequence[1:])
            else:
                self.sequence.extend(p.sequence)
                if self.freq is None:
                    self.freq = p.freq
            self.freq = min(self.freq, p.freq)

        def __str__(self):
            sstr = 'Sequence: ' + util.getStringFromList(self.sequence, ' ') + " Freq: " + str(
                self.freq) + " weight: " + str(self.weight)
            return sstr + " wsup: " + str(self.wsup) + " pruncon: " + str(self.pruncon)

    def _checkPatternLengths(self, pattern, maxPatternLength):
        for s in pattern.sequence:
            if len(s) > maxPatternLength:
                return False
        return True

    def _prefixSpan(self, pattern, S, weight_dict, lmaxw_dict, maxW, threshold, maxPatternLength, tsmw):
        patterns = []
        if self._checkPatternLengths(pattern, maxPatternLength):
            f_list = self._frequent_items(S, pattern, weight_dict, threshold, maxPatternLength)

            for i in f_list:
                p = self.SequencePattern(pattern.sequence, pattern.freq, maxPatternLength, self.PLACE_HOLDER)

                p.append(i)

                # p.supportSetLeftPair = i.supportSetLeftPair
                p.weight, tweight, cnt = util.getWeightWFSPM(p, weight_dict)
                p.wsup = (p.freq * p.weight)/tsmw
                # p.pruncon = getMaxPWS(i.supportSetLeftPair, tweight, cnt)
                p.pruncon = -1  # getMaxPWSv2(tweight, cnt, exWeight, exWeightFreq, left_dict)

                # print(p)
                # print(len(p.sequence))

                wSpanCond = (p.freq * maxW)/tsmw
                glb.pCount += 1
                if self._checkPatternLengths(pattern, maxPatternLength):
                    if p.wsup >= threshold:
                        glb.fCount = glb.fCount + 1
                        patterns.append(p)
                        glb.canCount = glb.canCount + 1
                        p_S = self._build_projected_database(S, weight_dict, p)
                        p_patterns = self._prefixSpan(p, p_S, weight_dict, lmaxw_dict, maxW, threshold,
                                                      maxPatternLength, tsmw)
                        patterns.extend(p_patterns)
                    elif wSpanCond >= threshold:
                        p.pruncon = getMaxPWSv2(tweight, cnt, i.exWeight, i.exWeightFreq, i.left_dict)/tsmw
                        glb.maxpwsCount += 1
                        if p.pruncon >= threshold:
                            glb.SatisfiedmaxpwsCount += 1
                            glb.canCount = glb.canCount + 1
                            p_S = self._build_projected_database(S, weight_dict, p)
                            #pickle fump S to i.pickle
                            p_patterns = self._prefixSpan(p, p_S, weight_dict, lmaxw_dict, maxW, threshold,
                                                          maxPatternLength, tsmw)
                            #load i.pickle to S

                            patterns.extend(p_patterns)

        return patterns

    def _frequent_items(self, S, pattern, weight_dict, threshold, maxPatternLength):
        items = {}
        _items = {}

        exWeight = {}
        _exWeight = {}

        exWeightFreq = {}
        _exWeightFreq = {}

        left_dict = {}
        _left_dict = {}

        #maxLeft = glb.maxL # maxPatternLength - len(pattern.sequence)

        # supportSetLeftPair = {}
        # _supportSetLeftPair = {}

        # prunCon = {}
        # _prunCon = {}

        f_list = []
        if S is None or len(S) == 0:
            return []

        if len(pattern.sequence) != 0:
            last_e = pattern.sequence[-1]
        else:
            last_e = []
        ##                print(S)
        for s_t in S:

            s, sid, lmaxW = s_t

            # class 1 and 2
            indices, unique_items, leftVec = util.findLasteOccurrenceWFSPM(last_e, s, weight_dict, self.PLACE_HOLDER)
            i = 0
            for item in unique_items:
                if item in _left_dict:
                    _items[item] += 1
                    # _prunCon[item] += lmaxW
                    # _supportSetLeftPair[item].append((sid,leftVec[i], lmaxW))
                    # MaxPWS
                    if leftVec[i] in _exWeight[item]:
                        _exWeight[item][leftVec[i]] += lmaxW
                        _exWeightFreq[item][leftVec[i]] += 1
                    else:
                        _exWeight[item][leftVec[i]] = lmaxW
                        _exWeightFreq[item][leftVec[i]] = 1
                    _left_dict[item] = util.getMax(_left_dict[item], leftVec[i])

                else:
                    _items[item] = 1
                    # _prunCon[item] = lmaxW
                    # _supportSetLeftPair[item] = [(sid,leftVec[i], lmaxW)]
                    # MaxPWS
                    _exWeight[item] = {}#util.zerolistmaker(maxLeft)
                    _exWeight[item][leftVec[i]] = lmaxW
                    _exWeightFreq[item] = {}#util.zerolistmaker(maxLeft)
                    _exWeightFreq[item][leftVec[i]] = 1
                    _left_dict[item] = leftVec[i]

                i = i + 1

            # class 2
            if self.PLACE_HOLDER in s[0]:
                s = s[1:]

            # class 3
            counted = []
            # leftVec2 = []
            i = 0
            for element in s:
                for item in element:
                    if item not in counted:
                        counted.append(item)
                        if item in left_dict:
                            items[item] += 1
                            # prunCon[item] += lmaxW
                            # supportSetLeftPair[item].append((sid,len(s)-i-1, lmaxW))
                            # MaxPWS
                            leftVec2 = len(s) - i - 1
                            #if leftVec2>glb.maxL:
                            #    print(leftVec2)
                            if leftVec2  in exWeight[item]:
                                exWeight[item][leftVec2] += lmaxW
                                exWeightFreq[item][leftVec2] += 1
                            else:
                                exWeight[item][leftVec2] = lmaxW
                                exWeightFreq[item][leftVec2] = 1

                            #exWeight[item][leftVec2] += lmaxW
                            #exWeightFreq[item][leftVec2] += 1
                            left_dict[item] = util.getMax(left_dict[item], leftVec2)
                        else:
                            items[item] = 1
                            # prunCon[item] = lmaxW
                            # supportSetLeftPair[item] = [(sid,len(s)-i-1, lmaxW)]
                            # MaxPWS

                            leftVec2 = len(s) - i - 1
                            #if leftVec2>glb.maxL:
                            #    print(leftVec2)
                            exWeight[item] = {}#util.zerolistmaker(maxLeft)
                            ##                                                        print(exWeight[item])
                            ##                                                        print(leftVec2)
                            exWeight[item][leftVec2] = lmaxW
                            exWeightFreq[item] = {}#util.zerolistmaker(maxLeft)
                            exWeightFreq[item][leftVec2] = 1
                            left_dict[item] = leftVec2  # getMax(left_dict[item], leftVec2)
                i = i + 1

        for k, v in _items.items():
            ##                        if v>= threshold:
            ##                        print("{}, {}, {}".format(k, v, threshold))
            tmp = self.SequencePattern([[self.PLACE_HOLDER, k]], v, maxPatternLength, self.PLACE_HOLDER)
            # tmp.pruncon = _prunCon[k]
            # tmp.supportSetLeftPair = _supportSetLeftPair[k]
            # MaxPWS
            tmp.exWeight = _exWeight[k]
            tmp.exWeightFreq = _exWeightFreq[k]
            tmp.left_dict = _left_dict[k]

            # print(tmp.pruncon)
            f_list.append(tmp)

        for k, v in items.items():
            ##                        print("{}, {}, {}".format(k, v, threshold))
            tmp = self.SequencePattern([[k]], v, maxPatternLength, self.PLACE_HOLDER)
            # tmp.pruncon = prunCon[k]
            # tmp.supportSetLeftPair = supportSetLeftPair[k]
            # MaxPWS
            tmp.exWeight = exWeight[k]
            tmp.exWeightFreq = exWeightFreq[k]
            tmp.left_dict = left_dict[k]
            f_list.append(tmp)

            # todo: can be optimised by including the following line in the 2 previous lines
        f_list = [i for i in f_list if self._checkPatternLengths(i, maxPatternLength)]

        # sorted_list = sorted(f_list, key=lambda p: p.freq)
        # return sorted_list
        return f_list

    def _build_projected_database(self, S, weight_dict, pattern):
        """
        suppose S is projected database base on pattern's prefix,
        so we only need to use the last element in pattern to
        build projected database
        """
        p_S = []
        p_sid = 0

        last_e = pattern.sequence[-1]
        last_item = last_e[-1]
        for s_t in S:
            p_s = []
            s, sid, lmaxW = s_t
            for element in s:
                is_prefix = False
                if self.PLACE_HOLDER in element:
                    if last_item in element and len(pattern.sequence[-1]) > 1:
                        is_prefix = True
                else:
                    is_prefix = True
                    for item in last_e:
                        if item not in element:
                            is_prefix = False
                            break

                if is_prefix:
                    e_index = s.index(element)
                    i_index = element.index(last_item)
                    if i_index == len(element) - 1:
                        p_s = s[e_index + 1:]
                    else:
                        p_s = s[e_index:]
                        index = element.index(last_item)
                        e = element[i_index:]
                        e[0] = self.PLACE_HOLDER
                        p_s[0] = e
                    break
            if len(p_s) != 0:
                # lmaxW = getLmaxW(p_s, weight_dict)
                p_s_t = (p_s, sid, lmaxW)
                p_sid = p_sid + 1
                p_S.append(p_s_t)

        return p_S



def getMaxPWSv2(weight, cnt, exWeight, exWeightFreq, left_dict):
##        print("Maximum left is {}".format(left_dict))
##        print("weight: {}\n cnt: {}\n exWeight: {}\n exWeightFreq: {}".format(weight, cnt, exWeight, exWeightFreq))
        #i = left_dict
        maxpws = 0
        xisum = 0
        n = 0
        #unique = 0
        #print(i)
        keys =sorted(exWeight,reverse=True)
        unique = 0
        for i in keys:
            unique += 1
            xisum += exWeight[i]
            n += exWeightFreq[i]
            pws = (n * weight + i * xisum) / (cnt + i)
            if pws > maxpws:
                maxpws = pws
        #while i > 0:
        #        if exWeightFreq[i] > 0:

        #        i -= 1
        #print("({},{})".format(left_dict, unique))
        return maxpws

