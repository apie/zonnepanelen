#!/usr/bin/env python3
# By Apie, jun 2019
import os
import datetime
from pydblite import Base
from fetch_usage import fetch_usage

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
db = Base(os.path.join(SCRIPT_DIR, 'usage.db'))
db.create('date', 'usage', mode="open")

def save_usage(date, usage):
    if not db(date=date):
        db.insert(date=date, usage=usage)
        db.commit()

def save_weekday_usage():
    # Save all but today's usage, because that can still increase
    today = datetime.date.today()
    week = fetch_usage()['week']
    for wd in week:
        date = datetime.datetime.strptime(wd['date'], '%Y-%m-%d').date()
        if date == today:
            continue
        save_usage(date, wd)

if __name__ == '__main__':
    save_weekday_usage()
