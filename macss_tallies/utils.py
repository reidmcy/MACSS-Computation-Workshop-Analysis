import urllib
import json
import datetime
import shutil
import os.path

import dateutil
import requests
#import pandas
#import matplotlib.pyplot as plt

apiURL = 'https://api.github.com'
tokenFile = os.path.normpath(os.path.join(os.path.dirname(__file__) + '/..' , 'token.txt'))
workshopOrgName = 'uchicago-computation-workshop'
#This is likely to change, https://developer.github.com/v3/reactions/
reactionsHeader = {'Accept' : 'application/vnd.github.squirrel-girl-preview'}

emojiMapping = {
    '+1' : '👍',
    '-1' : '👎',
    'heart' : '❤️',
    'hooray' : '🎉',
    'laugh' : '😄',
    'confused' : '😕',
}

def getGithubURL(target, headers = None):
    try:
        with open(tokenFile) as f:
            username, token = f.readline().strip().split()
            auth = (username, token)
    except FileNotFoundError:
        auth = None
    if target.startswith('http:'):
        url = target
    else:
        url = urllib.parse.urljoin(apiURL, target)
    r = requests.get(url, auth = auth, headers = headers)
    if not r.ok:
        raise RuntimeError('Invalid request: {}\n{}'.format(url, r.text))
    try:
        return json.loads(r.text)
    except json.JSONDecodeError:
        return []

def getRepos():
    orgInfo = getGithubURL('orgs/{}'.format(workshopOrgName))
    reposInfo = getGithubURL(orgInfo['repos_url'])
    currentRepos = sorted(reposInfo, key = lambda x : dateutil.parser.parse(x['created_at']), reverse = False)[2:]
    return currentRepos

def getIssueInfo(issueDict):
    reactions = getGithubURL('{}/reactions'.format(issueDict['url']), headers = reactionsHeader)
    return {
        'title' : issueDict['title'],
        'body' : issueDict['body'],
        'url' : issueDict['html_url'],
        'auth' : issueDict['user']['login'],
        'reactions' : ''.join(sorted([emojiMapping[r['content']] for r in reactions], reverse = True)),
        }

def printIssue(issueDat):
    width = shutil.get_terminal_size((80, 20)).columns
    print(issueDat['title'][:width])
    print(issueDat['url'][:width])
    print(issueDat['auth'][:width])
    print(issueDat['reactions'][:width])

def getIssues(repoDict):
    print("Getting questions for: {}".format(repoDict['name']))
    issues = getGithubURL("{}/issues".format(repoDict['url']))
    issuesInfo = []
    for i, issue in enumerate(issues):
        print("Querying GitHub: {:.0f}%".format(i / len(issues) * 100), end = '\r')
        issuesInfo.append(getIssueInfo(issue))
    issuesInfo = sorted(issuesInfo, key = lambda x : len(x['reactions']))
    for issueDat in issuesInfo:
        printIssue(issueDat)
