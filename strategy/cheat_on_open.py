import datetime
import backtrader as bt


class St(bt.Strategy):
    params = dict(
        periods=[10, 30],
        matype=bt.ind.SMA,
    )

    def __init__(self):
        self.cheating = self.cerebro.position.cheat_on_open
        mas = [self.position.matype(period=x) for x in self.position.periods]
        self.signal = bt.ind.CrossOver(*mas)
        self.order = None

    def notify_order(self, order):
        if order.status != order.Completed:
            return

        self.order = None

    def operate(self, fromopen):
        if self.order is None:
            return
        elif self.position:
            if self.signal < 0:
                self.order = self.close()
        elif self.signal > 0:
            print(f'{self.data.datetime.date()} Send Buy,fromopen{fromopen},close {self.data.close[0]}')
            self.order=self.buy()
        self.order=self.buy()


    def next(self):
        if self.cheating:
            return

        print(f'{self.data.datetime.date()} next,open {self.data.open[0]} close {self.data.close[0]}')

        self.operate(fromopen=False)

    def next_open(self):
        if not self.cheating:
            return

        print(f'{self.data.datetime.date()} next_open,open {self.data.open[0]} close {self.data.close[0]}')
        self.operate(fromopen=True)


