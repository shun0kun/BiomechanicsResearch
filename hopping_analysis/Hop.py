import numpy
from . import utils

class Hop:
	def __init__(self, mass: float, time: list[float], vgrf: list[float]) -> None:
		self.mass = mass
		self.time = [t - time[0] for t in time]
		self.vgrf = vgrf
		self.vdisp = None
		self.time_norm, self.vgrf_norm = utils.time_normalize(time, vgrf)
		_, self.vdisp_norm = utils.time_normalize(time, self.vdisp)
		self.vgrf_max = max(vgrf)
		self.freq = self._compute_freq()
		self.gct = time[-1] - time[0]
		self.vstiffness = self._compute_vstiffness()

	def _compute_vdisp(self) -> list[float]:
		vdisp = []
		# script
		return vdisp
	
	# 未定義動作あり
	def _compute_freq(self) -> float:
		t = []
		bw = self.mass * 9.81
		for i in range(len(self.vgrf)):
			if self.vgrf[i] >= bw:
				t.append(self.time[i])
		period = (t[-1] - t[0]) * 2
		freq = 1 / period
		return freq

	def _compute_vstiffness(self) -> float:
		return self.mass * (2 * numpy.pi * self.freq) ** 2
