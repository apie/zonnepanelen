#!/usr/bin/env python3
# By Apie, sept 2018
import os
import requests
import datetime
import pprint
from email.utils import parsedate
from pydblite import Base
from credentials import USER_NAME, PASSWORD, HOUSE_ID

ROOT_URL = 'http://novusvidere.westeurope.cloudapp.azure.com:8091/application'
LOGIN_URL = '{root_url}/authentication/login'.format(root_url=ROOT_URL)
USAGE_API_URL = '{root_url}/energysensing/{house_id}/2018-08-01'.format(root_url=ROOT_URL, house_id=HOUSE_ID)
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

db = Base(os.path.join(SCRIPT_DIR, 'token.db'))
db.create('token', 'expiry', mode="open")

def save_in_db(token, expiry):
    db.delete(db) # Clear db first
    db.insert(token=token, expiry=expiry)
    db.commit()

def get_valid_token(now):
  token = [a['token'] for a in db('expiry') >= now]
  return token[0] if len(token) >= 1 else None


session = requests.Session()
now = datetime.datetime.now()

token = get_valid_token(now)
if not token:
  response = session.post(LOGIN_URL, json=dict(grant_type='password', username=USER_NAME, password=PASSWORD))
  response.raise_for_status()
  token = response.json()['access_token']
  expires = response.json()['.expires']
  save_in_db(token, datetime.datetime(*parsedate(expires)[:6]))
  print('logged in')
response = session.get(USAGE_API_URL, headers={'sso-token': token})
response.raise_for_status()
usage_data = response.json()

data_today = usage_data['week'][0]

print('Data vandaag')
pprint.pprint(data_today)
assert data_today['date'] == now.strftime('%Y-%m-%d')
