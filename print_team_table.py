#!/usr/bin/python

import time
from datetime import datetime
import boto.dynamodb2
from boto.dynamodb2.fields import HashKey, RangeKey, KeysOnlyIndex, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER

def getTeams():
  season=2017
  t = Table('nepreprpiteams')
  teams= t.query_2(season__eq=season,
                   index='season-name-index',
  )

  return teams

teams = getTeams()

print "<table>\n<tr><th>Name</th><th>Season</th><th>URL</th></tr>\n"
for team in teams:
  print "<tr><td>"+team['name']+"</td>"
  print "<td>"+str(team['season'])+"</td>"
  print "<td>"+team['url']+"</td>"
  print "</tr>\n"

print "</table>\n"
