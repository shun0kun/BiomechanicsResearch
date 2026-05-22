from hopping_analysis import HoppingAnalysis
import matplotlib.pyplot as plt

speed = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

indir = "../data/"
infile = [f"forward_{x}mps.csv" for x in ["0.0", "0.5", "1.0", "1.5", "2.0", "2.5", "3.0"]] + [f"inplace_{x}.csv" for x in ["1.2Hz", "1.5Hz","2.8Hz", "3.6Hz", "PF"]]
inpath = [indir + x for x in infile]
dir = "../result/"
outdirs = [dir + x.removesuffix(".csv") + "/" for x in infile]

a = []

for i, f in enumerate(inpath):
	a.append(HoppingAnalysis(f, "../data/mass.csv"))

# a[1].invalidate_hops(40)
# a[2].invalidate_hops(38)
# a[4].invalidate_hops([0, 36, 37, 38])
# a[5].invalidate_hops(range(25, 46))
# a[6].invalidate_hops(range(0, 3))
# a[6].invalidate_hops(range(21, 48))

# for i in range(len(a)):
# 	a[i].export_analysis(outdirs[i])

plt.figure()
for i in range(0, 7):
	plt.errorbar(speed[i], a[i].freq_mean, a[i].freq_se, fmt="o-", capsize=5, color="black")
plt.xlabel("Speed [m/s]")
plt.ylabel("Hopping Frequency [Hz]")
plt.title("The Relationship of Hopping Frequency and Speed")
plt.savefig(dir + "freq-speed.png", dpi=300)
plt.close()

plt.figure()
for i in range(0, 7):
	plt.errorbar(speed[i], a[i].vstiffness_mean, a[i].vstiffness_se, fmt="o-", capsize=5, color="black")
plt.xlabel("Speed [m/s]")
plt.ylabel("Vertical Stiffness [N/m]")
plt.title("The Relationship of Vertical Stiffness and Speed")
plt.savefig(dir + "vstiffness-speed.png", dpi=300)
plt.close()

plt.figure()
for i in range(7, 12):
	plt.errorbar(a[i].freq_mean, a[i].vstiffness_mean, a[i].vstiffness_se, fmt="o-", capsize=5, color="black")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Vertical Stiffness [N/m]")
plt.title("The Relationship of Vertical Stiffness and Hopping Frequency")
plt.savefig(dir + "vstiffness-freq.png", dpi=300)
plt.close()

plt.figure()
for i in range(7, 12):
	plt.errorbar(a[i].freq_mean, a[i].gct_mean, a[i].gct_se, fmt="o-", capsize=5, color="black")
plt.xlabel("Hopping Frequency [Hz]")
plt.ylabel("GCT [s]")
plt.title("The Relationship of GCT and Hopping Frequency")
plt.savefig(dir + "gct-freq.png", dpi=300)
plt.close()

