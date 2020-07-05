import copy
from typing import List


class DataPoint:

	value = None
	associated_attribute = None
	associated_classlabel = None

	def __init__(self, value: float, associated_attribute=None, associated_classlabel=None):
		self.value = value
		self.associated_attribute = associated_attribute
		self.associated_classlabel = associated_classlabel


class Sample:

	datapoints = None
	associated_attributes = None
	classlabel = None

	def __init__(self, datapoints: List[DataPoint], associated_attributes=None, classlabel=None):
		self.datapoints = datapoints
		self.associated_attributes = associated_attributes
		self.classlabel = classlabel

	@classmethod
	def from_values(cls, values: List[float], associated_attributes: List[str], classlabel: str) -> 'Sample':

		datapoints = list()

		for i in range(0, len(values)):
			datapoints.append(DataPoint(values[i], associated_attributes[i], classlabel))

		return cls(datapoints, associated_attributes=associated_attributes, classlabel=classlabel)

	def length(self) -> int:
		return len(self.datapoints)

	def get(self, index: int) -> DataPoint:
		return self.datapoints[index]

	def set(self, datapoint: DataPoint, index: int):
		self.datapoints[index] = datapoint

	def set_value(self, value: float, index: int):
		self.datapoints[index].value = value


class DataMatrix:

	samples = None
	attributes = None
	classlabels = None
	dataset_name = None

	def __init__(self, samples: List[Sample], attributes=None, classlabels=None, dataset_name=None):
		self.samples = samples
		self.attributes = attributes
		self.classlabels = classlabels
		self.dataset_name = dataset_name

	@classmethod
	def from_list_of_list(cls, list_of_list: List[List[str]], has_attributes=True, has_classlabels=True) -> 'DataMatrix':

		samples = list()
		attributes = None
		classlabels = None

		if has_attributes:
			attributes = copy.deepcopy(list_of_list[0][:-1])
			list_of_list.pop(0)

		if has_classlabels:
			classlabels = list()

		for row in list_of_list:
			label = row[-1]
			samples.append(Sample.from_values(values=[float(i) for i in row[:-1]], associated_attributes=attributes, classlabel=label))
			if has_classlabels:
				classlabels.append(label)

		return cls(samples, attributes=attributes, classlabels=classlabels)

	def sample_count(self) -> int:
		return len(self.samples)

	def attribute_count(self) -> int:
		return len(self.attributes)

	def get_float_attribute_list(self, attr_index: int) -> List[float]:

		values = list()

		for sample in self.samples:
			values.append(sample.get(attr_index).value)

		return values

	def set_float_attribute_list(self, values: List[float], attr_index: int):
		for i in range(0, self.sample_count()):
			self.samples[i].set_value(values[i], i)
