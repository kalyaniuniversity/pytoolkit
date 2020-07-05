def readfile(filename, rstrip=False):

	lines = list()

	with open(filename, 'r') as datafile:
		for line in datafile:
			if rstrip:
				line = line.rstrip()
			lines.append(line)

	return lines


def writefile(filename, content):
	writer = open(filename, 'w+')
	writer.write(content)
	writer.close()
