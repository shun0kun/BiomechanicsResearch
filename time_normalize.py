def is_strictly_increasing(x: list[float]) -> bool:
	for i in range(len(x) - 1):
		if (x[i + 1] <= x[i]):
			return False
	return True

def time_normalize(time: list[float], signal: list[float], n_points: int = 101) -> tuple[list[float], list[float]]:

	if len(time) != len(signal) or len(time) < 2 or n_points < 2 or not is_strictly_increasing(time):
		raise ValueError("Invalid value")

	phase_original = []
	phase_target = []
	for i in range(len(time)):
		phase_original.append((time[i] - time[0]) / (time[-1] - time[0]))
	for i in range(n_points):
		phase_target.append(i / (n_points - 1))
	
	signal_normalized = []
	i = 0
	j = 0
	while i < n_points:
		while j < len(phase_original) - 1 and phase_original[j + 1] < phase_target[i]:
			j += 1
		x = signal[j] + (phase_target[i] - phase_original[j]) * (signal[j + 1] - signal[j]) / (phase_original[j + 1] - phase_original[j])
		signal_normalized.append(x)
		i += 1

	time_normalized = phase_target

	return time_normalized, signal_normalized
