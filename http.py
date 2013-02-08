#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httplib
from optparse import OptionParser
from urlparse import urlparse
from time import sleep 

def main():
  parser = OptionParser()
  parser.add_option("-u", "--url", dest="url",help="input you want to connect web site's url.")
  parser.add_option("-t", "--time", dest="time",help="input you want to connect time.")
  parser.add_option("-r", "--requesttype", dest="req_type",default="1",help="1:In the same connection to send requests.,2:Connection to send the request every time.")
  parser.add_option("-w", "--waittime", dest="wait",help="If you send multiple requests, it is time to wait before sending the next request.(sec)")
  (options, args) = parser.parse_args()

  parsed_url = urlparse(options.url)

  # ポートの有り無しでコネクションの仕方を分ける
  #if parsed_url.port == None:
  #  conn = parsed_url.hostname
  #else:
  #  conn = parsed_url.hostname + ':' + str(parsed_url.port)
  conn = parsed_url[1]

  # クエリストリングの有り無しでリクエストを分ける
  if parsed_url[4] != '':
    req = parsed_url[2] + '?' + parsed_url[4]
  else:
    req = parsed_url[2]

  # オプションで指定された回数だけリクエストを送る
  if options.time == None:
    time = 1
  else:
    time = int(options.time)

  # sleep時間の設定
  if options.wait == None:
    wait = 0
  else:
    wait = int(options.wait)

  # コネクションタイプ
  if options.req_type == '1':
    print 'In the same connection to send requests.'
    same_connection(conn,req,time,wait)
  else:
    print 'Connection to send the request every time.'
    other_connection(conn,req,time,wait)

# 異なるコネクションで複数回のGETを送る
def other_connection(conn,req,time,wait):
  for i in range(time):
    # コネクションを張る
    h = httplib.HTTPConnection(conn)

    h.request('GET', req)
    r = h.getresponse()

    #if r.status == httplib.OK:
    if r.status == 200:
      data = r.read()
      print data

    else:
      print 'Status=', r.status

    sleep(wait)


# 同一コネクション内で複数回のGETを送る
def same_connection(conn,req,time,wait):
  # コネクションを張る
  h = httplib.HTTPConnection(conn)

  for i in range(time):
    h.request('GET', req)
    r = h.getresponse()

    #if r.status == httplib.OK:
    if r.status == 200:
      data = r.read()
      print data

    else:
      print 'Status=', r.status

    sleep(wait)


if ( __name__ == "__main__" ):
  main()

