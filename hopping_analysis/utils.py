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

def time_normalize(time: list[float], signal: list[float], n_points: int = 101) -> tuple[list[float], list[float]]:
	time_norm = []
	signal_norm = []
	# script
	return time_norm, signal_norm
