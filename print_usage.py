#!/usr/bin/env python3
# By Apie, jun 2019
from datetime import date, timedelta
from fetch_usage import fetch_current_usage
from operator import itemgetter
from zonnepanelen_dbs import db_m, db_c, db_d

DATE_COL_LEN = 20
USAGE_COL_LEN = 10
USAGE_COL_H_LEN = USAGE_COL_LEN + 5

today = date.today()

def list_month_usage():
    one_year_ago = today - timedelta(days=365) - timedelta(days=32)
    for day in sorted(db_m("date") > one_year_ago, key=itemgetter('date')):
        c, p = day['usage']['accumulatedConsumption'], day['usage']['accumulatedProduction']
        print('{:<{dfill}} {:>{ufill}.0f} kWh'.format(
            day['date'].strftime('%Y-%m'), c-p,
            dfill=DATE_COL_LEN, ufill=USAGE_COL_LEN,
        ))

def list_day_usage():
    five_days_ago = today - timedelta(days=5)
    for day in sorted(db_d("date") > five_days_ago, key=itemgetter('date')):
        c, p = day['usage']['accumulatedConsumption'], day['usage']['accumulatedProduction']
        print('{:<{dfill}} {:>{ufill}.0f} kWh'.format(
            day['date'].strftime('%Y-%m-%d'), c-p,
            dfill=DATE_COL_LEN, ufill=USAGE_COL_LEN,
        ))

def list_current_usage():
    # Return latest record of current usage
    for day in sorted(db_c, key=itemgetter('datetime'), reverse=True):
        c, p = day['usage']['consumption'], day['usage']['production']
        return '{:<{dfill}} {:>{ufill}.3f} kW'.format(
            day['datetime'].strftime('%Y-%m-%d %H:%M'), c-p,
            dfill=DATE_COL_LEN, ufill=USAGE_COL_LEN,
        )

if __name__ == '__main__':
    print('{d:<{dfill}} {u:<{ufill}}'.format(
        d='Date',
        u='Netto usage',
        dfill=DATE_COL_LEN, ufill=USAGE_COL_H_LEN,
    ))
    print('='*(DATE_COL_LEN + USAGE_COL_H_LEN))
    list_month_usage()
    list_day_usage()

