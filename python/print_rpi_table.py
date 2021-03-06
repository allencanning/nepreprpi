#!/usr/bin/python

from __future__ import print_function
from __future__ import division

import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')

print('Loading function')

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

def getOwpct(games,record,team):
  numteams = 0
  owpct = 0
  for g in games:
    if team != g['winner']:
      numteams += 1
      owpct += record[g['winner']]['winpct']
    if team != g['loser']:
      numteams += 1
      owpct += record[g['loser']]['winpct']

  owpctavg = owpct / numteams
  
  return owpctavg

def getOOwpct(games,record,team):
  numteams = 0
  oowpct = 0
  for g in games:
    if team != g['winner']:
      numteams += 1
      owpct = getOwpct(games,record,g['winner'])
      oowpct += owpct
    if team != g['loser']:
      numteams += 1
      owpct = getOwpct(games,record,g['loser'])
      oowpct += owpct

  oowpctavg = oowpct / numteams

  return oowpctavg

def printRpiTableHandler (event, context):

  # Get all game results
  games = getGames()
  
  # Get all team names
  teams = getTeams()
  
  # build record entries
  record = getRecords(games,teams)

  content = '<html><body><table width="60%"><caption>New England Preps Lacrosse RPI</caption><tr><th>Name</th><th>Wins</th><th>Loss</th><th>WPCT</th><th>OWPCT</th></tr>'
  for team in teams:
    content += '<tr><td><a href="https://9pd8zvy326.execute-api.us-east-1.amazonaws.com/prod/printTeamTableHandler?team='+team['name']+'">'+team['name']+'</a></td>'
    content += '<td>'+str(record[team['name']]['win'])+'</td>'
    content += '<td>'+str(record[team['name']]['loss'])+'</td>'
    owpct = getOwpct(games,record,team['name'])
    content += "<td>%0.2f" % owpct
    content += "</td>"
    oowpct = getOOwpct(games,record,team)
    content += "<td>%0.2f" % oowpct
    content += "</td>"
    content += "</tr>\n"

  content += '</table></body></html>'
  return content


