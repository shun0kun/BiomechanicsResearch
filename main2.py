import hopping_analysis as ha
import matplotlib.pyplot as plt

a = ha.HoppingAnalysis("../data/inplace_PF.csv")

plt.figure()
plt.plot(a.hops[0].time, a.hops[0].vgrf)
plt.xlabel("Time [s]")
plt.ylabel("vGRF [N]")
plt.savefig("example.png", dpi=200)
plt.close()
