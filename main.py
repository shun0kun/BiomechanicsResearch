from hopping_analysis import HoppingAnalysis
import matplotlib.pyplot as plt
import os

dirpath = "../figs/"

h = HoppingAnalysis("../data/inplace_PF.csv")
plt.figure()
plt.plot(h.hops[0].time, h.hops[0].vgrf)
plt.xlabel("Time [s]")
plt.ylabel("vGRF [F]")
plt.title("F-t graph")
os.makedirs("../figs/", exist_ok=True)
plt.savefig(dirpath + "F-t.png", dpi=300)
plt.close()
