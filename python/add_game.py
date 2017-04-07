#!/usr/bin/python

import time
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key,Attr
from optparse import OptionParser


parser = OptionParser()
parser.add_option("-w","--winner",dest="winner",
                  help="Enter Winning Team Name -- REQUIRED")
parser.add_option( "-l","--loser",dest="loser",
		  help="Enter Losing Team Name -- REQUIRED")
parser.add_option( "-d","--date",dest="date",
		  help="Enter game date -- Defaults to today")
parser.add_option( "-S","--winner_score",dest="ws",
		  help="Enter winning score -- REQUIRED")
parser.add_option( "-s","--loser_score",dest="ls",
		  help="Enter losing score -- REQUIRED")
parser.add_option( "-g","--gender",dest="gender",
		  help="Enter Gender -- REQUIRED")

(options, args) = parser.parse_args()

if not options.winner:
  print "Please specify a winning team."
  parser.print_help()
  exit(1)

if not options.loser:
  print "Please specify a losing team."
  parser.print_help()
  exit(1)

if not options.ls:
  print "Please specify a losing score."
  parser.print_help()
  exit(1)

if not options.ws:
  print "Please specify a winning score."
  parser.print_help()
  exit(1)

if not options.date:
  date = datetime.strftime(datetime.today(),"%m/%d/%Y")
else:
  date = options.date

if not options.gender:
  print "Please specify a gender."
  parser.print_help()
  exit(1)

# create the record
record = {}
record['season'] = int(datetime.strftime(datetime.today(),"%Y"))
record['teams'] = options.winner+options.loser
record['winner'] = options.winner
record['loser'] = options.loser
record['date'] = date
record['scores'] = {}
record['scores']['winner'] = options.ws
record['scores']['loser'] = options.ls

table_name = ""
if gender == "female":
  table_name = 'nepreprpigirls'
elif gender == "male":
  table_name = 'nepreprpiboys'

t = dynamodb.Table(table_name)
t = Table(table)
t.put_item(Item=record)
