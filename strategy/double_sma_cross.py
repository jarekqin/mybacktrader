import backtrader as bt


class DoubleSMACross(bt.Strategy):
    params=dict(fast_period=5,slow_period=10,)

    def __init__(self):
        fast_ma=bt.ind.MovingAverageSimple(period=self.params.fast_period)
        slow_ma=bt.ind.MovingAverageSimple(period=self.params.slow_period)

        self.crossover=bt.ind.CrossOver(fast_ma,slow_ma)

        self.order=None


    def next(self):
        self.cancel(self.order)

        if not self.position:
            if self.crossover>0:
                self.order=self.buy(size=100)
        elif self.crossover<0:
            self.order=self.sell(size=100)
            