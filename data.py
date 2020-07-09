import csv
import model as m


def build_model_from_csv(filename: str, separator: str = ',', rstrip: bool = True) -> m.DataMatrix:
	return m.DataMatrix.from_list_of_list(list_of_list=csv.readcsv(filename, separator=separator, rstrip=rstrip))
