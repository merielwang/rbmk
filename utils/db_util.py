import psycopg2
import pandas.io.sql as sqlio
from utils.config import PROD_DB_CONFIG


def connect_to_db():
    """
    initiate an db instance
    :return: db instance obj
    """
    engine = psycopg2.connect(
        database=PROD_DB_CONFIG["DATABASE"],
        user=PROD_DB_CONFIG["USER"],
        password=PROD_DB_CONFIG["PASSWORD"],
        host=PROD_DB_CONFIG["HOST"],
        port=PROD_DB_CONFIG["PORT"]
    )
    return engine


def download_data_intraday(conn, security_symbol, date_key_int, interval="1m"):
    """
    downloading intraday trading data
    :param conn: (obj) db connection
    :param security_symbol: (str)
    :param date_key_int: (int)
    :param interval: 1m or 5m
    :return: pandas dataframe
    """
    # print(f"Downloading data for {security_symbol} on {date_key_int}...")
    sql = f"select * from us_equity_{interval} where security_symbol = '{security_symbol}' " \
          f"and date_key_int = {date_key_int} ORDER BY time_stamp asc;"
    df = sqlio.read_sql_query(sql, conn)
    return df if df.size > 0 else None


def download_data_daily(conn, security_symbol, start_date, end_date, interval="daily"):
    """
    Download daily trading data
    :param conn: (obj) db connection
    :param security_symbol: (str) security symbol
    :param start_date: (int) YYYYMMDD
    :param end_date: (int) YYYYMMDD
    :param interval: "daily"
    :return:
    """
    # print(f"Downloading data for {security_symbol} on {date_key_int}...")
    sql = f"select * from us_equity_{interval} where security_symbol = '{security_symbol}' " \
          f"and date_key_int between {start_date} AND {end_date} ORDER BY date_key_int asc;"
    df = sqlio.read_sql_query(sql, conn)
    return df if df.size > 0 else None


def delete_rows(conn, security_symbol, date_key_int, interval):
    """
    Caution! Delete database data
    :param conn: (obj) db connection
    :param security_symbol: (str) security symbol
    :param date_key_int: (int) YYYYMMDD
    :param interval: 1m or 5m or daily
    :return:
    """
    cursor = conn.cursor()
    sql = f"DELETE FROM us_equity_{interval} " \
          f"WHERE security_symbol = '{security_symbol}' and date_key_int = {date_key_int}"
    cursor.execute(sql)
    cursor.close()
