import backtrader as bt
import math


class OverUnderMovAv(bt.Indicator):
    lines = ('over', 'under')
    params = dict(period=20)

    def __init__(self):
        movav = bt.ind.MovingAverageSimple(self.data, period=self.params.period)
        self.lines.over = movav + 10
        self.linew.under = movav - 10

class SimpleMovingAverage1(bt.Indicator):
    lines=('sma',)
    params=(('period',20),)

    def __init__(self):
        self.addminperiod(self.params.period)


    def next(self):
        datasum=math.fsum(self.data.get(size=self.params.period))
        self.lines.sma[0]=datasum/self.params.period