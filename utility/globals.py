from utility.result_util import Results

canCount = 0
fCount = 0
pCount = 0
maxpwsCount = 0
SatisfiedmaxpwsCount = 0


##For evaluation.py
#sign_thrs = [0.20, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65]
sign_thrs = [0.05, 0.10, 0.15, 0.20, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]

#leviathan_thrs = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55]
leviathan_thrs = [0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19]

fifa_thrs = [0.1, 0.125, 0.15, 0.175, 0.2, 0.225, 0.25, 0.275, 0.3]
#kosarak_thrs = [ 0.002,  0.003,  0.004,  0.005,  0.006,  0.007,  0.008,  0.009,  0.010,  0.011]
kosarak_thrs = [ 0.0014, 0.0016, 0.0018, 0.0020, 0.0022, 0.0024, 0.0026, 0.0028, 0.0030, 0.0032]

synthetic_posskewed_thrs = [0.0004, 0.0005, 0.0006, 0.0007, 0.0008, 0.0009, 0.0010, 0.0011]
synthetic_negskewed_thrs = [0.0005, 0.0006, 0.0007, 0.0008, 0.0009, 0.0010, 0.0011, 0.0012, 0.0013]



thrs = kosarak_thrs
#algs = ['wfspm', 'iua', 'wspan']
algs = ['wfspm', 'iua']


stats = Results(thrs, algs)

maxL = 0
