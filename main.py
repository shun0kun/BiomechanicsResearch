from hopping_analysis import HoppingAnalysis
import matplotlib.pyplot as plt

dirpath = "../figs"

a = HoppingAnalysis("../data/inplace_PF.csv", "../data/mass.csv")
a.analyze(dirpath)
