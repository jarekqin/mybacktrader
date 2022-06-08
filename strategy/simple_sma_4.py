import backtrader as bt
from datetime import datetime


class SMA(bt.Strategy):
    params = {'period': 5}

    def __init__(self):
        print('__init__')
        self.ma = bt.ind.MovingAverageSimple(self.data, period=self.params.period)

    def log(self, text, dt=None):
        dt = dt or self.datetime.date(0)
        print('%s, %s' % (dt.isoformat(), text))

    def notify_order(self, order):
        self.log('order status %s' % order.getstatusname())

    def nofity_trade(self, trade):
        for h in trade.history:
            print(h.event)
        status_names = ['Created', 'Open', 'CLosed']
        self.log('trade status %s' % status_names[trade.status])

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
        self.log('next')
        if not self.position:
            if self.data.close[-1] < self.ma[-1] and \
                    self.data.close[0] >= self.ma[0]:
                self.log('buy order!')
                self.buy(size=100)
        elif self.data.close[0] < self.ma[0] and \
                self.data.close[-1] >= self.ma[-1]:
            self.log('sell order!')
            self.sell(size=100)
