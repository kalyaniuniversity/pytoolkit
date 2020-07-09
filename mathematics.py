import math


def roundoff(value: float, decimal_place: int) -> float:
	decimal_place: float = pow(10, decimal_place)
	return math.ceil(value * decimal_place) / decimal_place
