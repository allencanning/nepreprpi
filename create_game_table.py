#!/usr/bin/python

import time
import boto.dynamodb2
from boto.dynamodb2.fields import HashKey, RangeKey, KeysOnlyIndex, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER

# connect to region
con = boto.dynamodb2.connect_to_region('us-east-1')

# Create table
nepreprpiboys = Table.create('nepreprpiboys', schema=[
    HashKey('season', data_type=NUMBER),
    RangeKey('teams'),
  ], throughput={
    'read' : 10,
    'write' : 2,
  }, global_indexes=[
    GlobalAllIndex('WinnerLoserIndex', parts=[
      HashKey('winner'),
      RangeKey('loser'),
    ],
    throughput={
      'read': 10,
      'write': 2,
    })
  ],
)
