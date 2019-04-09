import numpy as np

# Container class for images
class Image:
	def __init__(self, w, h, data):
		self.w = w
		self.h = h
		self.data = data

# Open image (bit of a misnomer)
def convert(filename):
	with open(filename, 'r') as file:
		data = np.asarray([list(line.replace('\n','')) for line in file.readlines()])

	dim = data.shape
	return Image(dim[1], dim[0], data)

# Quick test
if __name__ == '__main__':
	print(convert('dvd.txt').data)
