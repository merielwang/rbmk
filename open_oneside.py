from utils.db_util import connect_to_db
from utils.helpers import read_sec_list
import plotly.graph_objects as go
import pandas.io.sql as sqlio
import datetime


def download_data(conn, security_symbol, date_key_int, interval="1m"):
    print(f"Downloading data for {security_symbol} on {date_key_int}...")
    sql = f"select * from us_equity_{interval} where security_symbol = '{security_symbol}' " \
          f"and date_key_int = {date_key_int} ORDER BY time_stamp asc;"
    df = sqlio.read_sql_query(sql, conn)
    return df


def candle_stick(security_symbol, date_key_int, conn=None, df=None):
    """
    plot candle stick chart
    :param conn: db engine obj
    :param security_symbol: string
    :param date_key_int: int
    :return:
    """
    if df is None:
        conn = connect_to_db() if conn is None else conn
        df = download_data(conn, security_symbol, date_key_int, "1m")

    print(f"plotting chart for {security_symbol} on {date_key_int}...")
    fig = go.Figure(data=[go.Candlestick(x=df['time_stamp'],
                    open=df['open_price'],
                    high=df['high_price'],
                    low=df['low_price'],
                    close=df['close_price'])])
    fig.update_layout(
        title=f'Daily Price Visualization For {date_key_int}',
        yaxis_title=f'{security_symbol} Stock'
    )
    fig.show()


def time_diff(earlier, later):
    etime = datetime.datetime(2000, 1, 1, int(earlier[:2]), int(earlier[3:4]), int(earlier[6:]))
    ltime = datetime.datetime(2000, 1, 1, int(later[:2]), int(later[3:4]), int(earlier[6:]))
    return (ltime - etime).seconds


def oneside_test_drop(df):
    pre_clo = 999999
    ded = 0
    cnt = 0
    if df.size < 100:
        return False
    for index, row in df.iterrows():
        if row['time_stamp'] < '10:00:00':
            if pre_clo < row['close_price']:
                ded += 1
            else:
                cnt += 1
            pre_clo = row['close_price']
    return ded <= 10 and cnt >= 20


def oneside_test_raise(df):
    pre_clo = 0
    ded = 0
    cnt = 0
    if df.size < 100:
        return False
    for index, row in df.iterrows():
        if row['time_stamp'] < '10:00:00':
            if pre_clo > row['close_price']:
                ded += 1
            else:
                cnt += 1
            pre_clo = row['close_price']
    return ded <= 10 and cnt >= 20


def date_int_increment(date_key_int: int) -> int:
    date_key_int += 1
    if date_key_int % 100 == 32:
        date_key_int = date_key_int // 100
        date_key_int += 1
        if date_key_int % 100 == 13:
            date_key_int = date_key_int // 100
            date_key_int += 1
            date_key_int = date_key_int * 100 + 1
        date_key_int = date_key_int * 100 + 1
    return date_key_int


def find_onesides(conn, security_symbol, start_date_int, end_date_int):
    onesides_dict = dict()
    date_key_int = start_date_int
    while date_key_int <= end_date_int:
        df = download_data(conn, security_symbol, date_key_int, interval="1m")
        if oneside_test_drop(df) or oneside_test_raise(df):
            print(f"oneside found for {security_symbol} on {date_key_int}!")
            onesides_dict[date_key_int] = df
        date_key_int = date_int_increment(date_key_int)
    return onesides_dict


if __name__ == '__main__':
    conn = connect_to_db()
    securities = read_sec_list("sec_list.csv")
    osc_lst = dict()
    for security in securities:
        # input()
        # candle_stick(security, 20200605)
        oscs = find_onesides(conn, security, 20200601, 20200605)
        if len(oscs) != 0:
            osc_lst[security] = oscs
    conn = None
    for security in osc_lst:
        for date_key_int in osc_lst[security]:
            candle_stick(security, date_key_int, df=osc_lst[security][date_key_int])
