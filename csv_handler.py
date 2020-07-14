import file
import model as m
import util as u
from typing import List, Union
import copy
import os


def readcsv(filename: str, separator: str = ',', rstrip: bool = True) -> List[List[str]]:

	list_of_list: List[List[str]] = list()
	lines: List[str] = file.readfile(filename, rstrip)

	for line in lines:
		list_of_list.append(line.split(separator))

	return list_of_list


def writecsv(
		filename: str,
		list_of_list: List[List[float]] or List[List[str]],
		directory: str or None = None,
		separator: str = ',',
		newline: bool = True
):

	writecontent: str = ""

	for row in list_of_list:
		line: str = ""
		for value in row[:-1]:
			line += str(value) + separator

		line += str(row[-1]) + ("\n" if newline else "")
		writecontent += line

	if directory is not None or directory != '':
		if not u.is_valid_path(directory):
			os.mkdir(directory)
		complete_file_path = os.path.join(directory, filename)
	else:
		complete_file_path = filename

	file.writefile(complete_file_path, writecontent)


def writecsv_matrix(datamatrix: m.DataMatrix, filename: str = None):

	list_of_list: List[List[Union[float, str]]] = u.get_classlabeled_list_of_list_from_datamatrix(datamatrix) \
													if datamatrix.classlabels is not None else \
													u.get_list_of_list_from_datamatrix(datamatrix)
	attributes: List[str] or None = copy.deepcopy(datamatrix.attributes) if datamatrix.attributes is not None else None

	if attributes is not None:
		attributes.append('class')
		list_of_list.insert(0, attributes)

	if filename is None:
		filename = datamatrix.dataset_name if datamatrix.dataset_name is not None else u.hash()

	filename += '.csv'

	writecsv(filename, list_of_list, directory='output')


def wcsvm(datamatrix: m.DataMatrix, filename: str = None):
	writecsv_matrix(datamatrix, filename=filename)