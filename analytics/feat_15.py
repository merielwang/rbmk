from utils.log_return import feature_extraction_fallraise
from utils.db_util import connect_to_db, download_data_daily
import matplotlib.pyplot as plt


def stat_feat_15(security_symbol, start_date, end_date, thrd=-0.001, interval=None, conn=None):
    conn = connect_to_db() if conn is None else conn
    df = download_data_daily(conn, security_symbol, start_date, end_date)
    features = feature_extraction_fallraise(df)
    pos_cnt = 0
    neg_cnt = 0
    pos = 0
    neg = 0
    expp_list = list()
    for index, row in features.iterrows():
        if row['lr02'] < row['lr01'] < thrd:
            if row['lr0'] > 0.000:
                pos_cnt += 1
                pos += row['lr0']
            elif row['lr0'] < -0.000:
                neg_cnt += 1
                neg += row['lr0']
            if interval is not None and pos_cnt + neg_cnt >= interval:
                exp_p = (pos + neg) / (pos_cnt + neg_cnt)
                expp_list.append(round(100*exp_p, 2))
                pos_cnt = 0
                neg_cnt = 0
                pos = 0
                neg = 0
    if interval is None:
        exp_p = (pos + neg)/(pos_cnt + neg_cnt)
        print(f"corr: {pos_cnt} with expected return {round(100*pos/pos_cnt, 2)}%, wrong: {neg_cnt} with expected return "
              f"{round(100*neg/neg_cnt, 2)}%, Strategy Total Expected Return {round(100*exp_p, 2)}%")
    else:
        print(expp_list)


def dist_feat_15(security_symbol, start_date, end_date, thrd=-0.001, conn=None):
    conn = connect_to_db() if conn is None else conn
    df = download_data_daily(conn, security_symbol, start_date, end_date)
    features = feature_extraction_fallraise(df)
    features_ss = features.loc[(features['lr01'] < thrd) & (features['lr02'] < features['lr01'])]
    print(f"Mean: {features_ss['lr0'].mean()}, Sigma: {features_ss['lr0'].std()}")
    # print(features_ss)
    features_ss.hist(column='lr0', bins=500)
    plt.show()
