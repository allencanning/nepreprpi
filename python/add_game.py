#!/usr/bin/python

import time
from datetime import datetime
import boto.dynamodb2
from boto.dynamodb2.fields import HashKey, RangeKey, KeysOnlyIndex, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER
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

t = Table('nepreprpiboys')

t.put_item(data=record)
