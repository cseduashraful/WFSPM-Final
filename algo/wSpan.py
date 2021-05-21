import utility.utils as util
import utility.globals as glb

class wSpan:

        def __init__(self, sequences, weight_dict, maxW, minSupport=0.1, maxPatternLength=10, tsmw=1):

                #minSupport = minSupport * len(sequences)
                self.PLACE_HOLDER = '_'

                freqSequences = self._prefixSpan(
                        self.SequencePattern([], None, maxPatternLength, self.PLACE_HOLDER), 
                        sequences, weight_dict, maxW,  minSupport, maxPatternLength, tsmw)

                self.freqSeqs = wSpan.FreqSequences(freqSequences)

        @staticmethod
        def train(sequences, weight_dict, maxW,  minSupport=0.1, maxPatternLength=10, tsmw=1):
                return wSpan(sequences, weight_dict, maxW, minSupport, maxPatternLength, tsmw)

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
                        sstr = 'Sequence: ' + util.getStringFromList(self.sequence, ' ')+" Freq: "+str(self.freq)+" weight: "+str(self.weight)
                        return sstr +" wsup: "+str(self.wsup)+ " pruncon: "+str(self.pruncon)

        def _checkPatternLengths(self,pattern, maxPatternLength):
                for s in pattern.sequence:
                        if len(s)>maxPatternLength:
                                return False
                return True


        def _prefixSpan(self,pattern, S, weight_dict, maxW, threshold, maxPatternLength, tsmw):
                patterns = []
                if self._checkPatternLengths(pattern, maxPatternLength):
                        f_list = self._frequent_items(S, pattern, threshold, maxPatternLength)

                        for i in f_list:
##                                print("----start before----")
                                p = self.SequencePattern(pattern.sequence, pattern.freq, maxPatternLength, self.PLACE_HOLDER)
##                                print(p)
##                                print(i)
                                p.append(i)
                                p.weight = util.getWeight(p, weight_dict)
                                p.wsup = (p.freq * p.weight)/tsmw
##                                print(maxW)
                                p.pruncon = (p.freq * maxW)/tsmw
                                #print(p)
##                                print("----end before----")
                                glb.pCount += 1
                                if self._checkPatternLengths(pattern, maxPatternLength):
                                        if p.wsup >= threshold:
                                                glb.fCount = glb.fCount + 1
                                                patterns.append(p)
                                        #patterns.append(p)

                                if p.pruncon >= threshold:
                                        glb.canCount = glb.canCount + 1
                                        p_S = self._build_projected_database(S, p)
                                        p_patterns = self._prefixSpan(p, p_S, weight_dict, maxW, threshold, maxPatternLength, tsmw)
                                        patterns.extend(p_patterns)

                return patterns


        def _frequent_items(self, S, pattern, threshold, maxPatternLength):
                items = {}
                _items = {}
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
                        #class 1 and 2
                        #print(s)
                        indices, unique_items = util.findLasteOccurrence(last_e, s, self.PLACE_HOLDER)
                        for item in unique_items:
                                if item in _items:
                                        _items[item] += 1
                                else:
                                       _items[item] = 1
##
                        #class 2 rest
                        if self.PLACE_HOLDER in s[0]:
                                s = s[1:]

                        #class 3
                        counted = []
                        for element in s:
                                for item in element:
                                        if item not in counted:
                                                counted.append(item)
                                                #print(type(items))
                                                #print(type(item))
                                                #print(item)
                                                if item in items:
                                                        items[item] += 1
                                                else:
                                                        items[item] = 1
                                
                

                for k, v in _items.items():
##                        print("{}, {}, {}".format(k, v, threshold))
                        tmp = self.SequencePattern([[self.PLACE_HOLDER, k]], v, maxPatternLength, self.PLACE_HOLDER)
                        #print(tmp)
                        f_list.append(tmp)

                for k, v in items.items():
##                        print("{}, {}, {}".format(k, v, threshold))
                        tmp = self.SequencePattern([[k]], v, maxPatternLength, self.PLACE_HOLDER)
                        #print(tmp)
                        f_list.append(tmp)
                                
                
                f_list = [i for i in f_list if self._checkPatternLengths(i, maxPatternLength)]

                return f_list


        def _build_projected_database(self, S, pattern):
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
                                p_s_t = (p_s, sid, lmaxW)
                                p_sid = p_sid + 1
                                p_S.append(p_s_t)

                return p_S
