from typing import List, Tuple, Union
import model
import data
import normalization as nz
import mathematics as mt
import util as u
import statistics as st
import copy
import pandas as pd
import scanpy as sc
import anndata as ad
import numpy as np
from scipy import sparse
import csv_handler as csv
import os


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
			mt.roundoff(nz.zscore(attr, attributes), decimal_place) for attr in attributes
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
			mt.roundoff(nz.minmax(attr, min(attributes), max(attributes), scaled_min, scaled_max), decimal_place) for attr in attributes
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


def filter_cells(datamatrix: model.DataMatrix, min_counts: int) -> model.DataMatrix:

	list_of_list: List[List[float]] = datamatrix.get_list_of_list(append_attribute_labels=False, append_classlabels=False)
	cell_filtered_lol: List[Union[List[str], List[Union[float, str]]]] = list()
	unfiltered_attributes_list: List[str] = copy.deepcopy(datamatrix.attributes)
	temp_folder: str = '__temp__'
	filehash: str = u.hash()
	filename: str = filehash + '.csv'
	cf_filename: str = filehash + '-cell_filtered.csv'
	complete_file_path: str = os.path.join(temp_folder, filename)

	u.create_path_if_not_exists(temp_folder)
	pd.DataFrame(list_of_list).to_csv(complete_file_path, index=False, index_label=False, header=False)

	sc_object: ad.AnnData = sc.read_csv(complete_file_path)
	stale_X: Union[np.ndarray, sparse.spmatrix, None] = copy.deepcopy(sc_object.X)

	sc.pp.filter_cells(sc_object, min_counts=min_counts)

	for row in sc_object.X:
		cell_filtered_lol.append(row.tolist())

	# delete
	count: int = 0

	for filtered_row in cell_filtered_lol:
		for row_index in range(datamatrix.sample_count()):
			if u.equal_lists(filtered_row, list_of_list[row_index]):
				filtered_row.append(datamatrix.get_classlabel(row_index))
				count += 1
				break

	print("count: ", count)

	cell_filtered_lol.insert(0, unfiltered_attributes_list)
	cell_filtered_lol[0].append('class')
	csv.writecsv(cf_filename, cell_filtered_lol, directory=temp_folder)




















def fc(datamatrix: model.DataMatrix, min_counts: int) -> model.DataMatrix:
	return filter_cells(datamatrix, min_counts)
