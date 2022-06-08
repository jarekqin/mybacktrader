import pandas as pd
import tushare as ts
import os
import baostock as bs

from config import Token


def get_data_from_tushare(code, start_date, end_date, save_type='csv',
                          adj='qfq', save_path=None, file_name=None,
                          picker_name=None, table_name=None):
    ts.set_token(Token.tushare_token.value)
    df = ts.pro_bar(
        ts_code=code, adj=adj, start_date=start_date,
        end_date=end_date
    )
    df.sort_index(inplace=True, ascending=False)
    if save_type == 'csv':
        df.to_csv(os.path.join(save_path, file_name))
    elif save_type == 'excel':
        df.to_excel()
    elif save_type == 'sql' and picker_name is not None and table_name is not None:
        ...
    else:
        raise TypeError('save_type only supports with "csv/excel/sql"!')


def get_data_from_bs(code, start_date, end_date, save_type='csv',
                     adj='1', save_path=None, file_name=None,
                     picker_name=None, table_name=None,
                     out_put_col="date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
                     freq='d'):
    lg=bs.login()
    print('log in response error_code',lg.error_code)
    print('log in response error messge',lg.error_msg)
    rs = bs.query_history_k_data_plus(
        code, out_put_col,start_date=start_date,end_date=end_date,
        frequency=freq,adjustflag=adj
    )
    print('data response error_code',lg.error_code)
    print('data response error messge',lg.error_msg)
    df=rs.get_data()
    df=df.apply(pd.to_numeric,axis=0,errors='ignore')
    df=df[df.tradestatus==1]
    df=pd.to_datetime(df['date'])

    if save_type == 'csv':
        df.to_csv(os.path.join(save_path, file_name))
    elif save_type == 'excel':
        df.to_excel()
    elif save_type == 'sql' and picker_name is not None and table_name is not None:
        ...
    else:
        raise TypeError('save_type only supports with "csv/excel/sql"!')


if __name__ == '__main__':
    # get_data_from_tushare('600000.SH', adj='hfq', start_date='20000101', end_date='20200710',
    #                       save_path='/media/star/data/backtrader_data/save_data',
    #                       file_name='tushare_600000.csv'
    #                       )
    get_data_from_bs('sh.600000', '2000-01-01', '2020-07-10',adj='2',
                          save_path='/media/star/data/backtrader_data/save_data',
                          file_name='tushare_600000.csv'
                          )
