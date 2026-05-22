import os
import csv
from collections.abc import Iterable
import numpy
import matplotlib.pyplot as plt
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
		self.n_valid_hops = len(self.hops)
		self.gct_mean, self.vgrf_max_mean, self.freq_mean, self.vstiffness_mean, self.gct_se, self.freq_se, self.vstiffness_se = self._calc_statistics()

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
	
	def validate_hops(self, ids: int | Iterable[int]) -> None:
		if isinstance(ids, int):
			ids = [ids]
		if any(i > len(self.hops) - 1 or i < 0 for i in ids):
			raise IndexError("Invalid index")
		for i in ids:
			if not self.hops[i].is_valid:
				self.hops[i].is_valid = True
				self.n_valid_hops += 1
		self._reanalize()
	
	def invalidate_hops(self, ids: int | Iterable[int]) -> None:
		if isinstance(ids, int):
			ids = [ids]
		if any(i > len(self.hops) - 1 or i < 0 for i in ids):
			raise IndexError("Invalid index")
		for i in ids:
			if self.hops[i].is_valid:
				self.hops[i].is_valid = False
				self.n_valid_hops -= 1
		self._reanalize()

	def select_hops(self, ids: int | list[int]) -> None:
		self.invalidate_hops(range(len(self.hops)))
		self.validate_hops(ids)

	def _calc_statistics(self) -> tuple[float, float, float, float, float, float, float]:
		if self.n_valid_hops >= 2:
			gct_mean = sum(h.gct for h in self.hops if h.is_valid) / self.n_valid_hops
			vgrf_max_mean = sum(h.vgrf_max for h in self.hops if h.is_valid) / self.n_valid_hops
			freq_mean = sum(h.freq for h in self.hops if h.is_valid) / self.n_valid_hops
			vstiffness_mean = sum(h.vstiffness for h in self.hops if h.is_valid) / self.n_valid_hops
			gct_se = numpy.std([h.gct for h in self.hops if h.is_valid], ddof=1) / numpy.sqrt(self.n_valid_hops)
			freq_se = numpy.std([h.freq for h in self.hops if h.is_valid], ddof=1) / numpy.sqrt(self.n_valid_hops)
			vstiffness_se = numpy.std([h.vstiffness for h in self.hops if h.is_valid], ddof=1) / numpy.sqrt(self.n_valid_hops)
		elif self.n_valid_hops == 1:
			gct_mean = self.hops[0].gct
			vgrf_max_mean = self.hops[0].vgrf_max
			freq_mean = self.hops[0].freq
			vstiffness_mean = self.hops[0].vstiffness
			gct_se = None
			freq_se = None
			vstiffness_se = None
		else:
			gct_mean = None
			vgrf_max_mean = None
			freq_mean = None
			vstiffness_mean = None
			gct_se = None
			freq_se = None
			vstiffness_se = None
		return gct_mean, vgrf_max_mean, freq_mean, vstiffness_mean, gct_se, freq_se, vstiffness_se

	def _reanalize(self) -> None:
		self.gct_mean, self.vgrf_max_mean, self.freq_mean, self.vstiffness_mean, self.gct_se, self.freq_se, self.vstiffness_se = self._calc_statistics()

	def export_analysis(self, outdir: str = "") -> None:
		if len(outdir) > 0 and outdir[-1] != '/':
			outdir = outdir + '/'
		os.makedirs(outdir, exist_ok = True) # ""や"."のときはどうなる？

		plt.figure()
		plt.plot(self.time, self.vgrf, color="black", alpha=1.0, linewidth=1.0)
		plt.xlabel("Time [s]")
		plt.ylabel("vGRF [N]")
		plt.title("Vertical GRF")
		plt.savefig(outdir + "vgrf.png", dpi=300)
		plt.close()

		plt.figure()
		plt.plot(self.time, self.filtered_vgrf, color="black", alpha=1.0, linewidth=1.0)
		plt.xlabel("Time [s]")
		plt.ylabel("vGRF [N]")
		plt.title("Vertical GRF (filtered)")
		plt.savefig(outdir + "filtered_vgrf.png", dpi=300)
		plt.close()

		plt.figure()
		plt.plot(self.time, self.filtered_vgrf, color="black", alpha=1.0, linewidth=1.0)
		for i, hop in enumerate(self.hops):
			if hop.is_valid:
				plt.plot(hop.global_time, hop.vgrf, color="red", alpha=1.0, linewidth=1.0)
			plt.text(hop.global_time[0], hop.vgrf_max + 30, str(i), fontsize=5)
		plt.xlabel("Time [s]")
		plt.ylabel("vGRF [N]")
		plt.title("Valid Hops (Red)")
		plt.savefig(outdir + "valid_hops.png", dpi=300)
		plt.close()

		if self.n_valid_hops == 0:
			return

		bw = self.mass * G
		phase = [x * 100 for x in self.hops[0].time_norm]
		valid_hops = [h for h in self.hops if h.is_valid]
		vgrf_mean = [sum(h.vgrf_norm[i] for h in valid_hops) / self.n_valid_hops for i in range(len(phase))]
		vdisp_mean = [sum(h.vdisp_norm[i] for h in valid_hops) / self.n_valid_hops for i in range(len(phase))]

		plt.figure()
		for h in valid_hops:
			plt.plot(phase, [x / bw for x in h.vgrf_norm], color="gray", alpha=0.3, linewidth=0.8)
		plt.plot(phase, [x / bw for x in vgrf_mean], color="black", alpha=1.0, linewidth=1.0)
		plt.xlabel("Stance Phase [%]")
		plt.ylabel("vGRF [BW]")
		plt.title("Time-Normalized Vertical GRF")
		plt.savefig(outdir + "F-t.png", dpi=300)
		plt.close()

		plt.figure()
		for h in valid_hops:
			plt.plot(h.vdisp_norm, [x / bw for x in h.vgrf_norm], color="gray", alpha=0.3, linewidth=0.8)
		plt.plot(vdisp_mean, [x / bw for x in vgrf_mean], color="black", alpha=1.0, linewidth=1.0)
		plt.xlabel("Vertical Displacement [m]")
		plt.ylabel("vGRF [BW]")
		plt.title("Time-Normalized Vertical GRF-Displacement Relationship")		
		plt.savefig(outdir + "F-x.png", dpi=300)	
		plt.close()

		data = {
			"n_valid_hops": self.n_valid_hops,
			"gct_mean [s]": self.gct_mean,
			"vgrf_max_mean [F]": self.vgrf_max_mean,
			"freq_mean [Hz]": self.freq_mean,
			"vstiffness_mean [N/m]": self.vstiffness_mean
			}
		with open(outdir + "summary.csv", "w") as f:
			writer = csv.writer(f)
			for key, value in data.items():
				writer.writerow([key, f"{value:.3f}"])
