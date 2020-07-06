from typing import List
import copy


def get_label_separated_attributes(attribute_list: List[float], classlabels: List[str], unique_classlabels: List[str]) -> List[List[float]]:

	label_separated_attributes = list()

	for label in unique_classlabels:

		similar_labeled_attributes = list()

		for i in range(0, len(attribute_list)):
			if classlabels[i] == label:
				similar_labeled_attributes.append(attribute_list[i])

		label_separated_attributes.append(copy.deepcopy(similar_labeled_attributes))

	return label_separated_attributes
