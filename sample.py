from typing import List, Union
from datapoint import DataPoint
import copy


class Sample:

	datapoints: List[DataPoint] = None
	associated_attributes: List[str] or None = None
	classlabel: str or None = None

	def __init__(self, datapoints: List[DataPoint], associated_attributes: List[str] = None, classlabel: str = None):
		self.datapoints = datapoints
		self.associated_attributes = associated_attributes
		self.classlabel = classlabel

	@classmethod
	def from_values(cls, values: List[float], associated_attributes: List[str], classlabel: str) -> 'Sample':

		datapoints: List[DataPoint] = list()

		for i in range(0, len(values)):
			datapoints.append(DataPoint(values[i], associated_attributes[i], classlabel))

		return cls(datapoints, associated_attributes=associated_attributes, classlabel=classlabel)

	def length(self) -> int:
		return len(self.datapoints)

	def get(self, index: int) -> DataPoint:
		return self.datapoints[index]

	def get_datapoints(self, indices: List[int]) -> List[DataPoint]:

		datapoints: List[DataPoint] = list()

		for index in indices:
			datapoints.append(copy.deepcopy(self.datapoints[index]))

		return datapoints

	def get_values(self, append_classlabel: bool = False) -> List[float] or List[Union[float, str]]:

		values: List[float] or List[Union[float, str]] = list()

		for datapoint in self.datapoints:
			values.append(datapoint.value)

		if append_classlabel:
			values.append(self.classlabel)

		return values

	def set(self, datapoint: DataPoint, index: int):
		self.datapoints[index] = datapoint

	def set_value(self, value: float, index: int):
		self.datapoints[index].value = value

	def reset_attributes(self, new_attributes: List[str]):

		self.associated_attributes = copy.deepcopy(new_attributes)

		for i in range(0, len(new_attributes)):
			self.datapoints[i].associated_attribute = new_attributes[i]

	def subsample(self, origin: int = 0, bound: int = None):

		if bound is None:
			bound = self.length()

		datapoints: List[DataPoint] = copy.deepcopy(self.datapoints[origin:bound])
		attributes: List[str] = copy.deepcopy(self.associated_attributes[origin:bound])

		return Sample(datapoints, associated_attributes=attributes, classlabel=self.classlabel)
