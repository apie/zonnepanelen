#!/usr/bin/env python3
# By Apie, jun 2019
import os
from pydblite import Base
from save_usage import save_weekday_usage
from operator import itemgetter

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
db = Base(os.path.join(SCRIPT_DIR, 'usage.db'))
db.create('date', 'usage', mode="open")

def list_usage():
    for day in sorted(db, key=itemgetter('date')):
        netto = day['usage']['accumulatedConsumption'] - day['usage']['accumulatedProduction']
        print('{} Netto usage: {:.0f}'.format(day['date'], netto))

if __name__ == '__main__':
    list_usage()
