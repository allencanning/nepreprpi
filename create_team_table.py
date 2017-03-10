#!/usr/bin/python

import time
import boto.dynamodb2
from boto.dynamodb2.fields import HashKey, RangeKey, KeysOnlyIndex, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER
import pprint

pp = pprint.PrettyPrinter(indent=4)

# connect to region
con = boto.dynamodb2.connect_to_region('us-east-1')

#r=con.describe_table('nepreprpiteams')
#if r and r['Table']['TableStatus'] == 'ACTIVE':
#  nepreprpiteams = Table('nepreprpiteams')
#  nepreprpiteams.delete()

# Create table
nepreprpiteams = Table.create('nepreprpiteams', schema=[
   HashKey('name')
   ], throughput={
     'read' : 10,
     'write' : 2,
   }, global_indexes=[
     GlobalAllIndex('season-name-index', parts=[
      HashKey('season', data_type=NUMBER),
      RangeKey('name'),
   ],
   throughput={
    'read': 10,
    'write': 2,
   })
 ],
)
