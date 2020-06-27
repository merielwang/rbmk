from utils.db_util import connect_to_db
from utils.helpers import read_sec_list
from utils.visualization import candle_stick
from analytics.oscillation_20 import find_oscs


if __name__ == '__main__':
    conn = connect_to_db()
    securities = read_sec_list("sec_list.csv")
    negs = 0
    poss = 0
    osc_lst = dict()
    for security in securities:
        oscs, n, p = find_oscs(conn, security, 20200604, 20200605)
        if len(oscs) != 0:
            osc_lst[security] = oscs
        negs += n
        poss += p
    conn = None
    print(f"positive: {poss}; negative: {negs}")
    print("ready to plot, press anykey to continue:")
    for security in osc_lst:
        for date_key_int in osc_lst[security]:
            input()
            candle_stick(security, date_key_int, df=osc_lst[security][date_key_int])
