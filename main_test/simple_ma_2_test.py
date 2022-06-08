from strategy.simple_sma_2 import SimpleSMA
from datetime import datetime

import backtrader as bt
import os

cerebro=bt.Cerebro()
basic_path='/media/star/data/backtrader_data'
read_file=os.path.join(basic_path,'600000qfq.csv')


data=bt.feeds.GenericCSVData(
    dataname=read_file,
    datetime=2,
    open=3,
    high=4,
    low=5,
    close=6,
    volume=10,
    openinterest=-1,
    dtformat=('%Y%m%d'),
    fromdate=datetime(2019,1,1),
    todate=datetime(2020,7,8))
cerebro.adddata(data)
cerebro.addstrategy(SimpleSMA)
cerebro.broker.setcash(10000.0)
cerebro.broker.setcommission(0.001)
cerebro.broker.set_slippage_fixed(0.05)
print('original market value: %0.2f'  % cerebro.broker.get_value())
cerebro.run()
print('final market value: %0.2f' % cerebro.broker.get_value())
cerebro.plot(style='bar')