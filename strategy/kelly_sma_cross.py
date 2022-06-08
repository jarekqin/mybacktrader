from datetime import datetime

import backtrader as bt


class SmaCross(bt.Strategy):
    params = dict(period=2)

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s,%s' % (dt.isoformat(), txt))

    def __init__(self):
        self.move_average = bt.ind.MovingAverageSimple(self.data.close, period=self.params.period)

    def next(self):
        if not self.position:
            if self.data.close[-1] < self.move_average.sma[-1] and \
                    self.data.close[0] >= self.move_average.sma[0]:
                self.buy(size=100)
        elif self.data.close[-1] > self.move_average.sma[-1] and \
                self.data.close[0] <= self.move_average.sma[0]:
            self.sell(size=100)
