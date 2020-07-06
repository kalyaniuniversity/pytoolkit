from typing import List
import copy
import model as m
import string
import random


def hash(length=10) -> str:
	return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def get_label_separated_attributes(attribute_list: List[float], classlabels: List[str], unique_classlabels: List[str]) -> List[List[float]]:

	label_separated_attributes = list()

	for label in unique_classlabels:

		similar_labeled_attributes = list()

		for i in range(0, len(attribute_list)):
			if classlabels[i] == label:
				similar_labeled_attributes.append(attribute_list[i])

		label_separated_attributes.append(copy.deepcopy(similar_labeled_attributes))

	return label_separated_attributes


def get_list_of_list_from_datamatrix(datamatrix: m.DataMatrix) -> List[List[float]]:

	list_of_list = list()

	for sample in datamatrix.samples:
		list_of_list.append(sample.get_values())

	return list_of_list


def get_classlabeled_list_of_list_from_datamatrix(datamatrix: m.DataMatrix):

	list_of_list = list()

	for sample in datamatrix.samples:
		values = sample.get_values()
		values.append(sample.classlabel)
		list_of_list.append(values)

	return list_of_list


def gclld(datamatrix: m.DataMatrix):
	return get_classlabeled_list_of_list_from_datamatrix(datamatrix)