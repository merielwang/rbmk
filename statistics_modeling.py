from analytics import stat_feat_14, dist_feat_14, stat_feat_15, dist_feat_15, stat_m21, dist_m21, compare_hl_oc_dists
from utils.db_util import connect_to_db, download_data_daily
from utils.helpers import read_sec_list
from utils.visualization import candle_stick_daily


if __name__ == '__main__':
    conn = connect_to_db()
    securities = read_sec_list("sec_list.csv")

    for sec in securities:
        print(f"evaluating {sec}")
        df = download_data_daily(conn, sec, 20170101, 20200601)
        mean_hl, mean_oc, sigma_hl, sigma_oc = compare_hl_oc_dists(df_candle=df)
        print(f"mean_hl: {round(100*mean_hl, 2)}%, mean_oc: {round(100*mean_oc, 2)}%,"
              f" sigma_hl: {round(100*sigma_hl, 2)}%, sigma_oc: {round(100*sigma_oc, 2)}%")
        input()
        # stat_m21(sec, 20170101, 20200520, thrd=-0.01, interval=None, conn=conn)
        # dist_feat_14("USMV", 20130101, 20200520, conn=conn)
    # stat, ann = stat_feat_14("SDOW", 20130601, 20200601, thrd=-0.001, interval=None, conn=conn)
    # stat_m21("TQQQ", 20130601, 20200601, thrd=-0.001, interval=None, conn=conn)
    # candle_stick_daily("SDOW", 20130610, 20200601, annotations=ann)
