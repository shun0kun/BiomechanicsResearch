import csv
import matplotlib.pyplot as plt

class Hop:
	def __init__(self, time: list[float], vgrf: list[float]) -> None:
		self.time = time
		self.vgrf = vgrf
		self.time_norm: list[float] = []
		self.vgrf_norm: list[float] = []
		self.vdisp_norm: list[float] = []
		self._compute_vdisp()
		self._time_normalize()

	def _compute_vdisp(self) -> None:
		self.vdisp: list[float] = []

	def _time_normalize(self) -> None:
		N_POINTS = 101
		phase_origin = []
		phase_target = []
		for i in range(len(self.time)):
			phase_origin.append((self.time[i] - self.time[0]) / (self.time[-1] - self.time[0]))
		for i in range(N_POINTS):
			phase_target.append(i / (N_POINTS - 1))
		self.time_norm = phase_target
		i = 0
		j = 0
		while i < N_POINTS:
			while j < len(phase_origin) - 1 and phase_origin[j + 1] < phase_target[i]:
				j += 1
			x = self.vgrf[j] + (phase_target[i] - phase_origin[j]) * (self.vgrf[j + 1] - self.vgrf[j]) / (phase_origin[j + 1] - phase_origin[j])
			self.vgrf_norm.append(x)
			i += 1

class HoppingAnalysis:
	def __init__(self, filepath: str) -> None:
		self.filepath = filepath
		self.mass = 720 / 9.81
		self.hops: list[Hop] = []
		self._extract_hops()

	def _extract_hops(self) -> None:
		TIME_COL = 0
		VGRF_COL = 23
		THRESHOLD = 40
		time = []
		vgrf = []
		filtered_vgrf = []
		with open(self.filepath, encoding="cp932") as f:
			reader = csv.reader(f)
			for i, row in enumerate(reader):
				if i < 13:
					continue
				time.append(float(row[TIME_COL]))
				vgrf.append(float(row[VGRF_COL]))
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

		i = 0
		while i < n:
			while i < n and filtered_vgrf[i] == 0:
				i += 1
			left = i - 1
			while i < n and filtered_vgrf[i] > 0:
				i += 1
			right = i
			if left != right:
				self.hops.append(Hop(time[left:right + 1], filtered_vgrf[left:right + 1]))

	def save_hops_plots(self, output_path: str = "F-t.png") -> None:
		plt.figure()
		for hop in self.hops:
			plt.plot([x * 100 for x in hop.time_norm], [x / (self.mass * 9.81) for x in hop.vgrf_norm])
		plt.xlabel("Hop cycle [%]")
		plt.ylabel("vGRF [BW]")
		plt.title("F-t curve")
		plt.savefig(output_path, dpi=300)
		plt.close()
