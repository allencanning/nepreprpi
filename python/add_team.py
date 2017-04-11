#!/usr/local/bin/python3

import time
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key,Attr
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-t","--team",dest="team",
                  help="Enter Team Name -- REQUIRED")
parser.add_option( "-s","--season",dest="season",
		  help="Enter Season -- Defaults to current")
parser.add_option( "-u","--url",dest="url",
		  help="Enter website URL -- REQUIRED")
parser.add_option( "-g","--gender",dest="gender",
		  help="Enter Gender -- REQUIRED")

(options, args) = parser.parse_args()

if not options.team:
  print("Please specify a team.")
  parser.print_help()
  exit(1)

if not options.url:
  print("Please specify a url.")
  parser.print_help()
  exit(1)

if not options.gender:
  print("Please specify a gender.")
  parser.print_help()
  exit(1)

if not options.season:
  options.season = int(datetime.strftime(datetime.today(),"%Y"))

# create the record
record = {}
record['season'] = options.season
record['name'] = options.team
record['url'] = options.url

dynamodb = boto3.resource('dynamodb')

table_name = ""
if options.gender == "female":
  table_name = 'nepreprpigirlsteams'
elif options.gender == "male":
  table_name = 'nepreprpiboysteams'

t = dynamodb.Table(table_name)
t.put_item(Item=record)

print("Added team ("+options.team+")")
