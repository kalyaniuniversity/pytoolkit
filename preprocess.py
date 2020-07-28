import copy
import statistics as st
from typing import List, Tuple, Union
import scanpy as sc
import csv_handler as csv
import data
import model
import normalization as nz
import util as u


def filter_csv_by_sd(filename: str, attr_count: int, separator: str = ',', rstrip: bool = True) -> model.DataMatrix:
	return filter_attributes_by_sd(data.build_model_from_csv(filename, separator=separator, rstrip=rstrip), attr_count)


def normalize(datamatrix: model.DataMatrix, type: str = 'zscore', scaled_min: float = 0, scaled_max: float = 1) -> model.DataMatrix:
	if type == 'zscore':
		return zscore_normalize(datamatrix)
	if type == 'minmax':
		return minmax_normalize(datamatrix, scaled_min=scaled_min, scaled_max=scaled_max)


def zscore_normalize(datamatrix: model.DataMatrix, roundoff: bool = True, decimal_place: int = 4) -> model.DataMatrix:

	for i in range(0, datamatrix.attribute_count()):
		attributes: List[float] = datamatrix.get_float_attribute_list(i)
		nz_attributes: List[float] = [
			u.roundoff(nz.zscore(attr, attributes), decimal_place) for attr in attributes
		] if roundoff else [
			nz.zscore(attr, attributes) for attr in attributes
		]
		datamatrix.set_float_attribute_list(nz_attributes, i)

	return datamatrix


def zsn(datamatrix: model.DataMatrix, roundoff: bool = True, decimal_place: int = 4) -> model.DataMatrix:
	return zscore_normalize(datamatrix, roundoff=roundoff, decimal_place=decimal_place)


def minmax_normalize(
		datamatrix: model.DataMatrix,
		scaled_min: float = 0,
		scaled_max: float = 1,
		roundoff: bool = True,
		decimal_place: int = 4
) -> model.DataMatrix:

	for i in range(0, datamatrix.attribute_count()):
		attributes: List[float] = datamatrix.get_float_attribute_list(i)
		nz_attributes: List[float] = [
			u.roundoff(nz.minmax(attr, min(attributes), max(attributes), scaled_min, scaled_max), decimal_place) for attr in attributes
		] if roundoff else [
			nz.minmax(attr, min(attributes), max(attributes), scaled_min, scaled_max) for attr in attributes
		]
		datamatrix.set_float_attribute_list(nz_attributes, i)

	return datamatrix


def sort_attributes_by_sd(datamatrix: model.DataMatrix) -> model.DataMatrix:

	sd_tuples: List[Tuple[int, float]] = list()

	for i in range(0, datamatrix.attribute_count()):
		sd_tuples.append((i, st.stdev(datamatrix.get_float_attribute_list(i))))

	return rearrange_sd_tuples(datamatrix, sd_tuples)


def sort_classlabeled_attributes_by_sd(datamatrix: model.DataMatrix) -> model.DataMatrix:

	sd_tuples: List[Tuple[int, float]] = list()

	for i in range(0, datamatrix.attribute_count()):
		sd_tuples.append(
			(i, sum([
				st.stdev(attr_list) for attr_list in u.get_label_separated_attributes(
					datamatrix.get_float_attribute_list(i),
					datamatrix.classlabels,
					datamatrix.unique_classlabels
				)
			]))
		)

	return rearrange_sd_tuples(datamatrix, sd_tuples)


def rearrange_sd_tuples(datamatrix: model.DataMatrix, sd_tuples: List[Tuple[int, float]]) -> model.DataMatrix:

	new_attributes: List[str] = list()

	sd_tuples.sort(key=lambda value: value[1], reverse=True)

	for i in range(0, datamatrix.attribute_count()):
		index: int = sd_tuples[i][0]
		datamatrix.set_float_attribute_list(datamatrix.get_float_attribute_list(index), i)
		new_attributes.append(datamatrix.get_attribute_label(index))

	datamatrix.reset_attributes(new_attributes)

	return datamatrix


def filter_attributes_by_sd(datamatrix: model.DataMatrix, attr_count: int) -> model.DataMatrix:

	samples: List[model.Sample] = list()
	datamatrix = sort_attributes_by_sd(datamatrix)
	attribute_labels: List[str] = datamatrix.attributes[:attr_count]

	for sample in datamatrix.samples:
		samples.append(sample.subsample(bound=attr_count))

	return model.DataMatrix(
		samples,
		attributes=attribute_labels,
		classlabels=copy.deepcopy(datamatrix.classlabels),
		unique_classlabels=copy.deepcopy(datamatrix.unique_classlabels),
		dataset_name=datamatrix.dataset_name
	)


