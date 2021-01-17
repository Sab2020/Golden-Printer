import pandas as pd
import datetime
import math
from other import jalali
import pytse_client as tse
import technic as ta
from pathlib import Path


class TseTmc:
    @staticmethod
    def emrooz():
        y = datetime.datetime.now().year
        m = datetime.datetime.now().month
        d = datetime.datetime.now().day
        today = jalali.gregorian_to_jalali(y, m, d)
        y = str(today[0])
        m = str(today[1])
        d = str(today[2])
        if (today[1]) < 10:
            m = '0' + str(today[1])
        if (today[2]) < 10:
            d = '0' + str(today[2])
        seq = (y, m, d)
        s = ''
        endemrooz = s.join(seq)
        return endemrooz

    def __init__(self):
        print("Welcome To Golden Printer.")

    def get_last_date(self, namad_name):
        da = pd.read_csv("tickers_data/" + namad_name + ".csv")
        ld = da['jdate'].tail(1).values

        return ld

    def chart_sym(self, sym, period):
        # symbol = pd.read_csv('tickers_data/' + str(sym) + '.csv')
        # sb.lineplot(x=symbol['jdate'], y=symbol['adjClose'], ci=None, data=tips)
        print(period + sym)
        return

    def get_data(self):
        print("Start...")
        tse.download(symbols="all", include_jdate=True, write_to_csv=True)
        print("Done...")
        return

    def start_analyze(self, rooz):
        csv_folder = Path('tickers_data/').rglob('*.csv')
        files = [x for x in csv_folder]
        file_name = str(rooz).replace('[', '')
        file_name = file_name.replace(']', '')
        file_name = file_name.replace('\'', '')
        print(file_name)
        for name in files:
            symbol = pd.read_csv(str(name))
            # print(symbol)
            rsi = ta.trsi(symbol['adjClose'], 14)
            if (rsi.tail(1).item()) < 20:
                print(name)
                with open('signal/' + file_name + '.txt', 'a', encoding="utf-8") as f:
                    f.write(str(name.name.title() + " = " + str(rsi.tail(1).item()) + "\n"))
                    print(rsi.tail(1).item())
                f.close()

        return

    def ini_csv(self, name_namad, period):
        symbol = pd.read_csv("tickers_data/" + str(name_namad) + ".csv")
        symbol = symbol.set_index("jdate")
        symbol['dayGrowth'] = symbol['adjClose'] - symbol['open']
        symbol['dayStat'] = symbol['dayGrowth'] > 0
        symbol['smmap'] = 0
        symbol['smman'] = 0

        num = symbol.open.count()
        smap = 0
        sman = 0
        # set First Step
        p = period
        while p > 0:
            if not (symbol.iloc[p, 10]):
                sman += symbol.iloc[p, 9]
            elif symbol.iloc[p, 10]:
                smap += symbol.iloc[p, 9]
            p -= 1
        print('sman :' + str(sman))
        print('smap :' + str(smap))
        print(symbol.head(15))
        start = num - period
        while start > 0:
            if not (symbol.iloc[start, 10]):
                sman += symbol.iloc[start, 9]
            elif symbol.iloc[start, 10]:
                smap += symbol.iloc[start, 9]
            start -= 1
        return

    def cal_rsi(self, period, namad_name):
        saina = pd.read_csv("tickers_data/" + namad_name + ".csv")
        f = saina.tail(period)
        f = f.set_index("jdate")
        f['dayGrowth'] = f['adjClose'] - f['open']
        manfi = 0
        mosbat = 0
        f['dayStat'] = f['dayGrowth'] > 0
        s = period - 1
        while s > -1:
            if not (f.iloc[s, 10]):
                manfi += f.iloc[s, 9]
            elif f.iloc[s, 10]:
                mosbat += f.iloc[s, 9]
            s -= 1
        print(f)
        print("Mosbat :" + str(mosbat))
        print("Manfi :" + str(manfi))
        rs = math.fabs(mosbat / manfi)
        print("Rs :" + str(rs))
        rsi = 100 - (100 / (1 + rs))
        print("RSI : " + str(rsi))
        # print(f['dayGrowth'].head(14).sum())
        # f['adjClose'].plot()
        # plt.show()
        return


t = TseTmc()
# t.get_data()

r = t.get_last_date('ساینا')
t.start_analyze(r)
