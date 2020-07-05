import statistics as st


zscore = lambda value, value_list: (value - st.mean(value_list)) / st.stdev(value_list)


minmax = lambda value, actual_min, actual_max, normalized_min, normalized_max: \
	(((value - actual_min) / (actual_max - actual_min)) * (normalized_max - normalized_min)) + normalized_min
