class DataPoint:

	value: float = None
	associated_attribute: str or None = None
	associated_classlabel: str or None = None

	def __init__(self, value: float, associated_attribute: str = None, associated_classlabel: str = None):
		self.value = value
		self.associated_attribute = associated_attribute
		self.associated_classlabel = associated_classlabel
