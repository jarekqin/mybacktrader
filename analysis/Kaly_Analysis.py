from __future__ import (absolute_import,division,print_function,unicode_literals)
from backtrader import Analyzer
from backtrader.mathsupport import average
from backtrader.utils import AutoOrderedDict

class Kelly(Analyzer):

    def create_analysis(self):
        self.rets=AutoOrderedDict()

    def start(self):
        super(Kelly,self).start()
        self.pnlWins=[]
        self.pnlLosses=[]


    def notify_trade(self, trade):
        if trade.status==trade.Closed:
            if trade.pnlcomm>=0:
                self.pnlWIns.append(trade.pnlcomm)
            else:
                self.pnlLosses.append(trade.pnlcomm)

    def stop(self):
        if len(self.pnlWins)>0 and len(self.pnlLosses)>0:
            avgWins=average(self.pnlWins)
            avgLosses=abs(average(self.pnlLosses))

            winlossratio=avgWins/avgLosses
            if winlossratio==0:
                kellypercent=None
            else:
                numberofwins=len(self.pnlWins)
                numberoflosses=len(self.pnlLosses)
                numberoftrades=numberoflosses+numberofwins
                winprob=numberofwins/numberoftrades
                inverse_winprob=1-winprob

                kellypercent=winprob-(inverse_winprob/winlossratio)
        else:
            kellypercent=None
        self.rets.kellyratio=kellypercent
        self.rets.kellypercent=kellypercent
