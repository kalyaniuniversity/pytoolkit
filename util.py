from typing import List, Union
import copy
import model as m
import string
import random
import os
import math


def hash(length=10) -> str:
	return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def is_valid_path(path: str) -> bool:
	return os.path.exists(path)


def create_path_if_not_exists(path: str):
	if not is_valid_path(path):
		os.mkdir(path)


def roundoff(value: float, decimal_place: int, force_completion: bool = False) -> float:
	decimal_place: float = pow(10, decimal_place)
	rounded_value: float = math.ceil(value * decimal_place) / decimal_place

	if force_completion:
		while decimal_points(rounded_value) != decimal_place:
			rounded_value = float(str(rounded_value) + '0')

	return rounded_value


def decimal_points(value: float) -> int:

	value = str(value)

	if '.' not in value:
		return 0
	return len(value.split('.')[1])


def equal_lists(list1: List[float], list2: List[float], tolerance: float = 0.0) -> bool:

	if len(list1) != len(list2):
		return False

	for i in range(len(list1)):
		if not math.isclose(list1[i], list2[i], rel_tol=tolerance) and not math.isclose(list1[i], list2[i], abs_tol=tolerance):
			return False

	return True


def get_column(list_of_list: List[List], index: int) -> List:

	column: List = list()

	for row in list_of_list:
		column.append(row[index])

	return column


def get_label_separated_attributes(attribute_list: List[float], classlabels: List[str], unique_classlabels: List[str]) -> List[List[float]]:

	label_separated_attributes: List[List[float]] = list()

	for label in unique_classlabels:

		similar_labeled_attributes: List[float] = list()

		for i in range(0, len(attribute_list)):
			if classlabels[i] == label:
				similar_labeled_attributes.append(attribute_list[i])

		label_separated_attributes.append(copy.deepcopy(similar_labeled_attributes))

	return label_separated_attributes


def get_list_of_list_from_datamatrix(datamatrix: m.DataMatrix) -> List[List[float]]:

	list_of_list: List[List[float]] = list()

	for sample in datamatrix.samples:
		list_of_list.append(sample.get_values())

	return list_of_list


def get_classlabeled_list_of_list_from_datamatrix(datamatrix: m.DataMatrix) -> List[List[Union[float, str]]]:

	list_of_list: List[List[Union[float, str]]] = list()

	for sample in datamatrix.samples:
		values: List[Union[float, str]] = sample.get_values()
		values.append(sample.classlabel)
		list_of_list.append(values)

	return list_of_list


def gclld(datamatrix: m.DataMatrix) -> List[List[Union[float, str]]]:
	return get_classlabeled_list_of_list_from_datamatrix(datamatrix)
