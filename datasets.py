import data
import model


def dlbcl() -> model.DataMatrix:
	return data.build_model_from_csv('sample_datasets/dlbcl-fl.csv')


def leukemia() -> model.DataMatrix:
	return data.build_model_from_csv('sample_datasets/leukemia.csv')


def gse412() -> model.DataMatrix:
	return data.build_model_from_csv('sample_datasets/GSE412.csv')


def bmmcaml() -> model.DataMatrix:
	return data.build_model_from_csv('sample_datasets/bmmc-aml.csv')


def gse75140binary() -> model.DataMatrix:
	return data.build_model_from_csv('sample_datasets/GSE75140-binary.csv')


def pbmc3kprocessed() -> model.DataMatrix:
	return data.build_model_from_csv('sample_datasets/pbmc3k-processed.csv')
