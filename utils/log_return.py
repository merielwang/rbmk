import numpy as np
from utils.vwap import estimate_vwap_daily, calc_vwap_moving_avg


def log_return(df_candle, res_name="log_return", col_name="close_price", shift=5):
    # print(df_candle[df_candle[col_name] == 0])
    df_candle[res_name] = np.log(df_candle[col_name]) - np.log(df_candle[col_name].shift(shift))
    return df_candle


def log_return_intraday(df_candle, res_name="log_return_intra", col_bft="open_price", col_aft="close_price", abs=True):
    if abs:
        df_candle[res_name] = np.absolute(np.log(df_candle[col_aft]) - np.log(df_candle[col_bft]))
    else:
        df_candle[res_name] = np.log(df_candle[col_aft]) - np.log(df_candle[col_bft])
    return df_candle


def get_falls_raises(df_candle, falls_thd, raises_thd, shift=5):
    falls = list()
    raises = list()
    if df_candle.log_return is None:
        df_candle = log_return(df_candle)
    for index, row in df_candle.iterrows():
        if row['log_return'] > raises_thd and index >= shift:
            raises.append({
                'x': df_candle.iloc[index - shift]['date_key_int'],
                'y': df_candle.iloc[index - shift]['low_price'],
                'text': "Raising: " + str(round(row['log_return'] * 100, 2)) + "%"
            })
        elif row['log_return'] < falls_thd and index >= shift:
            falls.append({
                'x': df_candle.iloc[index - shift]['date_key_int'],
                'y': df_candle.iloc[index - shift]['high_price'],
                'text': "Falling: " + str(round(row['log_return'] * 100, 2)) + "%"
            })
    return {"falls": falls, "raises": raises}


def feature_extraction_fallraise(df_candle, df_rf1=None, df_rf2=None, df_rf3=None, falls_thd=0, raises_thd=0, shift=5):
    merged = df_candle
    if df_rf1 is not None:
        merged = df_candle.join(df_rf1.set_index('date_key_int'), on="date_key_int", how="inner", rsuffix="_rf1")
    if df_rf2 is not None:
        merged = merged.join(df_rf2.set_index('date_key_int'), on="date_key_int", how="inner", rsuffix="_rf2")
    if df_rf3 is not None:
        merged = merged.join(df_rf3.set_index('date_key_int'), on="date_key_int", how="inner", rsuffix="_rf3")
    merged = log_return(merged, res_name="lr1", col_name="close_price", shift=1)
    merged = log_return(merged, res_name="lr2", col_name="close_price", shift=2)
    merged = log_return(merged, res_name="lr3", col_name="close_price", shift=3)
    merged = log_return(merged, res_name="lr4", col_name="close_price", shift=4)
    if df_rf1 is not None:
        merged = log_return(merged, res_name="r1lr1", col_name="close_price_rf1", shift=1)
        merged = log_return(merged, res_name="r1lr2", col_name="close_price_rf1", shift=2)
    if df_rf2 is not None:
        merged = log_return(merged, res_name="r2lr1", col_name="close_price_rf2", shift=1)
        merged = log_return(merged, res_name="r2lr2", col_name="close_price_rf2", shift=2)
    if df_rf3 is not None:
        merged = log_return(merged, res_name="r3lr1", col_name="close_price_rf3", shift=1)
        merged = log_return(merged, res_name="r3lr2", col_name="close_price_rf3", shift=2)
    merged = log_return(merged, res_name="vlr1", col_name="volume", shift=1)

    merged['volatility'] = merged['lr1'].rolling(5).std()
    merged['lr11'] = merged['lr1'].shift(1)
    merged['lr12'] = merged['lr1'].shift(2)
    merged['lr13'] = merged['lr1'].shift(3)
    merged['lr31'] = merged['lr3'].shift(1)
    merged = log_return(merged, res_name="lr5-5", col_name="close_price", shift=1)
    merged["lr5-5"] = merged["lr5-5"].shift(-1)
    merged["vlr11"] = merged["vlr1"].shift(1)

    merged['lr0'] = np.log(merged["close_price"]) - np.log(merged["open_price"])
    merged['lr01'] = merged['lr0'].shift(1)
    merged['lr02'] = merged['lr0'].shift(2)

    merged = estimate_vwap_daily(merged, res_name='vwap_daily')
    merged = calc_vwap_moving_avg(merged, vwap_col="vwap_daily", window=5, res_name="vwap_ma_5")
    merged = calc_vwap_moving_avg(merged, vwap_col="vwap_daily", window=3, res_name="vwap_ma_3")
    merged = merged.iloc[shift:-shift]

    # merged['label'] = 0
    # merged['label'][merged['lr5-5'] < falls_thd] = 1
    # merged['label'][merged['lr5-5'] > raises_thd] = -1
    # merged = merged[merged.label != 0]

    # pos_sum = merged['lr5-5'][merged['label'] == 1].abs().sum()
    # neg_sum = merged['lr5-5'][merged['label'] == -1].abs().sum()
    #
    # print(pos_sum, neg_sum)
    #
    # merged['weight'] = 0
    # merged['weight'][merged['label'] == 1] = merged['lr5-5'][merged['label'] == 1].abs() * (neg_sum / pos_sum)
    # merged['weight'][merged['label'] == -1] = merged['lr5-5'][merged['label'] == -1].abs()

    # feature = merged[['lr1', 'lr2', 'lr3', 'lr4', 'r1lr1', 'r1lr2', 'r2lr1', 'r2lr2', 'r3lr1', 'r3lr2', 'vlr1',
    #                   'volatility', 'lr11', 'lr31', 'vlr11', 'lr0', 'lr01', 'lr02']]
    # label = merged[['label']]
    # weight = merged[['weight']]

    # return feature, label, weight
    return merged
