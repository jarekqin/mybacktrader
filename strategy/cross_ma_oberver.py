import backtrader as bt
from datetime import datetime


# 创建策略类
class SmaCross(bt.Strategy):
    # 定义参数
    params = dict(period=5  # 移动平均期数
                  )

    # 日志函数
    def log(self, txt, dt=None):
        '''日志函数'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # 订单状态 submitted/accepted，无动作
            return

        # 订单完成
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('买单执行, %.2f' % order.executed.price)

            elif order.issell():
                self.log('卖单执行, %.2f' % order.executed.price)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('订单 Canceled/Margin/Rejected')

    # 记录交易收益情况（可省略，默认不输出结果）
    def notify_trade(self, trade):
        if trade.isclosed:
            self.log('毛收益 %0.2f, 扣佣后收益 % 0.2f, 佣金 %.2f' %
                     (trade.pnl, trade.pnlcomm, trade.commission))

    def __init__(self):
        # 移动平均线指标
        # self.move_average = bt.ind.MovingAverageSimple(self.data, period=self.params.period, subplot=True,
        #                                                plotname='mysma')
        # use talib function
        self.move_average=bt.talib.SMA(self.data,timeperiod=self.p.period)

        # set plot
        # set plot name
        # preferred set into above
        # self.move_average.plotinfo.plotname = 'mysma'
        # # set plotted at independent subplot
        # self.move_average.plotinfo.subplot = True
        # self.move_average.plotinfo.plotmaster = self.data


def next(self):
    # 输出回撤值，今日的drawdown还没有，故输出昨日的
    self.log(f'Benchmark: {self.stats.benchmark.benchmark[0]:.2f}')
    self.log(f'Broker: {self.stats.broker.cash[0]:.2f}')
    self.log(f'BuySell: {self.stats.buysell.buy[0]:.2f}')
    self.log(f'DrawDown: {self.stats.drawdown.drawdown[0]:.2f}')
    self.log(f'TimeReturn: {self.stats.timereturn.timereturn[0]:.2f}')
    self.log(f'Trades: {self.stats.trades.pnlplus[0]:.2f}')
    # self.log(f'LogReturns: {self.stats.logreturns.logret1[0]:.2f}')

    if not self.position:  # 还没有仓位
        # 当日收盘价上穿5日均线，创建买单，买入100股
        if self.data.close[
            -1] < self.move_average[-1] and self.data > self.move_average:
            self.log('创建买单')
            self.buy(size=100)
    # 有仓位，并且当日收盘价下破5日均线，创建卖单，卖出100股
    elif self.data.close[
        -1] > self.move_average[-1] and self.data < self.move_average:
        self.log('创建卖单')
        self.sell(size=100)
