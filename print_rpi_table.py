#!/usr/bin/python

import time
from datetime import datetime
import boto.dynamodb2
from boto.dynamodb2.fields import HashKey, RangeKey, KeysOnlyIndex, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER
import pprint

pp = pprint.PrettyPrinter(indent=4)

## Query DB and get all the teams
def getTeams():
  season=2017
  t = Table('nepreprpiteams')
  teams = t.query_2(season__eq=season,
                   index='season-name-index',
  )

  return teams

## Query DB and get all the games
def getGames():
  season=2017
  g = Table('nepreprpiboys')
  games = g.query_2(season__eq=season)

  return games

## Loop through the games and calculate the wins and losses
def getRecords(games):
  record = {}
  for game in games:
    # Set the wins and losses to 0
    if game['winner'] not in record:
      print "Winner = "+game['winner']
      record[game['winner']] = {}
      record[game['winner']]['win'] = 0
      record[game['winner']]['loss'] = 0
    if game['loser'] not in record:
      print "Loser = "+game['loser']
      record[game['loser']] = {}
      record[game['loser']]['win'] = 0
      record[game['loser']]['loss'] = 0

    record[game['winner']]['win'] += 1
    record[game['loser']]['loss'] += 1

  return record

games = getGames()

record = getRecords(games)

teams = getTeams()

print "<table>\n<tr><th>Name</th><th>Wins</th><th>Loss</th><th>WPCT</th></tr>\n"
for team in teams:
  print "<tr><td>"+team['name']+"</td>"
  print "<td>"+str(record[team['name']]['win'])+"</td>"
  print "<td>"+str(record[team['name']]['loss'])+"</td>"
  winpct = record[team['name']]['win']/(record[team['name']]['win']+record[team['name']]['loss'])
  print "<td>%0.2f" % winpct
  print "</td>"
  print "</tr>\n"

print "</table>\n"
