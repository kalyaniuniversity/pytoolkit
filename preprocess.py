import csv
import model
import normalization as nz
import mathematics as mt


def filter_csv_by_sd(filename: str, attr_count: int, separator=',', rstrip=True) -> model.DataMatrix:
	return filter_attributes_by_sd(csv.readcsv(filename, separator=separator, rstrip=rstrip), attr_count)


def normalize(datamatrix: model.DataMatrix, type='zscore') -> model.DataMatrix:
	if type == 'zscore':
		return zscore_normalize(datamatrix)
	if type == 'minmax':
		return minmax_normalize(datamatrix)


def zscore_normalize(datamatrix: model.DataMatrix) -> model.DataMatrix:

	for i in range(0, datamatrix.sample_count()):
		attributes = datamatrix.get_float_attribute_list(i)
		datamatrix.set_float_attribute_list([mt.roundoff(nz.zscore(attr, attributes), 4) for attr in attributes], i)

	return datamatrix


def minmax_normalize(datamatrix: model.DataMatrix) -> model.DataMatrix:
	pass


def filter_attributes_by_sd(datamatrix: model.DataMatrix, attr_count: int) -> model.DataMatrix:
	pass
