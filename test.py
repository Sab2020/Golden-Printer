import math
import pytse_client as tse
import pandas as pd
import datetime
import matplotlib.pyplot as plt

print("Start...")
tickers = tse.download(symbols="all", include_jdate=True, write_to_csv=True)
# tickers = tse.download(symbols="ساینا", include_jdate=True, write_to_csv=True)
# print(tickers)

a = -3
b = math.fabs(a)
print(b)
