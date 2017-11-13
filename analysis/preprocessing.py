"""
Some data preprocessing functions
"""
from analysis.statistics import mean, std
import math


def normalize(arr) -> None:
	"""
	Normalize data in given array

	:param arr: array of data
	"""
	minX = min(arr)
	maxX = max(arr)
	diff = maxX - minX

	for i in range(len(arr)):
		arr[i] = (arr[i] - minX) / diff

def normalize_max(arr) -> None:
	"""
	Normalize data in given array to values from (-infinity; 1]. This algo scales data in such way that max positive values are 1
	and min negative value is inifinity but negative values also scales to max positive values.

	:param arr: array of data
	"""
	maxX = max(arr)

	if maxX <= 0:
		return arr

	for i in range(len(arr)):
		arr[i] = arr[i] / maxX

def anti_shift(arr) -> None:
	"""
	Shift data to zero mean

	:param arr: Array of data
	"""
	m = mean(arr)
	for i in range(len(arr)):
		arr[i] -= m

def anti_spike(arr) -> None:
	"""
	Delete spikes that are more than mean + 4 sigmas

	:param arr: array of data with spikes
	"""
	avg = mean(arr)
	sigma = std(arr)
	for x in range(len(arr)):
		if math.fabs(arr[x]) > avg + 4 * sigma:
			if x == 0:
				arr[x] = (arr[x + 1] + arr[x + 2]) / 2
			elif x == len(arr) - 1:
				arr[x] = (arr[x - 2] + arr[x - 1]) / 2
			else:
				arr[x] = (arr[x-1] + arr[x + 1]) / 2

def anti_trend(arr, window_width = None) -> None:
	"""
	Use floating window to remove trends from data

	:param arr: array of values
	:param window_width: width of window
	"""
	if window_width is None :
		window_width = int(len(arr) / 100)

	counter = int(math.floor(len(arr) / window_width))
	for i in range(counter):
		mean_v = mean(arr[i * window_width : (i + 1) * window_width])
		for x in range(window_width):
			arr[i * window_width + x] -= mean_v

	# Resize last values
	if window_width * counter == len(arr):
		return

	mean_v = mean(arr[window_width * counter:])
	for x in range(window_width * counter, len(arr)):
		arr[x] -= mean_v

