import numpy
import matplotlib.pyplot as plt
from . import utils

G = 9.81

class Hop:
	def __init__(self, mass: float, time: list[float], vgrf: list[float]) -> None:
		self.is_valid = True
		self.mass = mass
		self.global_time = time
		self.time = [t - time[0] for t in time]
		self.vgrf = vgrf
		self.vdisp = self._compute_vdisp()
		self.time_norm, self.vgrf_norm = utils.time_normalize(time, vgrf)
		_, self.vdisp_norm = utils.time_normalize(time, self.vdisp)
		self.gct = time[-1] - time[0]
		self.vgrf_max = max(vgrf)
		self.vstiffness = self._compute_vstiffness()

	# 鉛直下向きを正とする
	def _compute_vdisp(self) -> list[float]:
		vacc = []
		vvel = [0.0] * len(self.time)
		vdisp = [0.0] * len(self.time)
		for i in range(len(self.vgrf)):
			vacc.append((self.mass * G - self.vgrf[i]) / self.mass)
		i_max = self.vgrf.index(max(self.vgrf))
		vvel[i_max] = 0.0
		for i in range(i_max, len(self.time) - 1):
			vvel[i + 1] = vvel[i] + utils.mean2(vacc[i], vacc[i + 1]) * (self.time[i + 1] - self.time[i])
		for i in range(i_max, 0, -1):
			vvel[i - 1] = vvel[i] + utils.mean2(vacc[i - 1], vacc[i]) * (self.time[i - 1] - self.time[i])
		for i in range(len(self.time) - 1):
			vdisp[i + 1] = vdisp[i] + utils.mean2(vvel[i], vvel[i + 1]) * (self.time[i + 1] - self.time[i])
		return vdisp
	
	def _compute_vdisp_euler(self) -> list[float]:
		vacc = []
		vvel = [0.0] * len(self.time)
		vdisp = [0.0] * len(self.time)
		for i in range(len(self.vgrf)):
			vacc.append((self.mass * G - self.vgrf[i]) / self.mass)
		i_max = self.vgrf.index(max(self.vgrf))
		vvel[i_max] = 0.0
		for i in range(i_max, len(self.time) - 1):
			vvel[i + 1] = vvel[i] + vacc[i] * (self.time[i + 1] - self.time[i])
		for i in range(i_max, 0, -1):
			vvel[i - 1] = vvel[i] + vacc[i - 1] * (self.time[i - 1] - self.time[i])
		for i in range(len(self.time) - 1):
			vdisp[i + 1] = vdisp[i] + vvel[i] * (self.time[i + 1] - self.time[i])
		return vdisp

	# 未定義動作あり。vgrf_max < bwのとき、tが空になる。bw以上のvgrf要素数が1でも0devideになる。最低連続した2要素必要。
	def _compute_vstiffness(self) -> float | None:
		t = []
		bw = self.mass * G
		for i in range(len(self.vgrf)):
			if self.vgrf[i] >= bw:
				t.append(self.time[i])
		if len(t) < 2:
			self.is_valid = False
			return None
		period = (t[-1] - t[0]) * 2.0	
		omega = 2.0 * numpy.pi / period 
		return self.mass * omega ** 2.0
	
	def fx_fig(self, path: str) -> None:
		bw = self.mass * G
		plt.figure()
		plt.plot(self.vdisp_norm, [x / bw for x in self.vgrf_norm])
		plt.xlabel("Vertical Displacement [m]")
		plt.ylabel("vGRF [BW]")
		plt.title("F-x")
		plt.savefig(path, dpi=300)
		plt.close()
	
	def ft_fig(self, path: str) -> None:
		plt.figure()
		bw = self.mass * G
		plt.plot([x * 100 for x in self.time_norm], [x / bw for x in self.vgrf_norm])
		plt.xlabel("Stance Phase [m]")
		plt.ylabel("vGRF [BW]")
		plt.title("F-t")
		plt.savefig(path, dpi=300)
		plt.close()
