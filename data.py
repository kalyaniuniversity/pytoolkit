import copy
import os
from typing import List
import anndata as ad
import scanpy as sc
import csv_handler as csv
import model as m
import util as u


def build_model_from_csv(filename: str, separator: str = ',', rstrip: bool = True) -> m.DataMatrix:
	return m.DataMatrix.from_list_of_list(list_of_list=csv.readcsv(filename, separator=separator, rstrip=rstrip))


def build_model_from_selected_attributes(filename: str, attributes: List[str], separator: str = ',', rstrip: bool = True) -> m.DataMatrix:

	new_samples: List[m.Sample] = list()
	datamatrix: m.DataMatrix = build_model_from_csv(filename, separator=separator, rstrip=rstrip)

	for sample in datamatrix.samples:
		new_samples.append(m.Sample(
			sample.get_datapoints([
				datamatrix.attributes.index(attribute.strip()) for attribute in attributes
			]),
			associated_attributes=copy.deepcopy(attributes),
			classlabel=sample.classlabel
		))

	return m.DataMatrix(
		new_samples,
		attributes=copy.deepcopy(attributes),
		classlabels=copy.deepcopy(datamatrix.classlabels),
		unique_classlabels=copy.deepcopy(datamatrix.unique_classlabels),
		dataset_name=datamatrix.dataset_name
	)


def bmsa(filename: str, attributes: List[str], separator: str = ',', rstrip: bool = True) -> m.DataMatrix:
	return build_model_from_selected_attributes(filename, attributes, separator=separator, rstrip=rstrip)


def read_as_anndata(list_of_list: List[List[float]], roundoff_decimal: int = 5, filename: str = None) -> ad.AnnData:

	temp_folder: str = '__temp__'
	complete_file_path: str = os.path.join(temp_folder, filename)

	list_of_list = [[u.roundoff(value, roundoff_decimal) for value in row] for row in list_of_list]

	u.create_path_if_not_exists(temp_folder)
	csv.writecsv(filename, list_of_list, directory=temp_folder)

	return sc.read_csv(complete_file_path)


def rad(list_of_list: List[List[float]], roundoff_decimal: int = 5, filename: str = None) -> ad.AnnData:
	return read_as_anndata(list_of_list, roundoff_decimal=roundoff_decimal, filename=filename)
