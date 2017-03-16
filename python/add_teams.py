#!/usr/bin/python

import time
import boto.dynamodb2
from boto.dynamodb2.fields import HashKey, RangeKey, KeysOnlyIndex, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER
from optparse import OptionParser

def readRecords(infile):
  records = []
  with open(infile,"r") as f:
    for line in f:
      # split the line into fields
      data = line.split(",")
      # Build array of data records
      records.append({'name': data[0], 'season': int(data[1]), 'url': data[2]})

  return records

def writeRecords(table,records):
  for record in records:
    print "Adding team "+record['name']
    table.put_item(data=record)

parser = OptionParser()
parser.add_option("-f", "--file", dest="file",
                  help="Team import file")
parser.add_option("-t", "--table", dest="table",
                  help="Dynamodb Table to use (defaults to nepreprpiteams")

(options, args) = parser.parse_args()

if not options.file:
  print "Please specify an input file\n\n"
  parser.print_help()
  exit(1)

# Set the table from the options listed on the command line
if not options.table:
  table = "nepreprpiteams"
else:
  table = options.table

# connect to the dynamodb table
t = Table(table)

# Read the file and build records
records = readRecords(options.file)

# Write the records to the DB
writeRecords(t,records)
