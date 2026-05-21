import csv
import matplotlib.pyplot as plt
import utils
from Hop import Hop

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
		for i in range(len(self.filtered_vgrf)):
			


	def analyze(self, outdir: str = "") -> None:
		plt.figure()
		plt.close()


