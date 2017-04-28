#!/usr/local/bin/python3

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
parser.add_option( "-g","--gender",dest="gender",
		  help="Enter gender -- REQUIRED")
parser.add_option( "-y","--year",dest="year",
		  help="Enter season -- Defaults to current")

(options, args) = parser.parse_args()

if not options.winner:
  print("Please specify a winning team.")
  parser.print_help()
  exit(1)

if not options.loser:
  print("Please specify a losing team.")
  parser.print_help()
  exit(1)

if not options.year:
  options.year = int(datetime.strftime(datetime.today(),"%Y"))
else:
  options.year = int(options.year)

dynamodb = boto3.resource('dynamodb')

table_name = ""
if options.gender == "female":
  table_name = 'nepreprpigirls'
elif options.gender == "male":
  table_name = 'nepreprpiboys'

t = dynamodb.Table(table_name)

t.delete_item(
  Key={
    'season': options.year,
    'teams': options.winner+options.loser
  }
)
