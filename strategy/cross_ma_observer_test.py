from strategy.cross_ma_oberver import SmaCross,LongOnly
from datetime import datetime
from utils.analyser_output_toolkits import printTradeAnalysis

import backtrader as bt
import os
import quantstats as qs

cerebro = bt.Cerebro(stdstats=False)
basic_path = '/media/shai/项目数据存放处/backtrader_data'
read_file = os.path.join(basic_path, '600000qfq.csv')
read_file2 = os.path.join(basic_path, 'benchmark.csv')

# cerebro.addobserver(bt.observers.DrawDown)

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
    fromdate=datetime(2010, 1, 1),
    todate=datetime(2019, 7, 8))

cerebro.adddata(data)

# benchmark = bt.feeds.GenericCSVData(
#     dataname=read_file2,
#     datetime=2,
#     open=3,
#     high=4,
#     low=5,
#     close=6,
#     volume=10,
#     openinterest=-1,
#     dtformat=('%Y%m%d'),
#     fromdate=datetime(2010, 1, 1),
#     todate=datetime(2019, 7, 8))

# cerebro.adddata(benchmark)
cerebro.addstrategy(SmaCross)
cerebro.addsizer(LongOnly)
cerebro.broker.setcash(100000)
cerebro.broker.setcommission(0.001)
cerebro.broker.set_slippage_fixed(0.05)
# cerebro.broker.setcommission(0.001)
# cerebro.broker.set_slippage_fixed(0.05)

# cerebro.addobserver(bt.observers.Benchmark, data=benchmark, timeframe=bt.TimeFrame.NoTimeFrame)
# cerebro.addobserver(bt.observers.TimeReturn, timeframe=bt.TimeFrame.NoTimeFrame)
# cerebro.addobserver(bt.observers.Broker)
# cerebro.addobserver(bt.observers.BuySell)
# cerebro.addobserver(bt.observers.DrawDown)
# cerebro.addobserver(bt.observers.Trades)
# cerebro.addobserver(bt.observers.LogReturns, timeframe=bt.TimeFrame.NoTimeFrame, compression=1)
# cerebro.addobserver(bt.observers.LogReturns2, timeframe=bt.TimeFrame.NoTimeFrame, compression=1)

print('original market value: %0.2f' % cerebro.broker.get_value())
cerebro.run()
print('final market value: %0.2f' % cerebro.broker.get_value())
cerebro.plot()
