#!/usr/bin/python

from __future__ import print_function
from __future__ import division

import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')

## Query DB and get all the teams
def getTeams():
  season=2017
  t = dynamodb.Table('nepreprpiteams')
  teams = t.query(KeyConditionExpression=Key('season').eq(season),
                   IndexName='season-name-index',
  )

  return teams['Items']

## Query DB and get all the games
def getGames():
  season=2017
  g = dynamodb.Table('nepreprpiboys')
  games = g.query(KeyConditionExpression=Key('season').eq(season))

  return games['Items']


## Loop through the games and calculate the wins and losses
def getRecords(games,teams):
  record = {}
  for game in games:
    # Set the wins and losses to 0
    if game['winner'] not in record:
      record[game['winner']] = {}
      record[game['winner']]['win'] = 0
      record[game['winner']]['loss'] = 0
    if game['loser'] not in record:
      record[game['loser']] = {}
      record[game['loser']]['win'] = 0
      record[game['loser']]['loss'] = 0

    record[game['winner']]['win'] += 1
    record[game['loser']]['loss'] += 1

  # calculate winpct
  for team in teams:
    record[team['name']]['winpct'] = record[team['name']]['win']/(record[team['name']]['win']+record[team['name']]['loss'])

  return record

def printTeamTableHandler(event, context):

  games = getGames()
  teams = getTeams()
  team = event['team']

  content = "<html><body><table width=\"60%\"><caption>"+team+" Results</caption>\n<tr><th>Team</th><th>Score</th><th>Opponent</th></th><th>Score</th><th>Date</th></tr>\n"
  for game in games:
    if team == game['winner'] or team == game['loser']:
      content += "<tr><td>"+game['winner']+"</td><td>"+str(game['scores']['winner'])+"</td><td>"+game['loser']+"</td><td>"+str(game['scores']['loser'])+"</td><td>"+game['date']+"</td></tr>\n"

  content += "</table></body></html>"
  return content

