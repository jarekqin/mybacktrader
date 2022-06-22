from strategy.cheat_on_open import St
import backtrader as bt
import os


cerebro=bt.Cerebro(cheat_on_open=True)
basic_path = '/media/shai/项目数据存放处/backtrader_data/samples/datas'
read_file = os.path.join(basic_path, '2005-2006-day-001.txt')


data = bt.feeds.GenericCSVData(dataname=read_file)
cerebro.adddata(data)
cerebro.broker.add_cash(10000)
cerebro.addstrategy(St)
cerebro.run()