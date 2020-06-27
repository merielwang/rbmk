from utils.db_util import connect_to_db
from utils.helpers import read_sec_list
from utils.visualization import candle_stick, candle_stick_daily


if __name__ == '__main__':
    conn = connect_to_db()

    # candle_stick_daily("SPY", 20100606, 20200606, conn)
    securities = read_sec_list("sec_list_f.csv")
    for security in securities:
        candle_stick(security, 20200618)
        input()
