import backtrader as bt


class SimpleSMA(bt.Strategy):
    params = dict(period=5)

    def __init__(self):
        self.ma = bt.ind.MovingAverageSimple(self.data, period=self.params.period)

    def log(self, text, dt=None):
        dt = dt or self.datetime.date(0)
        print('%s, %s' % (dt.isoformat(), text))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status == order.Completed:
            if order.isbuy():
                self.log(f'buy order programming! price{round(order.executed.price, 2)},'
                         f'size {order.executed.size} cost {round(order.executed.value, 2)}')
            elif order.issell():
                self.log(f'sell order programming! price{round(order.executed.price, 2)},'
                         f'size {order.executed.size} cost {round(order.executed.value, 2)}')
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('order canceled/margin/rejected')

    def nofity_trade(self, trade):
        print('trade')
        if trade.isclosed:
            print('original return %0.2f, return after taxies %0.2f,cost is %0.2f' % (
                trade.pnl, trade.pnlcomm, trade.commission
            ))

    def next(self):
        if not self.position:
            if self.data.close[-1] < self.ma[-1] and self.data[0] > self.ma[0]:
                self.log('create buy order')
                self.buy(size=100)
        elif self.data.close[-1] > self.ma[-1] and self.data[0] < self.ma[0]:
            self.log('create sell order')
            self.sell(size=100)
