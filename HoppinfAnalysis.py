class Hop:
	def __init__(self, time: list[float], vgrf: list[float]) -> None
		self.time = time
		self.vgrf = vgrf
		self._compute_vdisp()
		self._time_normalize()
	
	def _compute_vdisp(self) -> None:
		self.vdisp = []
	
	def _time_normalize(self) -> None:
		self.time_norm = []
		self.vgrf_norm = []
		self.vdisp_norm = []


class HoppingAnalysis:
	def __init__(self, filename: str) -> None:
		
		
	def _extract_hops(self) -> None:
		self.hops = []
		
