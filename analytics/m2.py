from utils.log_return import log_return, get_falls_raises, feature_extraction_fallraise
from utils.db_util import connect_to_db, read_sec_list, download_data_daily
import matplotlib.pyplot as plt


def stat_m21(security_symbol, start_date, end_date, thrd=-0.001, interval=None, conn=None):
    conn = connect_to_db() if conn is None else conn
    df = download_data_daily(conn, security_symbol, start_date, end_date)
    features = feature_extraction_fallraise(df)
    pos_cnt = 0
    neg_cnt = 0
    pos = 0
    neg = 0
    expp_list = list()
    for index, row in features.iterrows():
        if row['lr12'] < thrd and row['lr11'] < thrd and row['lr1'] < thrd:
            if row['lr5-5'] > 0.000:
                pos_cnt += 1
                pos += row['lr5-5']
            elif row['lr5-5'] < -0.000:
                neg_cnt += 1
                neg += row['lr5-5']
            if interval is not None and pos_cnt + neg_cnt >= interval:
                exp_p = (pos + neg) / (pos_cnt + neg_cnt)
                expp_list.append(round(100*exp_p, 2))
                pos_cnt = 0
                neg_cnt = 0
                pos = 0
                neg = 0
    if interval is None and (pos_cnt + neg_cnt) > 0:
        exp_p = (pos + neg)/(pos_cnt + neg_cnt)
        pos_rate = round(100*pos/pos_cnt, 2) if pos_cnt > 0 else "N/A"
        neg_rate = round(100*neg/neg_cnt, 2) if neg_cnt > 0 else "N/A"
        print(f"corr: {pos_cnt} with expected return {pos_rate}%, wrong: {neg_cnt} with expected return "
              f"{neg_rate}%, Strategy Total Expected Return {round(100*exp_p, 2)}%")
    else:
        print(expp_list)
        # print(features.iloc[-1]['date_key_int'])


def dist_m21(security_symbol, start_date, end_date, thrd=-0.001, conn=None):
    conn = connect_to_db() if conn is None else conn
    df = download_data_daily(conn, security_symbol, start_date, end_date)
    features = feature_extraction_fallraise(df)
    features_ss = features.loc[features['lr12'] < features['lr11'] & features['lr11'] < features['lr1'] & features['lr1'] < thrd]
    print(f"Mean: {features_ss['lr5-5'].mean()}, Sigma: {features_ss['lr5-5'].std()}")
    # print(features_ss)
    features_ss.hist(column='lr5-5', bins=500)
    plt.show()
