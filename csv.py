import file


def readcsv(filename, separator=',', rstrip=True):

	list_of_list = list()
	lines = file.readfile(filename, rstrip)

	for line in lines:
		list_of_list.append(line.split(separator))

	return list_of_list


def writecsv(filename, list_of_list, separator=',', newline=True):

	writecontent = ""

	for row in list_of_list:
		line = ""
		for value in row[:-1]:
			line += str(value) + separator

		line += str(row[-1]) + ("\n" if newline else "")
		writecontent += line

	file.writefile(filename, writecontent)



