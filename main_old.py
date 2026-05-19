import csv
import matplotlib.pyplot as plt
from time_normalize import time_normalize

TIME_COL = 0
FZ_COL = 23

time = []
fz = []
hops = []

# load data (time, fz)
with open("../data/inplace_PF.csv", encoding="cp932") as f:
	reader = csv.reader(f)
	for i, row in enumerate(reader):
		if i < 13:
			continue
		time.append(float(row[TIME_COL]))
		fz.append(float(row[FZ_COL]))

# create hops data (hops)
threshold = 10
is_contact = []
for i in range(len(time)):
	if fz[i] > threshold:
		is_contact.append(True)
	else:
		is_contact.append(False)
time_hop = []
fz_hop = []
i = 0
while is_contact[i] == True:
	i += 1
while is_contact[i] == False:
	i += 1
while i < len(is_contact) and is_contact[i] == True:
	time_hop.append(time[i])
	fz_hop.append(fz[i])
	i += 1

for i in range(len(time_hop) - 1, -1, -1):
	time_hop[i] = time_hop[i] - time_hop[0]

g = 9.8
dt = time_hop[1] - time_hop[0]
m = 720 / 9.8
a = []
v = [0] * len(time_hop)
d_hop = [0]
for i in range(len(time_hop)):
	a.append((fz_hop[i] - m * g) / m)

i_max = fz_hop.index(max(fz_hop))
v[i_max] = 0
for i in range(i_max, len(time_hop) - 1):
	v[i + 1] = v[i] + a[i] * dt
for i in range(i_max, 0, -1):
	v[i - 1] = v[i] - a[i - 1] * dt
for i in range(len(time_hop) - 1):
	d_hop.append(d_hop[i] + v[i] * dt)

t_norm, f_norm = time_normalize(time_hop, fz_hop)
_, d_norm = time_normalize(time_hop, d_hop)

# create F-t graph (F-t.png)
plt.figure()
plt.plot(time_hop, fz_hop)
plt.xlabel("Time [s]")
plt.ylabel("vGRF [N]")
plt.title("F-t curve")
plt.savefig("../figures/F-t.png", dpi=300)
plt.close()

# create F-x graph (F-x.png)
plt.figure()
plt.plot([-x for x in d_hop], fz_hop)
plt.xlabel("Vertical displacement [m]")
plt.ylabel("vGRF [N]")
plt.title("F-x curve")
plt.savefig("../figures/F-x.png", dpi=300)
plt.close()

# create normalized F-t graph (F-t_normalized.png)
plt.figure()
plt.plot([x * 100 for x in t_norm], [x / 720 for x in f_norm])
plt.xlabel("Hop cycle [%]")
plt.ylabel("vGRF [BW]")
plt.title("F-t curve (normalized)")
plt.savefig("../figures/F-t_normalized.png", dpi=300)
plt.close()

# createnormalized F-x graph (F-x_normalized.png)
plt.figure()
plt.plot([-x for x in d_norm], [x / 720 for x in f_norm])
plt.xlabel("Vertical displacement [m]")
plt.ylabel("vGRF [BW]")
plt.title("F-x curve (normalized)")
plt.savefig("../figures/F-x_normalized.png", dpi=300)
plt.close()