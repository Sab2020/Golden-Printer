import math
import pandas as pd
import technic as ta

s = pd.read_csv("tickers_data/شوینده.csv")
c = s.open.count()

rsi = ta.trsi(s['adjClose'], 14)
print(rsi.tail(1).item())
print(type(rsi))
