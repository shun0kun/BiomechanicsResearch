import utils

class Hop:
	def __init__(self, time: list[float], vgrf: list[float]) -> None:
		self.time = time
		self.vgrf = vgrf
		self.vdisp
		self.time_norm, self.vgrf_norm = utils.time_normalize(time, vgrf)
		_, self.vdisp_norm = utils.time_normalize(time, self.vdisp)
		self.vgrf_max = max(vgrf)
		self.freq = self._compute_freq()
		self.gct = self._compute_gct()
		self.vstiffness = self._compute_vstiffness()

	def _compute_vdisp(self) -> list[float]:
		vdisp = []
		return vdisp
	
	def _compute_freq(self) -> float:
	
	def _compute_gct(self) -> float:

	def _compute_vstiffness(self) -> float: