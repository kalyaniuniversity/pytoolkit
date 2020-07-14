import csv_handler as csv
import model as m
from typing import List
import copy


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
