import pandas as pd
import numpy as np
import sklearn

stock = pd.read_csv("tickers_data/ساینا.csv", sep=",")
stock["perd"] = 0

print(stock)
predict = "perd"

x = np.array(stock.drop([predict], 1))
y = np.array(stock[predict])

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1)
