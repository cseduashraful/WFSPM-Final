#For Graph Drawings

class Attrs:
    def __init__(self, alg):
        self.alg=alg
        self.runtimes = []
        self.thrs = []
        self.candidates = []
        self.frequents = []
        self.generatedSeq = []
        self.memory = []
        if alg == 'wfspm':
            self.maxpwsCounts = []
            self.SatisfiedmaxpwsCounts = []

    def _print(self):
        print("Thrs: ")
        print(self.thrs)
        print("Runtimes: ")
        print(self.runtimes)
        print("Total generated sequences: ")
        print(self.generatedSeq)
        print("candidates: ")
        print(self.candidates)
        print("frequents: ")
        print(self.frequents)
        print("memory")
        print(self.memory)
        if self.alg == 'wfspm':
            print("MaxPWS Counts")
            print(self.maxpwsCounts)
            print("Satisfied MaxPWS Counts")
            print(self.SatisfiedmaxpwsCounts)


class Results:
    def __init__(self, t, a):
        self.thresholds = t
        self.holder = {}
        for algorithm in a:
            self.holder[algorithm] = Attrs(algorithm)


    def _print(self):
        for k,v in self.holder.items():
            print("..............{}..........".format(k))
            v._print()

