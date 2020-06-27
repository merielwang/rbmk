import numpy as np


def estimate_vwap_intraday(df_candle, res_name="vwap"):
    vol = df_candle.volume.values
    high = df_candle.high_price.values
    low = df_candle.low_price.values
    close = df_candle.close_price.values
    df_candle[res_name] = np.cumsum(vol * (high + low + close) / 3) / np.cumsum(vol)
    return df_candle


def estimate_vwap_daily(df_candle, res_name="vwap_point"):
    vol = df_candle.volume.values
    high = df_candle.high_price.values
    low = df_candle.low_price.values
    close = df_candle.close_price.values
    df_candle[res_name] = (vol * (high + low + close) / 3) / vol
    return df_candle


def calc_vwap_moving_avg(df_candle, vwap_col, window=5, res_name="vwap_ma"):
    df_candle[res_name] = df_candle[vwap_col].rolling(window=window).mean()
    return df_candle
