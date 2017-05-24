#!/usr/local/bin/python3

import time
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key,Attr
from optparse import OptionParser

parser = OptionParser()
parser.add_option( "-g","--gender",dest="gender",
		  help="Enter Gender -- REQUIRED")

(options, args) = parser.parse_args()

if not options.gender:
  print("Please specify a gender.")
  parser.print_help()
  exit(1)

orig_table = ""
new_table = ""

if options.gender == "female":
  orig_table = 'nepreprpigirls'
  new_table = 'nepreprpigirlsnew'
elif options.gender == "male":
  orig_table = 'nepreprpiboys'
  new_table = 'nepreprpiboysnew'

season=int(datetime.strftime(datetime.today(),"%Y"))

dynamodb = boto3.resource('dynamodb')
t = dynamodb.Table(orig_table)

# Get all the games from the old table
games = t.query(KeyConditionExpression=Key('season').eq(season))

for game in games['Items']:
  record = {}
  record['key'] = int(datetime.strftime(datetime.today(),"%s"))
  record['TeamsDate'] = game['teams']+game['date']
  record['date'] = game['date']
  record['loser'] = game['loser']
  record['winner'] = game['winner']
  record['season'] = season
  if 'tie' in game:
    record['tie'] = game['tie']
  record['scores'] = {}
  record['scores']['winner'] = game['scores']['winner']
  record['scores']['loser'] = game['scores']['loser']
  n = dynamodb.Table(new_table)
  n.put_item(Item=record)
  time.sleep(1)
