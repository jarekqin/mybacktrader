from __future__ import (absolute_import, division, print_function, unicode_literals)
import backtrader as bt


class OrderObserver(bt.observers.Observer):
    lines = ('created', 'expired')
    plotinfo = dict(plot=True, subplot=True, plotlintlabels=True)
    plotlines = dict(
        created=dict(marker='*', markersize=8., color='lime', fillstyle='full'),
        expired=dict(marker='s', markersize=8., color='red', fillsytle='full'))

    def next(self):
        for order in self._ower._orderspending:
            if order.data != self.data:
                continue
            if not order.isbuy():
                continue
            if order.status in [bt.Order.Accepted,bt.Order.Submitted]:
                self.lines.created[0]=order.recrated.price
            elif order.status== bt.Order.Expired:
                self.lines.expired[0]=order.created.price
