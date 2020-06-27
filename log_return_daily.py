from utils.log_return import log_return, get_falls_raises, feature_extraction_fallraise
from utils.db_util import connect_to_db, download_data_daily
from utils.visualization import candle_stick, candle_stick_daily
from utils.helpers import read_sec_list
from ml_models.etf_disaster_forecasting import svc_modeling
import matplotlib.pyplot as plt
import pandas as pd


def get_performance_log_return(df, shift=5, plot=False):
    df = log_return(df, shift=shift)
    if plot:
        print(f"Mean: {df.log_return.mean()}, Sigma: {df.log_return.std()}")
        df.hist(column='log_return', bins=500)
        plt.show()
    return {"mean": df.log_return.mean(), "std": df.log_return.std()}


def show_all_fallraise(security_symbol, start_date, end_date, f_thd=-0.01, r_thd=0.02, conn=None):
    conn = connect_to_db() if conn is None else conn
    df = download_data_daily(conn, security_symbol, start_date, end_date)
    df = log_return(df)
    signals = get_falls_raises(df, falls_thd=f_thd, raises_thd=r_thd)
    signals['raises'].extend(signals['falls'])
    print(len(signals['raises']), len(signals['falls']))
    candle_stick_daily(security_symbol, start_date, end_date, conn, annotations=signals['raises'])


def rank_performances(file_name, start_date, end_date):
    """

    :param file_name:
    :param start_date:
    :param end_date:
    :return:
    """
    # take second element for sort
    def __take_second(elem):
        return elem[1]
    secs = read_sec_list(file_name)
    conn = connect_to_db()
    results = list()
    for sec in secs:
        df = download_data_daily(conn, sec, start_date, end_date)
        perf = get_performance_log_return(df)
        results.append([sec, perf['mean'], perf['std']])
    results.sort(key=__take_second)
    for each in results:
        print(each)


if __name__ == '__main__':
    show_all_fallraise("USMV", start_date=20120606, end_date=202006019, f_thd=-0.03, r_thd=0.05)
    # con = connect_to_db()
    # security_symbol = "USMV"
    # ref1_symbol = "SPY"
    # ref2_symbol = "DIA"
    # ref3_symbol = "IVV"
    # start_date = 20150101
    # end_date = 20200101
    # df_candle = download_data_daily(con, security_symbol, start_date, end_date)
    # ref1 = download_data_daily(con, ref1_symbol, start_date, end_date)
    # ref2 = download_data_daily(con, ref2_symbol, start_date, end_date)
    # ref3 = download_data_daily(con, ref3_symbol, start_date, end_date)
    # t_feature, t_label, t_weights = feature_extraction_fallraise(df_candle, ref1, ref2, ref3, falls_thd=0.02, raises_thd=0.02)
    # svc_modeling(t_feature, t_label, t_weights)

    # t_feature.to_csv("feature.csv", index=False)
    # start_date = 20190102
    # end_date = 20200615
    # df_candle = download_data_daily(con, security_symbol, start_date, end_date)
    # ref1 = download_data_daily(con, ref1_symbol, start_date, end_date)
    # ref2 = download_data_daily(con, ref2_symbol, start_date, end_date)
    # ref3 = download_data_daily(con, ref3_symbol, start_date, end_date)
    # result = feature_extraction_fallraise(df_candle, ref1, ref2, ref3, falls_thd=-0.02, raises_thd=0.02)
    # p_set = result[result.label != 0]
    # p_set.to_csv("test_set.csv", index=False)
