# calculate necessary components for oscillation detection 2.0
from utils.vwap import estimate_vwap_intraday
from utils.db_util import download_data_intraday
from utils.helpers import date_int_increment, time_later


def calc_spt_rst(candle_vwap, time_before='10:00:00'):
    cnt = 0
    high = None
    low = None
    for index, row in candle_vwap.iterrows():
        if time_later(row['time_stamp'], time_before):
            high = row['high_price'] if high is None or high < row['high_price'] else high
            low = row['low_price'] if low is None or low > row['low_price'] else low
            vwap = row['vwap']
            cnt += 1
    if cnt > 20:
        rst = vwap + (high - vwap) / 2
        spt = vwap - (vwap - low) / 2
        return spt, rst
    else:
        return None, None


def oscillation_detection(candle, low_thd, high_thd, time_start='10:00:00', time_end='11:00:00'):
    low_flag = False
    high_flag = False
    for index, row in candle.iterrows():
        if time_later(row['time_stamp'], time_end) and time_later(time_start, row['time_stamp']):
            if row['high_price'] >= high_thd:
                high_flag = True
            if row['low_price'] <= low_thd:
                low_flag = True
        elif time_later(time_end, row['time_stamp']):
            return high_flag and low_flag
    return high_flag and low_flag


def find_oscs(conn, security_symbol, start_date_int, end_date_int):
    positive = 0
    negative = 0
    osc_dict = dict()
    date_key_int = start_date_int
    while date_key_int <= end_date_int:
        df = download_data_intraday(conn, security_symbol, date_key_int, interval="1m")
        if df is not None:
            df_vwap = estimate_vwap_intraday(df)
            spt, rst = calc_spt_rst(df_vwap)
            if spt is not None and rst is not None:
                if oscillation_detection(df_vwap, spt, rst):
                    print(f"osc found for {security_symbol} on {date_key_int}!")
                    osc_dict[date_key_int] = df_vwap
                    positive += 1
                else:
                    print(f"{security_symbol} at {date_key_int} not oscillation!")
                    negative += 1
        date_key_int = date_int_increment(date_key_int)
    return osc_dict, negative, positive
