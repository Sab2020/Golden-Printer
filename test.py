import pandas as pd
da = pd.read_csv("tickers_data/شوینده.csv")
ld = da['jdate'].tail(1).values

print(ld)
