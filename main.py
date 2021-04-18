import calendar
import datetime
import multiprocessing

from fxcmpy import fxcmpy
from config import Config


def last_day_of_month(any_day):
    # this will never fail
    # get close to the end of the month for any day, and add 4 days 'over'
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    # subtract the number of remaining 'overage' days to get last day of current month, or said programattically
    # said, the previous day of the first of next month
    return next_month - datetime.timedelta(days=next_month.day)


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def write_csv(connection: fxcmpy, pair, from_dt, to_dt):
    start = from_dt
    mode = 'w'
    header = True
    file_name = pair.replace("/", "_") + '_m1_' + from_dt.strftime("%m_%Y") + '.csv'
    while start.date() <= to_dt.date():
        if (start + datetime.timedelta(days=7) + datetime.timedelta(seconds=-1)) > to_dt:
            end = to_dt
        else:
            end = start + datetime.timedelta(days=7) + datetime.timedelta(seconds=-1)
        his = connection.get_candles(instrument=pair, period="m1", number=9999, start=start, end=end)
        his.to_csv('./output/' + file_name, mode=mode, header=header)
        start += datetime.timedelta(days=7)
        mode = 'a'
        header = False
    print(from_dt.strftime("%m_%Y") + ' Successfuly')


def get_data(i):
    con = fxcmpy(access_token=Config.TOKEN, log_level=Config.LOG_LEVEL, server='demo', log_file=Config.LOG_FILE)
    month_from = Config.FROMDATE
    month_to = Config.TODATE
    fr_dt = add_months(month_from, i)
    to_dt = last_day_of_month(month_to)
    to_dt = datetime.datetime.combine(to_dt.date(), datetime.time.max)
    while fr_dt <= to_dt.date():
        start = datetime.datetime.combine(fr_dt, datetime.time.min)
        end = datetime.datetime.combine(last_day_of_month(fr_dt), datetime.time.max)
        write_csv(con, Config.PAIR, start, end)
        fr_dt = add_months(fr_dt, no_process)
        print(start.strftime("%m/%d/%Y, %H:%M:%S") + '-' + end.strftime("%m/%d/%Y, %H:%M:%S"))
    con.close()


# write_csv(con,"EUR/USD", month)

no_process = Config.PARALLEL
if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=no_process)
    # pool = multiprocessing.Semaphore(no_process)
    inputs = range(0, no_process)
    outputs = pool.map(get_data, inputs)
