#!/usr/local/bin/python3

import time
import boto3
import pprint
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-t","--table TABLENAME",dest="table",
                  help="Enter Table Name-- REQUIRED")

(options, args) = parser.parse_args()

if not options.table:
  parser.print_help()
  exit(1)

# connect to region
dynamodb = boto3.resource('dynamodb')

# Create table
t = dynamodb.create_table(
  TableName=options.table,
  KeySchema=[
    {
      'AttributeName': 'name',
      'KeyType': 'HASH'
    },
   ], AttributeDefinitions=[
      {
        'AttributeName': 'name',
        'AttributeType': 'S',
      },
      {
        'AttributeName': 'season',
        'AttributeType': 'N',
      },
   ],
   ProvisionedThroughput={
     'ReadCapacityUnits' : 10,
     'WriteCapacityUnits' : 2,
   }, GlobalSecondaryIndexes=[
     { 
      'IndexName': 'season-name-index',
       'KeySchema': [
         {
	   'AttributeName': 'season',
           'KeyType': 'HASH',
         },
         {
           'AttributeName': 'name',
           'KeyType': 'RANGE',
         }
       ],
       'Projection': {
         'ProjectionType': 'ALL',
         },
         'ProvisionedThroughput': {
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 2
         }
       },
   ],
)
