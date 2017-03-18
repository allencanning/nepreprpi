#!/usr/local/bin/python3

import time
import re
import boto3
from optparse import OptionParser
from openpyxl import load_workbook

def readRecords(sheet,infile):
  records = []
  wb = load_workbook(infile)
  for ws in wb:
    if ws.title != sheet:
      continue
    for row in ws.rows:
      # Build array of data records
      if not row[0].value or row[0].value == "School Name":
        continue
      url = ""
      if row[2].value:
        url = re.sub(r"=HYPERLINK\(\"","",row[2].value)
        url = re.sub(r"\",.*$","",url)
      records.append({'name': row[0].value, 'season': int(row[1].value), 'url': url})

  return records

def writeRecords(table,records):
  for record in records:
    print("Adding team "+record['name'])
    table.put_item(Item=record)

parser = OptionParser()
parser.add_option("-f", "--file", dest="file",
                  help="Team import file")
parser.add_option("-t", "--table", dest="table",
                  help="Dynamodb Table to use (defaults to nepreprpiboysteams")
parser.add_option("-s", "--sheet", dest="sheet",
                  help="XLS sheet to read")

(options, args) = parser.parse_args()

if not options.file:
  print("Please specify an input file\n\n")
  parser.print_help()
  exit(1)

if not options.sheet:
  print( "Please specify a sheet\n\n")
  parser.print_help()
  exit(1)

# Set the table from the options listed on the command line
if not options.table:
  table = "nepreprpiteams"
else:
  table = options.table

dynamodb = boto3.resource('dynamodb')

# connect to the dynamodb table
t = dynamodb.Table(table)

# Read the file and build records
records = readRecords(options.sheet,options.file)

# Write the records to the DB
writeRecords(t,records)
