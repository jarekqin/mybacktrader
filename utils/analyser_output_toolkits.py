from datetime import datetime
from os import path

import sys
import backtrader as bt


def pretty_print(format, *args):
    print(format.format(*args))


def exists(object, *properties):
    for property in properties:
        if not property in object:
            return False
        object = object.get(property)
    return True


def printTradeAnalysis(cerebro, analysers):
    format = ' {:<24} : {:<24}'
    NA = '-'
    print('Backtesting Result')
    if hasattr(analysers, 'ta'):
        ta = analysers.ta.get_analysis()

        openTotal = ta.total.open if exists(ta, 'total', 'open') else None
        closedTotal = ta.total.closed if exists(ta, 'total', 'closed') else None
        wonTotal = ta.won.total if exists(ta, 'won', 'total') else None
        lostdTotal = ta.lost.total if exists(ta, 'lost', 'total') else None

        streakWonLongest = ta.streak.won.logest if exists(ta, 'strea', 'won', 'longest') else None
        streakLostLongest = ta.streak.lost.logest if exists(ta, 'strea', 'lost', 'longest') else None

        pnlNetTotal = ta.pnl.net.total if exists(ta, 'pnl', 'net', 'total') else None
        pnlNetAverage = ta.pnl.net.average if exists(ta, 'pnl', 'net', 'average') else None

        pretty_print(format, 'Open Position', openTotal or NA)
        pretty_print(format, 'Closed Trades', closedTotal or NA)
        pretty_print(format, 'Winning Trades', wonTotal or NA)
        pretty_print(format, 'Loosing Trades', lostdTotal or NA)
        print()

        pretty_print(format, 'Longest Winning Streak', streakWonLongest or NA)
        pretty_print(format, 'Longest Loosing Streak', streakLostLongest or NA)
        pretty_print(format, 'Strike Rate(Win/closed) ',
                     (wonTotal / closedTotal) * 100 if wonTotal and closedTotal else NA)
        print()

        pretty_print(format, 'Net P/L', '{}'.format(round(pnlNetTotal, 2)) if pnlNetTotal else NA)
        pretty_print(format, 'P/L Average per trade', '{}'.format(round(pnlNetAverage, 2)) if pnlNetAverage else NA)
        print()

        if hasattr(analysers, 'drawdown'):
            pretty_print(format, 'Drawdown: ', '{}'.format(analysers.drawdown.get_analysis()['drawdown']))

        if hasattr(analysers, 'sharp'):
            pretty_print(format, 'SR: ', '{}'.format(analysers.sharpe.get_analysis()['sharperatio']))

        if hasattr(analysers, 'vwr'):
            pretty_print(format, 'VWR', '{}'.format(analysers.vwr.get_analysis()['vwr']))

        if hasattr(analysers, 'sqn'):
            pretty_print(format, 'SQN', '{}'.format(analysers.sqn.get_analysis()['sqn']))
        print()

        print('Transactions')
        format = '{:<24} : {:<24} {:<16} : {:<8} {:<8} : {:<16}'
        pretty_print(format, 'Date', 'Amount', 'Price', 'SID', 'Symbol', 'Value')
        for key, value in analysers.txn.get_analysis().items():
            pretty_print(
                format, key.strftime('%Y-%m-%d %H:%M:%S'), value[0][0], value[0][1],
                value[0][2], value[0][3], value[0][4]
            )
