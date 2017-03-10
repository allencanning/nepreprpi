#!/usr/bin/python

import time
import boto.dynamodb2
from boto.dynamodb2.fields import HashKey, RangeKey, KeysOnlyIndex, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER

nepreprpiteams = Table('nepreprpiteams')

nepreprpiteams.put_item(data={
  'name': 'Brooks',
  'season': 2017,
  'url': 'http://www.brooksschool.org',
})

nepreprpiteams.put_item(data={
  'name': 'Middlesex',
  'season': 2017,
  'url': 'http://www.mxschool.edu',
})
nepreprpiteams.put_item(data={
  'name': 'Deerfield',
  'season': 2017,
  'url': 'http://www.deerfield.edu',
})
nepreprpiteams.put_item(data={
  'name': 'Andover',
  'season': 2017,
  'url': 'http://www.andover.edu',
})
nepreprpiteams.put_item(data={
  'name': 'Pingree',
  'season': 2017,
  'url': 'http://www.pingree.org',
})

