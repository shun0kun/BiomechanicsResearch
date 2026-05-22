from hopping_analysis import HoppingAnalysis
import matplotlib.pyplot as plt

dirpath = "../figs_eular/"

h = HoppingAnalysis("../data/inplace_PF.csv")
print(h.hops[0].vdisp)
# h.analyze(dirpath)
