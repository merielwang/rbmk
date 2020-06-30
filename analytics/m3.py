from utils.log_return import log_return, log_return_intraday, feature_extraction_fallraise
from utils.db_util import connect_to_db, download_data_daily
import matplotlib.pyplot as plt
from utils.vwap import estimate_vwap_intraday
from utils.db_util import download_data_intraday
from utils.helpers import date_int_increment, time_later, measure_distribution


def compare_hl_oc_dists(df_candle):
    df_candle = log_return_intraday(df_candle, res_name="lr_hl", col_aft="high_price", col_bft="low_price", abs=False)
    df_candle = log_return_intraday(df_candle, res_name="lr_oc")
    mean_hl, sigma_hl = measure_distribution(df_candle, col_name="lr_hl", plot=False)
    mean_oc, sigma_oc = measure_distribution(df_candle, col_name="lr_oc", plot=False)
    plt.hist(df_candle["lr_hl"], 100, alpha=0.5, label='high low movement')
    plt.hist(df_candle["lr_oc"], 100, alpha=0.5, label='open close movement')
    plt.legend(loc='upper right')
    plt.show()
    return mean_hl, mean_oc, sigma_hl, sigma_oc


def m3_criteria(candle_intraday_vwap, time_before='11:00:00', p_thrd=0.9):
    pass


# def oscillation_detection(candle, low_thd, high_thd, time_start='10:00:00', time_end='11:00:00'):
#     low_flag = False
#     high_flag = False
#     for index, row in candle.iterrows():
#         if time_later(row['time_stamp'], time_end) and time_later(time_start, row['time_stamp']):
#             if row['high_price'] >= high_thd:
#                 high_flag = True
#             if row['low_price'] <= low_thd:
#                 low_flag = True
#         elif time_later(time_end, row['time_stamp']):
#             return high_flag and low_flag
#     return high_flag and low_flag
#
#
# def find_oscs(conn, security_symbol, start_date_int, end_date_int):
#     positive = 0
#     negative = 0
#     osc_dict = dict()
#     date_key_int = start_date_int
#     while date_key_int <= end_date_int:
#         df = download_data_intraday(conn, security_symbol, date_key_int, interval="1m")
#         if df is not None:
#             df_vwap = estimate_vwap_intraday(df)
#             spt, rst = calc_spt_rst(df_vwap)
#             if spt is not None and rst is not None:
#                 if oscillation_detection(df_vwap, spt, rst):
#                     print(f"osc found for {security_symbol} on {date_key_int}!")
#                     osc_dict[date_key_int] = df_vwap
#                     positive += 1
#                 else:
#                     print(f"{security_symbol} at {date_key_int} not oscillation!")
#                     negative += 1
#         date_key_int = date_int_increment(date_key_int)
#     return osc_dict, negative, positive

