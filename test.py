import hopping_analysis as ha
import matplotlib.pyplot as plt

a = ha.HoppingAnalysis("../data/inplace_PF.csv", "../data/mass.csv")

hop = a.hops[0]
bw = a.mass * 9.81
vgrf_bw = [x / bw for x in hop.vgrf]
plt.plot(hop.time, vgrf_bw, color="black", linewidth=1.0, alpha=1.0)
plt.plot([hop.time[i] for i in range(len(hop.time)) if hop.vgrf[i] >= bw], [x for x in vgrf_bw if x >= 1], color="#0177BD", linewidth=1.0, alpha=1.0)
plt.xlabel("Time [s]")
plt.ylabel("vGRF [BW]")
plt.savefig("F-t.png")

