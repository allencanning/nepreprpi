#!/usr/local/bin/python3

import time
import boto3
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-t","--table TABLENAME",dest="table",
                  help="Enter Table Name-- REQUIRED")

(options, args) = parser.parse_args()

if not options.table:
  parser.print_help()
  exit(1)

dynamodb = boto3.resource('dynamodb')

# Create table
nepreprpiboys = dynamodb.create_table(
  TableName=options.table,
  KeySchema=[
    {
      'AttributeName': 'season',
      'KeyType': 'HASH'
    },
    {
      'AttributeName': 'teams',
      'KeyType': 'RANGE',
    },
  ], AttributeDefinitions=[
    {
      'AttributeName': 'season',
      'AttributeType': 'N',
    },
    {
      'AttributeName': 'teams',
      'AttributeType': 'S',
    },
    {
      'AttributeName': 'date',
      'AttributeType': 'S',
    },
    {
      'AttributeName': 'loser',
      'AttributeType': 'S',
    },
    {
      'AttributeName': 'winner',
      'AttributeType': 'S',
    },
   ],
   ProvisionedThroughput={
     'ReadCapacityUnits' : 10,
     'WriteCapacityUnits' : 2,
   }, GlobalSecondaryIndexes=[
     { 
      'IndexName': 'winner-loser-index',
       'KeySchema': [
         {
           'AttributeName': 'winner',
           'KeyType': 'HASH',
         },
         {
           'AttributeName': 'loser',
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
     { 
      'IndexName': 'teams-date-index',
       'KeySchema': [
         {
           'AttributeName': 'teams',
           'KeyType': 'HASH',
         },
         {
           'AttributeName': 'date',
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
