import os
from pydblite import Base

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
db_c = Base(os.path.join(SCRIPT_DIR, 'current_usage.db'))
db_c.create('datetime', 'usage', mode="open")
db_d = Base(os.path.join(SCRIPT_DIR, 'daily_usage.db'))
db_d.create('date', 'usage', mode="open")
db_m = Base(os.path.join(SCRIPT_DIR, 'monthly_usage.db'))
db_m.create('date', 'usage', mode="open")

