import backtrader as bt
from datetime import timedelta


class SimpleSMA(bt.Strategy):
    params = dict(period=5)

    def __init__(self):
        self.ma = bt.ind.MovingAverageSimple(self.data, period=self.params.period)
        self.order = None

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
        self.order = None

    def nofity_trade(self, trade):
        print('trade')
        for h in trade.history:
            print('status:',h.status)
            print('event:',h.event)
        if trade.isclosed:
            print('original return %0.2f, return after taxies %0.2f,cost is %0.2f' % (
                trade.pnl, trade.pnlcomm, trade.commission
            ))

    def start(self):
        print('start')

    def stop(self):
        print('stop')

    def prenext(self):
        self.log('pre-next')

    def nextstart(self):
        self.log('next-start')
        self.next()

    def next(self):
        # if system has unactive order, then no needs to create new order.
        # return to next bar directly
        if self.order:
            return
        # or we can cancel pending order when xx rounds bar start calculate
        # self.cancel(self.order)
        if not self.position:
            if self.data.close[-1] < self.ma[-1] and self.data.close[0] >= self.ma[0]:
                self.log('create buy order')
                # inteference order
                validday = self.data.datetime.datetime(0) + timedelta(days=7)
                self.order = self.buy(size=100, exectype=bt.Order.Limit, price=0.99 * self.data.close[0],
                                      valid=validday)
        elif self.data.close[-1] > self.ma[-1] and self.data.close[0] <= self.ma[0]:
            self.log('create sell order')
            self.order = self.sell(size=100)
