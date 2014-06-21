'''
Created on May 31, 2014

@author Rainicy

@ref: https://github.com/mosqutip/EECS395_26/blob/master/Utils/getPostsFromUrl.py
'''

import urllib2
import urllib
import json
import time


disqus = {"key": 'sl7bIgSzV6S4Hdv3kVgHZrEAT5XhZdkReU83VWFzIxvesdSZJ0BDevlGJzi4F5Rq', 
          "url": 'http://disqus.com/api/3.0/threads/listPosts.json?api_secret={!s}&limit=100&thread=link:{!s}&forum=cnn',
          "next_url": 'http://disqus.com/api/3.0/threads/listPosts.json?api_secret={!s}&limit=100&thread=link:{!s}&forum=cnn&cursor={!s}'}


def parseDisqusURL(durl):
  '''
  Description: By given the Disqus API url to get the posts info from that URL.

  @param: url 
  @return: the information stored by json
  '''

  try:
    socket = urllib2.urlopen(durl)
    raw_json = socket.read()
    socket.close()
  except (urllib2.HTTPError):
    return json.loads('{"code":400}')
  parsed_json = json.loads(raw_json)
  return parsed_json


def parsePage(url, next=None, isFirst=True):
  '''
  Description: Given the CNN url, parse one page posts in the Disqus.

  @param: 
    url: CNN link
    next: next id in Disqus's cursor. 
    isFirst: if it's the first page, True, otherwise False.
  @return: the one page information stored by json
  '''
  if isFirst:
    durl = disqus['url'].format(disqus['key'], urllib.quote_plus(url))
  else:
    durl = disqus['next_url'].format(disqus['key'], urllib.quote_plus(url), next)
  return parseDisqusURL(durl)


def crawlComments(url):
  '''
  Description: given the url from CNN, crawl all the comments.

  @param:
    url: CNN link
  @return: All the comments from one article, stored by json.
  '''

  # First get the first page.
  json = parsePage(url, None, True)
  if json['code'] != 0: # None infomation
    return list()
  comments = json['response']

  # go through all the pages if exists.
  while (json['code'] == 0) and json['cursor']['hasNext']:
    json = parsePage(url, json['cursor']['next'], False)
    comments.extend(json['response'])

  return comments



def main():
  # open the links
  with open('linksCNN', 'r') as file:
    lines = file.readlines()
    file.close()

  # starting crawling the timestamps. 
  for count in range(55, 60):
    url = lines[count].split('\n')[0]
    print 'crawling ID: ' + str(count+1)
    # print url
    # raw_input()
    comments = crawlComments(url)
    # print len(comments)
    # raw_input()
    print 'writing  ID: ' + str(count+1)

    f = open('./timestamps/'+str(count+1), 'w')
    for comment in comments:
      creatTime = comment['createdAt']
      f.write(creatTime + '\n')
    f.close()

if __name__ == '__main__':
  main()

