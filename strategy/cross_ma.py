import backtrader as bt


class SMACross(bt.Strategy):
    params = {'period': 5}

    def __init__(self):
        # this can only use 'self.params.period' nor 'self.params['period']'
        self.ma = bt.ind.MovingAverageSimple(self.data, period=self.params.period)
        self.crossover = bt.ind.CrossOver(self.data,self.ma)

    def log(self, text, dt=None):
        dt = dt or self.datetime.date(0)
        print('%s, %s' % (dt.isoformat(), text))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        elif order.status == order.Completed:
            if order.isbuy():
                self.log('buy order! price= %0.2f' % order.executed.price)
            elif order.issell():
                self.log('sell order! price= %0.2f' % order.executed.price)
        elif order.status in [order.Canceled,order.Margin,order.Rejected]:
            self.log('order canceled/margin/rejected!')

    def notify_trade(self, trade):
        if trade.isclosed:
            print('pnl: %0.2f, pnl afer tax: %0.2f, tax: %0.2f' % (
                trade.pnl, trade.pnlcomm, trade.commission
            ))

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.log('buy symbol!')
                self.buy(size=100)
        elif self.crossover < 0:
            self.log('sell symbol!')
            self.sell(size=100)
        else:
            pass
