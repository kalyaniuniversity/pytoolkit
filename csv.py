import file
import model as m
import util as u
from typing import List
import copy


def readcsv(filename: str, separator=',', rstrip=True) -> List[List[str]]:

	list_of_list = list()
	lines = file.readfile(filename, rstrip)

	for line in lines:
		list_of_list.append(line.split(separator))

	return list_of_list


def writecsv(filename: str, list_of_list, separator=',', newline=True):

	writecontent = ""

	for row in list_of_list:
		line = ""
		for value in row[:-1]:
			line += str(value) + separator

		line += str(row[-1]) + ("\n" if newline else "")
		writecontent += line

	file.writefile(filename, writecontent)


def writecsv_matrix(datamatrix: m.DataMatrix, filename=None):

	list_of_list = u.get_classlabeled_list_of_list_from_datamatrix(datamatrix)
	attributes = copy.deepcopy(datamatrix.attributes)
	attributes.append('class')
	list_of_list.insert(0, attributes)

	if filename is None:
		filename = datamatrix.dataset_name if datamatrix.dataset_name is not None else u.hash()

	filename = 'output-' + filename + '.csv'

	writecsv(filename, list_of_list)


def wcsvm(datamatrix: m.DataMatrix, filename=None):
	writecsv_matrix(datamatrix, filename=filename)

