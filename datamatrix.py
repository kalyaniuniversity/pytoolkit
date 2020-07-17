import copy
from typing import List, Union, Tuple

from sample import Sample


class DataMatrix:

	samples: List[Sample] = None
	attributes: List[str] or None = None
	classlabels: List[str] or None = None
	dataset_name: str or None = None
	unique_classlabels: List[str] or None = None

	def __init__(
			self,
			samples: List[Sample],
			attributes: List[str] = None,
			classlabels: List[str] = None,
			unique_classlabels: List[str] = None,
			dataset_name: str = None
	):
		self.samples = samples
		self.attributes = attributes
		self.classlabels = classlabels
		self.unique_classlabels = unique_classlabels
		self.dataset_name = dataset_name

	@classmethod
	def from_list_of_list(cls, list_of_list: List[List[str]], has_attributes: bool = True, has_classlabels: bool = True) -> 'DataMatrix':

		samples: List[Sample] = list()
		attributes: List[str] or None = None
		classlabels: List[str] or None = None
		unique_classlabels: List[str] or None = None

		if has_attributes:
			attributes = copy.deepcopy(list_of_list[0][:-1])
			list_of_list.pop(0)

		if has_classlabels:
			classlabels = list()
			unique_classlabels = list()

		for row in list_of_list:
			label = row[-1]
			samples.append(
				Sample.from_values(
					values=[float(i) for i in (row[:-1] if has_classlabels else row)],
					associated_attributes=attributes,
					classlabel=(label if has_classlabels else None)
				)
			)
			if has_classlabels:
				classlabels.append(label)

		if has_classlabels:
			for label in classlabels:
				if label not in unique_classlabels:
					unique_classlabels.append(label)

		return cls(samples, attributes=attributes, classlabels=classlabels, unique_classlabels=unique_classlabels)

	@classmethod
	def fll(cls, list_of_list: List[List[str]], has_attributes: bool = True, has_classlabels: bool = True) -> 'DataMatrix':
		return cls.from_list_of_list(list_of_list, has_attributes=has_attributes, has_classlabels=has_classlabels)

	def sample_count(self) -> int:
		return len(self.samples)

	def attribute_count(self) -> int:
		return len(self.attributes)

	def shape(self) -> Tuple[int, int]:
		return self.sample_count(), self.attribute_count()

	def get_attribute(self, index: int) -> List[Union[str, float]]:

		attribute_column: List[Union[str, float]] = list()

		attribute_column.append(self.get_attribute_label(index))

		for value in self.get_float_attribute_list(index):
			attribute_column.append(value)

		return attribute_column

	def get_attribute_label(self, index: int) -> str:
		return self.attributes[index]

	def get_classlabel(self, index: int) -> str:
		return self.classlabels[index]

	def get_float_attribute_list(self, attr_index: int) -> List[float]:

		values: List[float] = list()

		for sample in self.samples:
			values.append(sample.get(attr_index).value)

		return values

	def get_list_of_list(self, append_attribute_labels: bool = True, append_classlabels: bool = True) -> List[Union[List[str], List[float]]]:

		list_of_list: List[Union[List[str], List[float]]] = list()

		if append_attribute_labels:
			attributes_row: List[str] = copy.deepcopy(self.attributes)
			if append_classlabels:
				attributes_row.append('class')
			list_of_list.append(attributes_row)

		for sample in self.samples:
			list_of_list.append(sample.get_values(append_classlabel=append_classlabels))

		return list_of_list

	def glol(self, aal: bool = True, acl: bool = True) -> List[Union[List[str], List[float]]]:
		return self.get_list_of_list(append_attribute_labels=aal, append_classlabels=acl)

	def set_float_attribute_list(self, values: List[float], attr_index: int):
		for i in range(0, self.sample_count()):
			self.samples[i].set_value(values[i], attr_index)

	def reset_attributes(self, new_attributes):

		self.attributes = copy.deepcopy(new_attributes)

		for sample in self.samples:
			sample.reset_attributes(new_attributes)

	def submatrix(self, attr_origin: int = 0, attr_bound: int = None, sample_origin: int = 0, sample_bound: int = None) -> 'DataMatrix':

		if attr_bound is None:
			attr_bound = self.attribute_count()

		if sample_bound is None:
			sample_bound = self.sample_count()

		samples: List[Sample] = list()
		attributes: List[str] or None = None
		classlabels: List[str] or None = None
		unique_classlabels: List[str] or None = None

		if self.attributes is not None:
			attributes = self.attributes[attr_origin:attr_bound]

		if self.classlabels is not None:

			unique_classlabels = list()
			classlabels = self.classlabels[sample_origin:sample_bound]

			for label in classlabels:
				if label not in unique_classlabels:
					unique_classlabels.append(label)

		for i in range(sample_origin, sample_bound + 1):
			samples.append(self.samples[i].subsample(attr_origin, attr_bound))

		return DataMatrix(
			samples,
			attributes=attributes,
			classlabels=classlabels,
			unique_classlabels=unique_classlabels,
			dataset_name=self.dataset_name
		)
