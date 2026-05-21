import csv
import matplotlib.pyplot as plt

THRESHOLD = 10
time = []
vgrf = []
filtered_vgrf = []

with open("../data/inplace_PF.csv", encoding="cp932") as f:
	reader = csv.reader(f)
	for i, row in enumerate(reader):
		if i < 13:
			continue
		time.append(float(row[0]))
		vgrf.append(float(row[23]))

n = len(time)

for i in range(n):
	if vgrf[i] > THRESHOLD:
		filtered_vgrf.append(vgrf[i])
	else:
		filtered_vgrf.append(0)
i = 0
while i < n and filtered_vgrf[i] > 0:
	filtered_vgrf[i] = 0
	i += 1
i = n - 1
while i >= 0 and filtered_vgrf[i] > 0:
	filtered_vgrf[i] = 0
	i -= 1

plt.figure()
plt.plot(time, vgrf)
plt.xlabel("Time [s]")
plt.ylabel("vGRF [N]")
plt.title("F-t")
plt.savefig("fig.png")
plt.close()

plt.figure()
plt.plot(time, filtered_vgrf)
plt.xlabel("Time [s]")
plt.ylabel("Filtered vGRF [N]")
plt.title("F-t_filtered")
plt.savefig("fig_filtered.png")
plt.close()