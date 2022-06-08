import backtrader as bt



class SimpleSMA(bt.Strategy):
    params = dict(period=5)

    def __init__(self):
        self.ma = bt.ind.MovingAverageSimple(self.data, period=self.params.period)

    def next(self):
        if not self.position:
            if self.data.close[-1]<self.ma[-1] and self.data[0]>self.ma[0]:
                self.buy(size=100)
            elif self.data.close[-1]>self.ma[-1] and self.data[0]<self.ma[0]:
                self.sell(size=100)
