from __future__ import print_function
from __future__ import division

import time
from datetime import datetime
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

def printFormData(teams):
  months = { 1: 'Jan',
             2: 'Feb',
             3: 'Mar',
             4: 'Apr',
             5: 'May',
             6: 'Jun',
             7: 'Jul',
             8: 'Aug',
             9: 'Sep',
             10: 'Oct',
             11: 'Nov',
             12: 'Dec'
  }
  content = '<form name="process" method="post" action="https://9pd8zvy326.execute-api.us-east-1.amazonaws.com/prod/addGameHandler">'
  content += '<div class="header">Enter Game Results<p>Winner:<select name="winner">'
  content += '<option value="">'
  for team in teams:
    content += '<option value="'+team['name']+'">'+team['name']+'</option>'
  content += '</select>'
  content += 'Score: <input type="text" name="winner_score">'
  content += '<p>Loser:<select name="loser">'
  content += '<option value="">'
  for team in teams:
    content += '<option value="'+team['name']+'">'+team['name']+'</option>'
  content += '</select>'
  content += 'Score: <input type="text" name="loser_score">'
  game_date = datetime.strftime(datetime.today(),"%m/%d/%Y")
  content += '<br>Date: <select name="month">'
  for month in sorted(months):
    content += '<option value="'+month+'">'+months[month]
  content += '</select>'
  content += '<br><input type="submit" name="Add Game" value="Add Game">'
  content += '<input type="reset">'
  content += '<input type="hidden" name="action" value="Process"></form>'
  return content
  
def addGameHandler(event, context):
  if 'action' in event:
    action=event['action']
  else:
    action="Form"
  
  css = '<link rel="stylesheet" href="https://s3.amazonaws.com/nepreprpi/neprep.css" type="text/css" />'
  script = '<script type="text/javascript src="https://s3.amazonaws.com/nepreprpi/neprepformcheck.js"></script>'
  content = "<html><head>"+css+script+"</head><body>"

  teams = getTeams()

  if action == 'Process':
    winner=event['winner']
    loser=event['loser']
    date=event['game_date']
    ws=event['winner_score']
    ls=event['loser_score']
    
    # create the record
    record = {}
    record['season'] = int(datetime.strftime(datetime.today(),"%Y"))
    record['teams'] = winner+loser
    record['winner'] = winner
    record['loser'] = loser
    record['date'] = date
    record['scores'] = {}
    record['scores']['winner'] = ws
    record['scores']['loser'] = ls
    t = dynamodb.Table('nepreprpiboys')
    t.put_item(data=record)
    content += '<p>Successful addtion of game'
  else:
    content += printFormData(teams)

  content += "</body></html>"
  return content
