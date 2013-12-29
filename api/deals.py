import json
from decorators import *
from config import UVConfig
from cache_server import UVCache
from json_util import JsonParser

@singleton
class UVDeals(object):
  """ This class used for getting deals """

  def get_deals(self):
    #TODO
    pass  
 

  def get_deals_by_category(self,l_country, l_city, l_category=''):
    redis_key_1 = l_country + '_'  + l_city
    redis_key_2 = l_category    
    response_json = {}       
    deals = UVCache().hget(redis_key_1, redis_key_2)
    if deals == None:
      deals = ''
    response_json['deals'] = list(eval(deals))
    return response_json  


  def get_deals_by_country_and_city(self, l_country = '', l_city = ''):
    response_json = {}       
    deals = UVCache().hget(l_country, l_city)   
    if deals == None:
      deals = '' 
    response_json['deals'] = list(eval(deals))

    return response_json



