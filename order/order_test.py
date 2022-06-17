import datetime
import os

import backtrader as bt


class OrderExecutionStrategy(bt.Strategy):
    params = (
        ('smaperiod', 15),
        ('exectype', 'Market'),
        ('perc1', 3),
        ('perc2', 1),
        ('valid', 4),
    )

    def __init__(self):
        sma = bt.ind.SMA(period=self.params.smaperiod)
        self.buysell = bt.ind.CrossOver(self.data.close, sma, plot=True)

    def log(self, text, dt=None):
        dt = dt or self.data.datetime[0]
        if isinstance(dt, float):
            dt = bt.num2date(dt)
        print('%s,%s' % (dt.isoformat(), text))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            self.log('Order accepted/sumbmitted', dt=order.created.dt)
            self.order = order
            return
        if order.status == order.Expired:
            self.log('Buy expired')
        elif order.status == order.Completed:
            if order.isbuy():
                self.log('Buy executed,price: %0.2f, Cose: %0.2f, Comm %0.2f' % (
                    order.executed.price, order.executed.value, order.executed.comm))
            else:
                self.log('Sell executed,price: %0.2f, Cose: %0.2f, Comm %0.2f' % (
                    order.executed.price, order.executed.value, order.executed.comm))

    def next(self):
        if self.position:
            if self.buysell < 0:
                self.log('Sell create, %0.2f' % self.data.close[0])
                self.sell()
        elif self.buysell > 0:
            if self.params.valid:
                valid = self.data.datetime.datetime(0) + datetime.timedelta(days=self.params.valid)
            else:
                valid = None
            if self.params.exectype == 'Market':
                self.order = self.buy(exectype=bt.Order.Market)
                self.log('Buy created,exectype Market, price: %0.2f' % self.data.close[0])

            elif self.params.exectype == 'Close':
                self.order = self.buy(exectype=bt.Order.Market)
                self.log('Buy created,exectype Close, price: %0.2f' % self.data.close[0])

            elif self.params.exectype == 'Limit':
                price = self.data.close * (1. - self.params.perc1 / 100.)
                self.order = self.buy(exectype=bt.Order.Limit, price=price, valid=valid)
                if self.params.valid:
                    self.log('Buy created,exectype Limit, price: %0.2f,valid: %s' % (price, valid.strftime('%Y-%m-%d')))
                else:
                    self.log('Buy created,exectype Stop, price: %0.2f' % price)

            elif self.params.exectype == 'Stop':
                price = self.data.close * (1. + self.params.perc1 / 100.)
                self.order = self.buy(exectype=bt.Order.Stop, price=price, valid=valid)
                if self.params.valid:
                    self.log('Buy created,exectype Stop, price: %0.2f,valid: %s' % (price, valid.strftime('%Y-%m-%d')))
                else:
                    self.log('Buy created,exectype Stop, price: %0.2f' % price)


            elif self.params.exectype == 'StopLimit':
                price = self.data.close * (1. + self.params.perc1 / 100.)
                plimit = self.data.close * (1. + self.params.perc2 / 100.)
                self.order = self.buy(exectype=bt.Order.StopLimit, price=price, valid=valid, plimit=plimit)
                if self.params.valid:
                    self.log('Buy created,exectype StopLimit, price: %0.2f,valid: %s,pricelimit: %0.2f' % (
                        price, valid.strftime('%Y-%m-%d'), plimit))
                else:
                    self.log('Buy created,exectype StopLimit, price: %0.2f, pricelimit:%0.2f' % (price, plimit))



if __name__=='__main__':
    cerebro=bt.Cerebro()

    basic_path = '/media/shai/项目数据存放处/backtrader_data'
    read_file = os.path.join(basic_path, '600000qfq.csv')
    read_file2 = os.path.join(basic_path, 'benchmark.csv')

    # cerebro.addobserver(bt.observers.DrawDown)

    data = bt.feeds.GenericCSVData(
        dataname=read_file,
        datetime=2,
        open=3,
        high=4,
        low=5,
        close=6,
        volume=10,
        openinterest=-1,
        dtformat=('%Y%m%d'),
        fromdate=datetime.datetime(2019, 1, 1),
        todate=datetime.datetime(2020, 7, 8))

    cerebro.adddata(data)
    cerebro.addstrategy(OrderExecutionStrategy,exectype='Market',perc1=1,perc2=2,valid=2,smaperiod=5)
    cerebro.run()
