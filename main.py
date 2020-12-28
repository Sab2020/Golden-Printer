import pandas as pd
import datetime
import math
from other import jalali
import matplotlib.pyplot as plt


class tsetmc():
    @staticmethod
    def emrooz():
        y = datetime.datetime.now().year
        m = datetime.datetime.now().month
        d = datetime.datetime.now().day
        emRooz = jalali.gregorian_to_jalali(y, m, d)
        y = str(emRooz[0])
        m = str(emRooz[1])
        d = str(emRooz[2])
        if (emRooz[1]) < 10:
            m = '0' + str(emRooz[1])
        if (emRooz[2]) < 10:
            d = '0' + str(emRooz[2])
        seq = (y, m, d)
        s = ''
        EndEmRooz = s.join(seq)
        return EndEmRooz

    def startAnalyze(self):
        f = open("tickers_data/"++".csv")

        return


    def calRsi(period, namad_name):
        saina = pd.read_csv("tickers_data/" + namad_name + ".csv")
        f = saina.tail(period)
        f = f.set_index("jdate")

        f['dayGrowth'] = f['adjClose'] - f['open']

        manfi = 0
        mosbat = 0

        f['dayStat'] = f['dayGrowth'] > 0

        s = period - 1
        while s > -1:
            if (f.iloc[s, 10]) == False:
                manfi += f.iloc[s, 9]
            elif (f.iloc[s, 10]) == True:
                mosbat += f.iloc[s, 9]
            s -= 1

        print(f)
        print("Mosbat :" + str(mosbat))
        print("Manfi :" + str(manfi))
        rs = math.fabs(mosbat / manfi)
        print("Rs :" + str(rs))

        rsi = 100 - ((100) / (1 + rs))
        print("RSI : " + str(rsi))

        # print(f['dayGrowth'].head(14).sum())
        # f['adjClose'].plot()
        # plt.show()
        return


t = tsetmc
t.calRsi(15, "ساینا")
