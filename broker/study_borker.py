import backtrader as bt


class StampDutyCommissionScheme(bt.CommissionInfo):
    params = (
        ('stamp_duty', 0.005),
        ('percabs', True)
    )

    def _getcommission(self, size, price, pseudoexec):
        if size > 0:
            return size * price * self.p.commission
        elif size < 0:
            return -size * price * (self.p.stamp_duty + self.p.commission)
        else:
            return 0


# Chinese Futures commission fee module
class ChineseFuturesCommissionSchemeValue(bt.CommissionInfo):
    params=(
        ('percabs',True),
        ('commtype',bt.CommissionInfo.COMM_PERC),
        ('stocklike',False),
    )

    def _getcommission(self, size, price, pseudoexec):
        abscommission=size*price*self.p.mulrt*self.p.commission
        return abs(abscommission)


class ChineseFuturesCommissionSchemeSize(bt.CommissionInfo):
    params = (
        ('commtype', bt.CommissionInfo.COMM_PERC),
        ('stocklike', False),
    )

    def _getcommission(self, size, price, pseudoexec):
        abscommission = size * price * self.p.commission
        return abs(abscommission)