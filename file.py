from typing import List


def readfile(filename: str, rstrip: bool = False) -> List[str]:

	lines: List[str] = list()

	with open(filename, 'r') as datafile:
		for line in datafile:
			if rstrip:
				line = line.rstrip()
			lines.append(line)

	return lines


def writefile(filename: str, content: str):
	writer = open(filename, 'w+')
	writer.write(content)
	writer.close()
