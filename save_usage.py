#!/usr/bin/env python3
# By Apie, jun 2019
import sys
import datetime
from fetch_usage import fetch_usage
from fetch_usage import fetch_current_usage
from zonnepanelen_dbs import db_m, db_c, db_d

def save_current_usage():
    db_c.insert(datetime=datetime.datetime.now(), usage=fetch_current_usage())
    db_c.commit()

def save_day_usage():
    # Save all but today's usage, because that can still increase
    def save_usage(date, usage):
        if not db_d(date=date):
            db_d.insert(date=date, usage=usage)
            db_d.commit()
    today = datetime.date.today()
    week = fetch_usage()['week']
    for wd in week:
        date = datetime.datetime.strptime(wd['date'], '%Y-%m-%d').date()
        if date == today:
            continue
        save_usage(date, wd)

def save_month_usage():
    def save_usage(date, usage):
        if not db_m(date=date):
            db_m.insert(date=date, usage=usage)
            db_m.commit()
    today = datetime.date.today()
    months = fetch_usage()['months']
    for md in months:
        date = datetime.datetime.strptime(md['month'], '%Y-%m-%d').date()
        if md['prediction'] or date.year == today.year and date.month == today.month:
            continue
        save_usage(date, md)

if __name__ == '__main__':
    if len(sys.argv)==1:
        print('Options: current, day, month')
    elif sys.argv[1] == 'current':
        save_current_usage()
    elif sys.argv[1] == 'day':
        save_day_usage()
    elif sys.argv[1] == 'month':
        save_month_usage()
    else:
        print('Unknown option')
