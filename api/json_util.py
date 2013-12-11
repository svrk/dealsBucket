
#from config import UVConfig
#from cache_server import UVCache
#from uv_decorators import *


#@singleton
class JsonParser(object):

  def get_json_deal(self, deal = ''):
    
    #json_deal = '{' + '\"price\":' + deal.get_price() + ',\"websiteurl\":' + deal.get_websiteurl() + ',\"discount\":' + deal.get_discount() + '}'
    json_deal = {}
    json_deal['price'] = deal.get_price()
    json_deal['websiteurl'] = deal.get_price()
    json_deal['discount'] = deal.get_price()
        
    return(json_deal)


  def to_json(self, deals_list):

    #json_response = '{\"deals\":['

    #for deal in deal_list:
    #   json_response = json_response + self.get_json_deal(deal) + ','
    
    #json_response = json_response[:-1]
    #json_response += ']}'

    json_deals = {}
    json_deals_list = []
    for deal in deals_list:
      json_deals_list.append(self.get_json_deal(deal))
    
    json_deals['deals'] = json_deals_list

    return(json_deals) 





if __name__ == '__main__':


  deal1 = Deal()
  deal2 = Deal()
  deal3 = Deal()

  deal_list = [deal1, deal2, deal3]
 
  print JsonParser().to_json(deal_list)  
  


  



