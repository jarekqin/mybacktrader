from strategy.double_sma_cross import DoubleSMACross
from datetime import datetime

import backtrader as bt
import os

cerebro=bt.Cerebro()
basic_path='/media/star/middle data/backtrader_data'
read_file=os.path.join(basic_path,'600000.csv')


data=bt.feeds.GenericCSVData(
    dataname=read_file,
    datetime=0,
    open=2,
    high=3,
    low=4,
    close=5,
    volume=6,
    openinterest=-1,
    dtformat=('%Y-%m-%d'),
    fromdate=datetime(2000,1,1),
    todate=datetime(2014,7,8))
cerebro.adddata(data)
cerebro.addstrategy(DoubleSMACross)
cerebro.broker.setcash(10000.0)
cerebro.broker.setcommission(0.001)
cerebro.broker.set_slippage_fixed(0.05)
print('original market value: %0.2f'  % cerebro.broker.get_value())
cerebro.run()
print('final market value: %0.2f' % cerebro.broker.get_value())
cerebro.plot(style='bar')