from strategy.cross_ma import SMACross
from datetime import datetime
from utils.analyser_output_toolkits import printTradeAnalysis

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
    fromdate=datetime(2019, 1, 1),
    todate=datetime(2020, 7, 8))

cerebro.adddata(data)
cerebro.addstrategy(SMACross)
cerebro.broker.setcash(100000)
# cerebro.broker.setcommission(0.001)
# cerebro.broker.set_slippage_fixed(0.05)
print('original market value: %0.2f' % cerebro.broker.get_value())
# preload if is False means that strategy will not load whole data into memory
# exactbars will load how many real bars we have to use and banned for plotting with no enough bars to plot
# cerebro=bt.Cerebro(runonce=False,exactbars=0) has same function to below setense

# add analyst module
# cerebro.addanalyzer(bt.analyzers.SharpeRatio,riskfreerate=0.01,annualize=True,_name='sharp_ratio')
# cerebro.addanalyzer(bt.analyzers.AnnualReturn,_name='annual_return')
# cerebro.addanalyzer(bt.analyzers.DrawDown,_name='drawdown')
# cerebro.addanalyzer(bt.analyzers.TradeAnalyzer,_name='trade_analyser')
# thestrats=cerebro.run()
# thestrat=thestrats[0]

# print('SR: ',thestrat.analyzers.sharp_ratio.get_analysis()['sharperatio'])
# print('max draw_down: ',thestrat.analyzers.drawdown.get_analysis()['max']['drawdown'])
# print('annual return: ',thestrat.analyzers.annual_return.get_analysis())

# for a in thestrat.analyzers:
#     # print whole analised results
#     a.print()
#     # print dict
#     # a.pprint()

#  observator
cerebro.addobserver(bt.observers.Broker)
cerebro.addobserver(bt.observers.BuySell)
cerebro.addobserver(bt.observers.Value)
cerebro.addobserver(bt.observers.DrawDown)
cerebro.addobserver(bt.observers.Trades)

cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='ta')
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
cerebro.addanalyzer(
    bt.analyzers.SharpeRatio, _name='sharp ratio', riskfreerate=0.0, annualize=True,
    timeframe=bt.TimeFrame.Days
)
cerebro.addanalyzer(bt.analyzers.VWR, _name='vwr')
cerebro.addanalyzer(bt.analyzers.SQN, _name='sqn')
cerebro.addanalyzer(bt.analyzers.Transactions, _name='txn')
cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='timereturn', timeframe=bt.TimeFrame.Days, data=data)
cerebro.addanalyzer(bt.analyzers.PyFolio, _name='PyFolio')

backtest = cerebro.run()
backtest_result = backtest[0]

printTradeAnalysis(cerebro, backtest_result.analyzers)

portfilio_stats = backtest_result.analyzers.getbyname('PyFolio')
returns, positions, transations, gross_lev = portfilio_stats.get_pf_items()
returns.index = returns.index.tz_convert(None)

qs.reports.html(returns, output='stats.html', title='SMA ports', rf=0.0)

backtest_result.analyzers.timereturn.print()

cerebro.plot(style='candlestick', volume=False)
