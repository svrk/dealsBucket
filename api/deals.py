import json
from decorators import *
from config import UVConfig
from cache_server import UVCache
from json_util import JsonParser

conf = UVConfig()
conf.init("/home/uvadmin/ucp/conf/deals.conf")

@singleton
class UVDeals(object):
  """ This class used for getting deals """

  def get_deals(self):
 
#    deals_list = eval(UVCache().get('deals'))
#    json_deals = JsonParser().to_json(deals_list) 
   
#    return json_deals 
    pass  


  def get_deals_by_division(self, division_id=''):
    
    #deal_api_name = conf.get_config_value("deals","apis")

    #TODO add deals from different deal api's
    deals = UVCache().hget('groupon_deals', division_id)
    return deals  


  def get_deals_by_country_and_city(self, country = '', city = ''):

    #deal_api_name = conf.get_config_value("deals","apis")

    #TODO add deals from different deal api's
    deals = UVCache().hget(country, city)
    return deals





#class Deal(object):

#  def __init__(self):
#    self.price = '10'
#    self.websiteurl = 'www.groupon.com'
#    self.discount = '5'

#  def set_price(self, price):
#    self.price = price
#  def set_websiteurl(self, websiteurl):
#    self.websiteurl = websiteurl
#  def set_discount(self, discount):
#    self.discount = discount

#  def get_price(self):
#    return self.price
#  def get_websiteurl(self):
#    return self.websiteurl
#  def get_discount(self):
#    return self.discount




