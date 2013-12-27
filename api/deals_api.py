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


@app.route('/uvdeals/', methods=['POST', 'GET'])
def newcall():
  print "ucp request url {0}".format(request.url)

  head, tail = os.path.split(request.url) 

  if str(tail):
    tail = str(tail.strip('?'))

    #if tail.split('=')[0] == 'division_id':  
    #  response = UVDeals().get_deals_by_division(division_id = str(tail.split('=')[1]))
    #else: 
    #  response = "{{'error':{'message': division_id is required as a URL parameter; Example: ?client_id=[your API key]','httpCode':400}}" 
    l_country = ''
    l_city = '' 
    l_division = ''
    response = ''
    #tail = tail + ','
    for l_opt in tail.split(','):
      if l_opt.split('=')[0] == 'country':
        l_country = l_opt.split('=')[1]
      if l_opt.split('=')[0] == 'city':
        l_city = l_opt.split('=')[1]
      if l_opt.split('=')[0] == 'division_id':
        l_division = l_opt.split('=')[1]
    if l_division != '':
      response = UVDeals().get_deals_by_division(division_id = division_id)    
    else:
      response = UVDeals().get_deals_by_country_and_city(l_country, l_city)  
      
  else:
    response = "{{'error':{'message': division_id or country,city are required as a URL parameter; Example: ?country=[country_name],city=[city_name] ','httpCode':400}}" 
    pass
    #TODO response for getting deals without division_id

  return Response(str(response), mimetype='application/json')


@app.route('/error/', methods=['POST', 'GET'])
def error():
  print "ucp request url - {0}".format(request.url)
  for key in request.form:
    print '{0} - {1}'.format(key,request.form.get(key,''))

  #web app should implement business logic here such as actions need to be performed before hangup

  response = "<Response>  </Response>"
  return Response(str(response), mimetype='application/json')

if __name__ == "__main__":
  port = int(os.environ.get('PORT', 4000))
  app.debug = True
  app.run(host='0.0.0.0', port=port)
