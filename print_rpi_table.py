#!/usr/bin/python

import json
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
def getRecords(games):
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

  return record

def printRpiTableHandler (event, context):

  games = getGames()

  record = getRecords(games)

  teams = getTeams()

def printRpiTableHandler (event, context):

  games = getGames()

  record = getRecords(games)

  teams = getTeams()

  content = "<html><body>\n"
  content += "<table>\n<tr><th>Name</th><th>Wins</th><th>Loss</th><th>WPCT</th></tr>\n"
  for team in teams:
    content += "<tr><td>"+team['name']+"</td>"
    content += "<td>"+str(record[team['name']]['win'])+"</td>"
    content += "<td>"+str(record[team['name']]['loss'])+"</td>"
    winpct = record[team['name']]['win']/(record[team['name']]['win']+record[team['name']]['loss'])
    content += "<td>%0.2f" % winpct
    content += "</td>"
    content += "</tr>\n"

  content += "</table>\n</body></html>"
  print content
  return content

printRpiTableHandler("HTTP","Something")
