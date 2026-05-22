import csv
import matplotlib.pyplot as plt
import os
from . import utils
from .Hop import Hop

G = 9.81

class HoppingAnalysis:
	def __init__(self, filepath: str, massdata: int | float | str | None = None) -> None:
		self.filepath = filepath
		self.mass = self._resolve_mass(massdata)
		self.time, self.vgrf = self._load_hopping_data()
		self.filtered_vgrf = self._filter_vgrf()
		self.hops = self._extract_hops()

	def _resolve_mass(self, massdata: int | float | str | None) -> float:
		if isinstance(massdata, (int, float)):
			return float(massdata)
		if isinstance(massdata, str):
			return utils.estimate_mass_from_csv(massdata)
		if massdata is None:
			return utils.estimate_mass_from_csv(self.filepath)
		raise TypeError("massdata must be int, float, str, or None")

	def _load_hopping_data(self) -> tuple[list[float], list[float]]:
		time = []
		vgrf = []
		with open(self.filepath, encoding="cp932") as f:
			reader = csv.reader(f)
			for i, row in enumerate(reader):
				if i < 13:
					continue
				time.append(float(row[0]))
				vgrf.append(float(row[23]))
		return time, vgrf

	def _filter_vgrf(self) -> list[float]:
		THRESHOLD = 40.0
		filtered_vgrf = []
		for f in self.vgrf:
			if f > THRESHOLD:
				filtered_vgrf.append(f)
			else:
				filtered_vgrf.append(0.0)
		for i in range(len(filtered_vgrf)):
			if filtered_vgrf[i] == 0.0:
				break
			filtered_vgrf[i] = 0.0
		for i in range(len(filtered_vgrf) - 1, -1, -1):
			if filtered_vgrf[i] == 0.0:
				break
			filtered_vgrf[i] = 0.0
		return filtered_vgrf

	def _extract_hops(self) -> list[Hop]:
		hops = []
		is_contact = False
		left = 0
		for i in range(len(self.filtered_vgrf) - 1):
			if not is_contact and self.filtered_vgrf[i + 1] > 0.0:
				is_contact = True
				left = i
			elif is_contact and self.filtered_vgrf[i + 1] == 0.0:
				is_contact = False
				right = i + 1
				hops.append(Hop(self.mass, self.time[left:right + 1], self.filtered_vgrf[left:right + 1]))
		return hops

	def analyze(self, outdir: str = "") -> None:
		if len(outdir) > 0 and outdir[-1] != '/':
			outdir = outdir + '/'
		os.makedirs(outdir, exist_ok = True) # ""や"."のときはどうなる？

		plt.figure()
		plt.plot(self.time, self.vgrf)
		plt.xlabel("Time [s]")
		plt.ylabel("vGRF [N]")
		plt.title("Vertical GRF")
		plt.savefig(outdir + "vertical_GRF.png")
		plt.close()

		plt.figure()
		plt.plot(self.time, self.filtered_vgrf)
		plt.xlabel("Time [s]")
		plt.ylabel("vGRF [N]")
		plt.title("Vertical GRF (filtered)")
		plt.savefig(outdir + "filtered_vertical_GRF.png")
		plt.close()

		plt.figure()
		for h in self.hops:
			plt.plot([x * 100 for x in h.time_norm], [x / (h.mass * G) for x in h.vgrf_norm])
		plt.xlabel("Hop phase [%]")
		plt.ylabel("vGRF [BW]")
		plt.title("F-t graph")
		plt.savefig(outdir + "F-t.png", dpi = 300)
		plt.close()

		plt.figure()
		for h in self.hops:
			plt.plot(h.vdisp, [x / (h.mass * G) for x in h.vgrf])
		plt.xlabel("Vertical displacement [m]")
		plt.ylabel("vGRF [BW]")
		plt.title("F-x graph")		
		plt.savefig(outdir + "F-x.png", dpi = 300)	
		plt.close()
