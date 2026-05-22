import csv
import numpy

# 簡易版(最初の5秒を抽出。1000Hzであると仮定)
# 未定義動作あり (エラーハンドリング) (未)
# 五秒間一定値区間自動検出機能 (未)
def estimate_mass_from_csv(filepath: str) -> float:
	# time = []
	vgrf = []
	with open(filepath, encoding="cp932") as f:
		reader = csv.reader(f)
		for i, row in enumerate(reader):
			if i < 13:
				continue
			# time.append(float[row[0]])
			vgrf.append(float(row[23]))
	mass = numpy.mean(vgrf[0:5000]) / 9.81
	return mass

# intも許した方がいいかな。型ヒントの書き方。
def is_strictly_increasing(x: list[float]) -> bool:
	for i in range(len(x) - 1):
		if x[i] >= x[i + 1]:
			return False
	return True

# 実装する。線形補間。スペルチェック。
def liner_compliment(x1: float, x2: float, ratio: float) -> float:
	return x1 + ratio * (x2 - x1)

def time_normalize(time: list[float], signal: list[float], n_points: int = 101) -> tuple[list[float], list[float]]:
	if len(time) != len(signal) or len(time) < 2 or n_points < 2 or not is_strictly_increasing(time):
		raise ValueError("time_normalize: Invalid value")
	phase_origin = []
	phase_target = []
	for i in range(len(time)):
		phase_origin.append((time[i] - time[0]) / (time[-1] - time[0]))
	for i in range(n_points):
		phase_target.append(i / (n_points - 1))
	time_norm = phase_target
	signal_norm = []
	i = 0
	j = 0
	while i < n_points:
		while j < len(phase_origin) - 1 and phase_origin[j + 1] < phase_target[i]:
			j += 1
		signal_norm.append(liner_compliment(signal[j], signal[j + 1], (phase_target[i] - phase_origin[j]) / (phase_origin[j + 1] - phase_origin[j])))
		i += 1
	return time_norm, signal_norm

def mean2(x: float, y: float) -> float:
	return (x + y) / 2
