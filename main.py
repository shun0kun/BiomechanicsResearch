from hopping_analysis import HoppingAnalysis
import numpy
import matplotlib.pyplot as plt

speed = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

indir = "../data/"
infile = [f"forward_{x}mps.csv" for x in ["0.0", "0.5", "1.0", "1.5", "2.0", "2.5", "3.0"]] + [f"inplace_{x}.csv" for x in ["1.2Hz", "1.5Hz", "1.8Hz", "PF", "2.8Hz", "3.6Hz"]]
inpath = [indir + x for x in infile]
dir = "../result/"
outdirs = [dir + x.removesuffix(".csv") + "/" for x in infile]

a = []

for i, f in enumerate(inpath):
	a.append(HoppingAnalysis(f, "../data/mass.csv"))

a[1].invalidate_hops(40)
a[2].invalidate_hops(38)
a[4].invalidate_hops([0, 36, 37, 38])
a[5].invalidate_hops(range(25, 46))
a[6].invalidate_hops(range(0, 3))
a[6].invalidate_hops(range(21, 48))

# for i in range(len(a)):
# 	a[i].export_analysis(outdirs[i])

freqs = [x.freq_mean for x in a[0:7]]
# ここから
coef = numpy.polyfit(speed, freqs, 1)
fit = numpy.poly1d(coef)
x_fit = numpy.linspace(min(speed), max(speed), 100)
y_fit = fit(x_fit)
# ここまで理解する！
plt.figure()
plt.scatter(speed, freqs, color="black", s=10)
plt.plot(x_fit, y_fit, color="black", alpha=1.0, linewidth=1.0)
plt.xlabel("Speed [m/s]")
plt.ylabel("Hopping Frequency [Hz]")
plt.title("The Relationship of Hopping Frequency and Speed")
plt.savefig(dir + "freq-speed.png", dpi=300)
plt.close()

ks = [x.vstiffness_mean / 1000.0 for x in a[0:7]]
coef = numpy.polyfit(speed, ks, 2)
fit = numpy.poly1d(coef)
x_fit = numpy.linspace(min(speed), max(speed), 100)
y_fit = fit(x_fit)
plt.figure()
plt.scatter(speed, ks, color="black", s=10)
plt.plot(x_fit, y_fit, color="black", alpha=1.0, linewidth=1.0)
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.xlabel("Speed [m/s]")
plt.ylabel("Vertical Stiffness [kN/m]")
plt.title("The Relationship of Vertical Stiffness and Speed")
plt.savefig(dir + "vstiffness-speed.png", dpi=300)
plt.close()

freqs = [x.freq_mean for x in a[10:13]]
ks = [x.vstiffness_mean / 1000.0 for x in a[10:13]]
coef = numpy.polyfit(freqs, ks, 1)
fit = numpy.poly1d(coef)
x_fit = numpy.linspace(min(freqs), max(freqs), 100)
y_fit = fit(x_fit)
plt.figure()
plt.scatter(freqs, ks, color="black", s=10)
plt.plot(x_fit, y_fit, color="black", alpha=1.0, linewidth=1.0)
plt.xlim(left=0)
plt.ylim(bottom=0)
plt.xticks([0, 1, 2, 3, 4])
plt.yticks([0, 10, 20, 30, 40, 50, 60])
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.xlabel("Frequency [Hz]")
plt.ylabel("Vertical Stiffness [kN/m]")
plt.title("The Relationship of Vertical Stiffness and Hopping Frequency")
plt.savefig(dir + "vstiffness-freq.png", dpi=300)
plt.close()

freqs = [x.freq_mean for x in a[10:13]]
gcts = [x.gct_mean for x in a[10:13]]
coef = numpy.polyfit(freqs, gcts, 1)
fit = numpy.poly1d(coef)
x_fit = numpy.linspace(min(freqs), max(freqs), 100)
y_fit = fit(x_fit)
plt.scatter(freqs, gcts, color="black", s=10)
plt.plot(x_fit, y_fit, color="black", alpha=1.0, linewidth=1.0)
plt.xticks([0, 1, 2, 3, 4])
plt.yticks([0.0, 0.1, 0.2, 0.3, 0.4])
plt.xlim(left=0)
plt.ylim(bottom=0)
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.xlabel("Hopping Frequency [Hz]")
plt.ylabel("GCT [s]")
plt.title("The Relationship of GCT and Hopping Frequency")
plt.savefig(dir + "gct-freq.png", dpi=300)
plt.close()

n_points = 101
bw = a[0].mass * 9.81
list_vdisp_norm_mean = [[sum(x.vdisp_norm[i] for x in y.hops if x.is_valid) / y.n_valid_hops for i in range(n_points)] for y in a[7:13]]
list_vgrf_norm_mean = [[sum(x.vgrf_norm[i] for x in y.hops if x.is_valid) / y.n_valid_hops / bw for i in range(n_points)] for y in a[7:13]]
offsets = [0.88, 0.15, 0.07, 0.05, 0.035, list_vdisp_norm_mean[4][0] - list_vdisp_norm_mean[4][-1] + 0.001]
txts = ["1.2", "1.5", "1.8", "P.F.", "2.8", "3.6"]
plt.figure()
for vdisp, vgrf, offset, txt in zip(list_vdisp_norm_mean, list_vgrf_norm_mean, offsets, txts):
	i_bottom = vdisp.index(max(vdisp))
	plt.plot([x + offset for x in vdisp[i_bottom:]], vgrf[i_bottom:], color="black", alpha=1.0, linewidth=0.5)
	plt.plot([x + offset for x in vdisp[0:i_bottom + 1]], vgrf[0:i_bottom + 1], color="black", alpha=1.0, linewidth=1.0)
	plt.text(vdisp[i_bottom] - 0.01 + offset, max(vgrf) + 0.2, txt, fontsize=8)
plt.xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
plt.yticks([0, 1, 2, 3, 4, 5, 6, 7])
plt.xlim(left=0.0)
plt.ylim(bottom=0)
plt.tick_params(axis='x', labelbottom=False)
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.xlabel("Vertical Displacement [m]", labelpad=10)
plt.ylabel("vGRF [BW]")
plt.title("Vertical GRF-Displacement Relationship")
plt.savefig(dir + "F-x-freq.png", dpi=300)
plt.close()