def fasd(datamatrix: model.DataMatrix, attr_count: int) -> model.DataMatrix:
	return filter_attributes_by_sd(datamatrix, attr_count)


def filter_cells(
		datamatrix: model.DataMatrix,
		min_cells: int,
		roundoff_decimal: int = 5,
		filehash: str = u.hash(),
		writefile: bool = True) -> model.DataMatrix:

	list_of_list: List[List[float]] = datamatrix.get_list_of_list(append_attribute_labels=False, append_classlabels=False)
	cell_filtered_lol: List[Union[List[str], List[Union[float, str]]]] = list()
	unfiltered_attributes_list: List[str] = copy.deepcopy(datamatrix.attributes)
	filename: str = filehash + '.csv'
	sc_object = data.read_as_anndata(list_of_list, roundoff_decimal=roundoff_decimal, filename=filename)

	sc.pp.filter_cells(sc_object, min_counts=min_cells)

	for row in sc_object.X:
		cell_filtered_lol.append([u.roundoff(value, roundoff_decimal) for value in row.tolist()])

	for filtered_row in cell_filtered_lol:
		for row_index in range(datamatrix.sample_count()):
			if u.equal_lists(filtered_row, list_of_list[row_index], tolerance=0.00002):
				filtered_row.append(datamatrix.get_classlabel(row_index))
				break

	cell_filtered_lol.insert(0, unfiltered_attributes_list)
	cell_filtered_lol[0].append('class')

	if writefile:
		csv.writecsv(filehash + '-cell_filtered.csv', cell_filtered_lol, directory='__temp__')

	return model.DataMatrix.from_list_of_list(cell_filtered_lol)


def fc(datamatrix: model.DataMatrix, mc: int, rd: int = 5, fh: str = u.hash(), wf: bool = True) -> model.DataMatrix:
	return filter_cells(datamatrix, min_cells=mc, roundoff_decimal=rd, filehash=fh, writefile=wf)


def filter_genes(
		datamatrix: model.DataMatrix,
		min_genes: int,
		roundoff_decimal: int = 5,
		filehash: str = u.hash(),
		writefile: bool = True
) -> model.DataMatrix:

	list_of_list: List[List[float]] = datamatrix.get_list_of_list(append_attribute_labels=False, append_classlabels=False)
	gene_filtered_lol: List[Union[List[str], List[Union[float, str]]]] = list()
	filtered_attributes_list: List[str] = list()
	filename: str = filehash + '-cell_filtered.csv'
	sc_object = data.read_as_anndata(list_of_list, roundoff_decimal=roundoff_decimal, filename=filename)

	sc.pp.filter_genes(sc_object, min_counts=min_genes)

	for row in sc_object.X:
		gene_filtered_lol.append([u.roundoff(value, roundoff_decimal) for value in row.tolist()])

	for filtered_attr_index in range(len(gene_filtered_lol[0])):

		f_column: List[float] = u.get_column(gene_filtered_lol, filtered_attr_index)

		for i in range(datamatrix.attribute_count()):
			if u.equal_lists(
				u.get_column(list_of_list, i),
				f_column,
				tolerance=0.00002
			):
				filtered_attributes_list.append(datamatrix.get_attribute_label(i))
				break

	for i in range(datamatrix.sample_count()):
		gene_filtered_lol[i].append(datamatrix.get_classlabel(i))

	gene_filtered_lol.insert(0, filtered_attributes_list)
	gene_filtered_lol[0].append('class')

	if writefile:
		csv.writecsv(filehash + '-gene_filtered.csv', gene_filtered_lol, directory='__temp__')

	return model.DataMatrix.from_list_of_list(gene_filtered_lol)


def fg(datamatrix: model.DataMatrix, mg: int, rd: int = 5, fh: str = u.hash(), wf: bool = True) -> model.DataMatrix:
	return filter_genes(datamatrix, min_genes=mg, roundoff_decimal=rd, filehash=fh, writefile=wf)


def filter_singlecells(
		datamatrix: model.DataMatrix,
		min_cells: int,
		min_genes: int,
		roundoff_decimal: int = 5,
		clear_temp: bool = False) -> model.DataMatrix:

	filehash: str = u.hash()
	datamatrix = filter_cells(datamatrix, min_cells=min_cells, roundoff_decimal=roundoff_decimal, filehash=filehash)
	datamatrix = filter_genes(datamatrix, min_genes=min_genes, roundoff_decimal=roundoff_decimal, filehash=filehash)

	if clear_temp:
		u.clear_temp()

	return datamatrix


def fsc(datamatrix: model.DataMatrix, mc: int, mg: int, rd: int = 5, ct: bool = False) -> model.DataMatrix:
	return filter_singlecells(datamatrix, mc, mg, roundoff_decimal=rd, clear_temp=ct)
