from utils.vwap import estimate_vwap_intraday
from utils.db_util import connect_to_db, download_data_intraday, download_data_daily
import plotly.graph_objects as go
import pandas as pd


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
        df = download_data_intraday(conn, security_symbol, date_key_int, "1m")
    df = estimate_vwap_intraday(df)

    print(f"plotting chart for {security_symbol} on {date_key_int}...")
    fig = go.Figure(data=[
        go.Candlestick(x=df['time_stamp'],
                       open=df['open_price'],
                       high=df['high_price'],
                       low=df['low_price'],
                       close=df['close_price'],
                       name="Candle Stick"),
        go.Line(x=df['time_stamp'],
                y=df['vwap'],
                mode="lines",
                name="VWAP")]
    )
    fig.update_layout(
        title=f'Daily Price Visualization For {date_key_int}',
        yaxis_title=f'{security_symbol} Stock'
    )
    fig.show()


def candle_stick_daily(security_symbol, start_date, end_date, conn=None, df=None, annotations=None):
    """
    :param security_symbol:
    :param start_date:
    :param end_date:
    :param conn:
    :param df:
    :param annotations: [{'x': date_key_int, 'y': high_price, 'text': 'falling?'}]
    :return:
    """
    def __update_annotations(fig, anns):
        if anns is not None:
            for ann in anns:
                fig.add_annotation(
                    x=pd.to_datetime(str(ann['x']), format='%Y%m%d'),
                    y=ann['y'],
                    text=ann['text'])
            fig.update_annotations(dict(
                xref="x",
                yref="y",
                showarrow=True,
                arrowhead=7,
                ax=0,
                ay=-40
            ))
        return True

    if df is None:
        conn = connect_to_db() if conn is None else conn
        df = download_data_daily(conn, security_symbol, start_date, end_date)
        df['date_key'] = df['date_key_int'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))

    print(f"plotting chart for {security_symbol} ...")
    fig = go.Figure(data=[
        go.Candlestick(x=df['date_key'],
                       open=df['open_price'],
                       high=df['high_price'],
                       low=df['low_price'],
                       close=df['close_price'],
                       name="Candle Stick")])
    __update_annotations(fig, annotations)

    fig.update_layout(
        title=f'Daily Price Visualization',
        yaxis_title=f'{security_symbol} Stock'
    )
    fig.show()
