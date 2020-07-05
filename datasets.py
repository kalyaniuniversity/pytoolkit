import data
import model


def dlbcl() -> model.DataMatrix:
	return data.build_model_from_csv('sample_datasets/dlbcl.csv')
