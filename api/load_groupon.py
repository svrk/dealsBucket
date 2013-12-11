import os.path, sys
import urllib2
import simplejson as json

try:
  UCPHOME=os.environ['UCPHOME']
except:
  UCPHOME="/home/uvadmin/ucp/"

sys.path.append(UCPHOME+"core/")
from uv_decorators import *
from genutils import *
from cache_server import UVCache
from config import UVConfig

@singleton
class UVLoadGroupon(object):

  def __init__(self):
    self.api_tag_name = 'https://api.groupon.com/v2/'
    self.divisions = ''
    self.client_id = '5840312a67ffe3dca32c82e5324eb8f8049332df'  
 
  def init(self):
    response = urllib2.urlopen(self.get_divisions_url())
    divisions = json.loads(response.read())
    UVCache().hset('deals_bucket', 'groupon', '')
    deals_list = [] 
    for division in divisions['divisions']:
      deals_output = urllib2.urlopen(self.get_deals_url_by_division(division['id']))
      deals_response = json.loads(deals_output.read())
      ucp_deal = {}      
      UVCache().hset('groupon_deals',str(division['id']), '')

      for deal in deals_response['deals']:
        #print deal['dealUrl']
        for deal_options in deal['options']:
          ucp_deal['price']= deal_options['price'].get('formattedAmount')
          ucp_deal['discount'] = deal_options['discount'].get('formattedAmount')
          ucp_deal['deal_url'] = deal_options['buyUrl'] 

        UVCache().hset('groupon_deals',str(division['id']),UVCache().hget('groupon_deals', str(division['id']))+str(ucp_deal))
        UVCache().hset('groupon_deals',str(division['id']),UVCache().hget('groupon_deals', str(division['id']))+',')


      UVCache().hset('groupon_deals',str(division['id']),UVCache().hget('groupon_deals', str(division['id'])).strip(','))    
    print "completed"
 

  def get_deals_url_by_division(self, division_id = ''):
    url = self.api_tag_name + 'deals.json?division_id=' + division_id + '&client_id=' + self.client_id
    return url
    
  
  def get_divisions_url(self):
    url = self.api_tag_name + 'divisions.json?client_id=' + self.client_id
    return url







if __name__ == '__main__':

  conf = UVConfig()
  conf.init(UCPHOME+"conf/deals.conf")
  #print UVConfig().get_config_value("groupon", 'apis') 
  UVLoadGroupon().init()

  data = json.loads(UVCache().hget('groupon', 'deals'))

  #print data['deals'][0]['division']['id']
  #print type(data) 





