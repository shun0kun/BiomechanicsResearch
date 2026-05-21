from HoppinfAnalysis import HoppingAnalysis

indir = "../data/"
outdir = "../figures/"

speed = ["0.0", "0.5", "1.0", "1.5", "2.0", "2.5", "3.0"]
freq = ["1.2", "1.5", "2.8", "3.6"]

inpath = [indir + "forward_" + x + "mps.csv" for x in speed] + [indir + "inplace_" + x + "Hz.csv" for x in freq]
outpath = [outdir + "F-t_" + x + "mps.png" for x in speed] + [outdir + "F-t_" + x + "Hz.png" for x in freq] + [outdir + "F-t_PF.png"]

for x, y in zip(inpath, outpath):
	h = HoppingAnalysis(x)
	h.save_hops_plots(y)

# h = HoppingAnalysis(inpath[5])
# h.save_hops_plots(outpath[5])
