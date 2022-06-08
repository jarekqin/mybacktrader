from strategy.kelly_sma_cross import SmaCross
from datetime import datetime
from tabulate import tabulate
# from utils.analyser_output_toolkits import printTradeAnalysis

import backtrader as bt
import os
import quantstats as qs

cerebro = bt.Cerebro(tradehistory=True)
basic_path = '/media/shai/项目数据存放处/backtrader_data'
read_file = os.path.join(basic_path, '600000qfq.csv')

data = bt.feeds.GenericCSVData(
    dataname=read_file,
    datetime=2,
    open=3,
    high=4,
    low=5,
    close=6,
    volume=10,
    openinterest=-1,
    dtformat=('%Y%m%d'),
    fromdate=datetime(2019, 3, 1),
    todate=datetime(2020, 5, 1))

cerebro.adddata(data)
cerebro.addstrategy(SmaCross)
cerebro.broker.setcash(10000.0)
cerebro.addanalyzer(bt.analyzers.Kelly,_name='kelly')
cerebro.addanalyzer(bt.analyzers.TradeList,_name='trade_list')
thestarts=cerebro.run()
thestart=thestarts[0]

trade_list=thestart.analyzers.trade_list.get_analysis()
print('kelly: ',thestart.analyzers.kelly.get_analysis())
for a in thestart.analyzers:
    a.print()

print(tabulate(trade_list,headers='keys'))