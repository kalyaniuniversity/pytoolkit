import data
import model


def dlbcl() -> model.DataMatrix:
	return data.build_model_from_csv('sample_datasets/dlbcl-fl.csv')


def leukemia() -> model.DataMatrix:
	return data.build_model_from_csv('sample_datasets/leukemia.csv')


def gse412() -> model.DataMatrix:
	return data.build_model_from_csv('sample_datasets/GSE412.csv')
