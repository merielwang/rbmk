import csv
import datetime


def read_sec_list(file_name):
    """
    read security csv into list
    :param file_name:
    :return: security list
    """
    res = list()
    with open(file_name, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            res.append(row[0])
    return res


def time_diff(earlier, later):
    """
    Get time difference in seconds
    :param earlier: (str) time string: hh:mm:ss
    :param later: (str) time string: hh:mm:ss
    :return: (int) difference in seconds
    """
    etime = datetime.datetime(2000, 1, 1, int(earlier[:2]), int(earlier[3:4]), int(earlier[6:]))
    ltime = datetime.datetime(2000, 1, 1, int(later[:2]), int(later[3:4]), int(earlier[6:]))
    if etime < ltime:
        return (ltime - etime).seconds
    else:
        return (etime - ltime).seconds


def time_later(earlier, later):
    """
    compare if later is actually later than earlier
    :param earlier: (str) time string: hh:mm:ss
    :param later: (str) time string: hh:mm:ss
    :return: (bool) True/False
    """
    etime = datetime.datetime(2000, 1, 1, int(earlier[:2]), int(earlier[3:4]), int(earlier[6:]))
    ltime = datetime.datetime(2000, 1, 1, int(later[:2]), int(later[3:4]), int(earlier[6:]))
    return etime < ltime


def curdp_move(curdp, ppoint, rst, spt):
    low = True if ppoint['low_price'] <= spt else False
    high = True if ppoint['high_price'] >= rst else False
    if curdp is None:
        curdp = ("both", '11:30:00')
    gap = time_diff(curdp[1], ppoint['time_stamp'])
    if low and high:
        curdp = ("both", ppoint['time_stamp'])
    elif low and curdp[0] == "high" or curdp[0] == "both":
        curdp = ("low", ppoint['time_stamp'])
    elif high and curdp[0] == "low" or curdp[0] == "both":
        curdp = ("high", ppoint['time_stamp'])
    return curdp, gap


def date_int_increment(date_key_int: int) -> int:
    """
    date_key_int increment function, increase the given datekey by 1
    :param date_key_int: (int) YYYYMMDD
    :return: (int) increased date_key_int
    """
    date_key_int += 1
    if date_key_int % 100 == 32:
        date_key_int = date_key_int // 100
        date_key_int += 1
        if date_key_int % 100 == 13:
            date_key_int = date_key_int // 100
            date_key_int += 1
            date_key_int = date_key_int * 100 + 1
        date_key_int = date_key_int * 100 + 1
    return date_key_int
