from flask import Flask, url_for, Response, request
import httplib, urllib
app = Flask(__name__)
import random
import os,sys
import urllib2
import simplejson as json

try:
  DEALSBUCKET = os.environ['DEALSBUCKET']
except:
  DEALSBUCKET = "/home/uvadmin/dealsBucket/"

from deals import UVDeals
from cache_server import UVCache
from config import UVConfig
from json_util import JsonParser

conf = UVConfig()
conf.init(DEALSBUCKET+"conf/deals_bucket.conf")


@app.route('/deals/', methods=['POST', 'GET'])
def deals():
  print "ucp request url {0}".format(request.url)

  head, tail = os.path.split(request.url) 

  if str(tail):
    tail = str(tail.strip('?'))
    l_country = ''
    l_city = '' 
    response = ''
    for l_opt in tail.split(','):
      if l_opt.split('=')[0] == 'country':
        l_country = l_opt.split('=')[1]
      if l_opt.split('=')[0] == 'city':
        l_city = l_opt.split('=')[1]
    if l_country != '' and l_city != '':
      response = UVDeals().get_deals_by_country_and_city(l_country, l_city)    
      
  else:
    response = "{{'error':{'message': country or country,city are required as a URL parameter; Example: ?country=[country_name],city=[city_name] ','httpCode':400}}" 
    pass
    #TODO response for getting deals without division_id

  return Response(str(response), mimetype='application/json')


@app.route('/deals_by_category/', methods=['POST', 'GET'])
def deals_by_category():
  print "ucp request url {0}".format(request.url)

  head, tail = os.path.split(request.url)

  if str(tail):
    tail = str(tail.strip('?'))

    l_country = ''
    l_city = ''
    l_category = ''
    response = ''
    for l_opt in tail.split(','):
      if l_opt.split('=')[0] == 'country':
        l_country = l_opt.split('=')[1]
      if l_opt.split('=')[0] == 'city':
        l_city = l_opt.split('=')[1]
      if l_opt.split('=')[0] == 'category':
        l_category = l_opt.split('=')[1]
    if l_category != '':
      response = UVDeals().get_deals_by_category(l_country, l_city, l_category = l_category)
    else:
      response = UVDeals().get_deals_by_country_and_city(l_country, l_city)

  else:
    response = "{{'error':{'message': category or country,city are required as a URL parameter; Example: ?country=[country_name],city=[city_name] ','httpCode':400}}"
    pass

  return Response(str(response), mimetype='application/json')



if __name__ == "__main__":
  port = int(os.environ.get('PORT', 4000))
  app.debug = True
  app.run(host='0.0.0.0', port=port)
