import  sys
import  os
import  re
import  urllib
import  json
from config import UVConfig
from cache_server import UVCache 


class BlipDealAPI:


	def __init__(self):
          #config = UVConfig()
          #config.init()   
          pass 


	def _call_function(self, function_name, json_object):
	  """
    		function to send the request to the API
	  """

	  json_object["message_status"  ] = "SUCCESS"
	  json_object["api_key_token"   ] = "26A1EBFECCEA04CF5E112FBEC3FDC3B1"
	  json_object["api_secret_token"] = "D2EBD70347B118875A61AFDCB984CB20"

	  response_handle = urllib.urlopen(
			'https://webapi.blipadeal.com/' + function_name + '?request=' + json.dumps( json_object )
		)

	  JSON_object = json.loads(response_handle.read())
    	  return ( JSON_object )

	"""
		This function will get the location of all the places where there are deals within
		a 200km region
	"""
	def _get_deals_near_by_text(self, country, city, distance):
		json_request = {
			"param_city"    :  city,
			"param_country" :  country,
			"param_distance":  distance
		}

		response_JSON = self._call_function( 
			'api_get_deal_location_near_by_text',
			json_request
		)

		return response_JSON

	"""
		This function will take the longtitude and lattitude from 
		the third city returned from the '_get_deals_near_by_text' function call
		and use it to find what is close by that within a 500km radius
	"""
	def _get_deals_near_by_coord(self, json_coords ):

		point = json_coords['poi_list'][2]
		lat   = point['blp_publish_lat_pos']
		lng   = point['blp_publish_long_pos']

                json_request = {
                        "param_lng"     :  lng,
                        "param_lat"     :  lat,
                        "param_distance":  500
                }

                response_JSON = self._call_function( 
                        'api_get_deal_location_near_by_geo',
                        json_request
                )

                return response_JSON

	"""
		This function will get all the deals based on a phrase in the city of 
		sydney. Then it will look for deals near by sydney given the same phrase
	"""
	def _get_deals_of_category_type_in_given_location(self, country, city, category):
		json_request = {
			"city_select"    : city,
			"country_select" : country,
			"category_list"  : [category],
			"sort_method"    : "bought"
		}
                response_JSON = self._call_function(
                        'api_get_category_deals',
                        json_request
                )

		response_status = response_JSON['message_action']
		if response_status == 'DEAL_RETRIEVE_SUCCESS':
		  return response_JSON
                else: 
                  return '{}'  

	"""
		This function will retrieve all of the countries currently active within
		the blipADeal 
	"""
	def _get_all_countries(self):
		json_request    = {}
		response_JSON   = self._call_function(
			'api_get_country',
			json_request
		)
		return response_JSON

	"""
		This function will retrieve all the cities in a given country. You may want to use this
		to get deals from multiple cities
	"""
	def _get_all_cities_from_a_country(self, country):
		json_request = {
			"param_country"   : country 
		}
                response_JSON   = self._call_function(
                        'api_get_location',
                        json_request
                )
		return response_JSON
	
	"""
		This function will retrieive all the categories given a location
		defined by a city and country
	"""	
	def _get_all_category_from(self, country, city):
                json_request = {
                        "param_country"   : country,
			"param_city"      : city
                }
                response_JSON   = self._call_function(
                        'api_get_category',
                        json_request
                )

		return response_JSON

	"""
		This function will retrieve all the deals given a location and 
		specific keywords
	"""
	def _get_deals_given_keywords(self, country, city, keyword_list):

            url_encode_keyword_list = []
            for category in keyword_list:
              url_encode_keyword_list.append(urllib.quote(category))


              json_request = {
			'param_city'         : city,
			'param_country'      : country ,
			'param_keyword_list' : url_encode_keyword_list,
			'param_sort_method'  : "bought"
	      }					
              response_JSON   = self._call_function(
                        'api_keyword_search',
                        json_request
              )
	      return response_JSON

        def _get_deals(self, country, city):

                json_request = {
                        'param_city'         : city,
                        'param_country'      : country ,
                        'param_sort_method'  : "bought"
                }                                       
                response_JSON   = self._call_function(
                        'api_get_deals',
                        json_request
                )
                return response_JSON




       
          
   
class LoadBlipDeals(BlipDealAPI):
        
        def init(self):
          self.load_countries()
          self.load_cities()        
          self.load_categories()  
             

      	def load_all_deals_by_country_city(self):
          """
          LOADS ALL DEALS FROM BLEP A DEAL INTO THE REDIS
          """
          countries_list = self.get_countries()                       
          for country in countries_list:
            city_list = self.get_cities(country)
            for city in city_list:                  

              response_JSON = self._get_deals(country, city)           
              response_status = response_JSON['message_action']
              if (UVCache().hget(country, city) is None):
                UVCache().hset(country, city, '')   

              if response_status == 'DEAL_RETRIEVE_SUCCESS':
                deals_list = deals_response_JSON['deal_list']
                uv_deal = {}

                for deal in deals_list:
                  uv_deal['deal_img_ref'] = deal['blp_main_deal_img_ref']
                  uv_deal['deal_url'] = deal['blp_main_deal_url_ref']
                  uv_deal['deal_price'] = deal['blp_main_deal_deal_price']
                  uv_deal['deal_discount'] = deal['blp_main_deal_savings']
                     
                  UVCache().hset(country_name, city_name, str(UVCache().hget(country_name, city_name)) + str(uv_deal) +',')
               
                #TODO  
                #deals_category_list = deals_response_JSON['deal_category'] 
                #for deal_by_category in 




        def load_deals_by_category_country_city(self):
          """
          LOAD DEALS BY CATAGORY WITH COUNTRY AND CITY 
          """
          countries_list = self.get_countries()
          for country in countries_list:
            city_list = self.get_cities(country)
            for city in city_list:
              category_list = self.get_categories(country,city) 
              for category in category_list:
                redis_key_1 = country + '_'  + city
                redis_key_2 = category

                if (UVCache().hget(redis_key_1, redis_key_2) is None):
                  UVCache().hset(redis_key_1, redis_key_2, '')
                if not category:
                  category = 'Gadgets and Electronics'  
                response_JSON = self._get_deals_of_category_type_in_given_location(country, city, category)
                response_status = response_JSON['message_action']

                if response_status == 'DEAL_RETRIEVE_SUCCESS':
                  category_deals_list = response_JSON['deal_list']
                  uv_deal = {}
                  for deal in category_deals_list:
                    uv_deal['deal_img_ref'] = deal['blp_main_deal_img_ref']
                    uv_deal['deal_url'] = deal['blp_main_deal_url_ref']
                    uv_deal['deal_price'] = deal['blp_main_deal_deal_price']
                    uv_deal['deal_discount'] = deal['blp_main_deal_savings']

                    UVCache().hset(redis_key_1, redis_key_2, str(UVCache().hget(redis_key_1, redis_key_2)) +str(uv_deal) +',')
                   
              print 'loaded deals from country:'+country+' and city:'+city


        def reset_redis(self): 

          countries_list = self.get_countries()
          for country in countries_list:
            city_list = self.get_cities(country)
            for city in city_list:
              category_list = self.get_categories(country,city)
              UVCache().hset(country, city, '')          
              redis_key = country + '_'  + city
              
              for category in category_list:
                redis_val = category
                UVCache().hset(redis_key, redis_val, '')          


        def load_countries(self):
          response_JSON = self._get_all_countries()
          response_status = response_JSON['message_action']
          res_list = []
          if response_status == 'COUNTRY_RETRIEVE_SUCCESS':
            blip_country_list = response_JSON['country_list']
            for country in blip_country_list:
              res_list.append(str(country['blp_main_deal_detail_country_location']))
          UVCache().hset('blip', 'countries', res_list) 

        def load_cities(self):
          country_list = self.get_countries()
          for country in country_list:
            response_JSON = self._get_all_cities_from_a_country(country)
            response_status = response_JSON['message_action']
            res_list = []

            if response_status == 'CITY_RETRIEVE_SUCCESS':
              city_list = response_JSON['location_list']
              for city in city_list:
                res_list.append(str(city['deal_location']))
            UVCache().hset('cities', country, res_list) 

        def load_categories(self):
          country_list = self.get_countries()
          for country in country_list:
            city_list = self.get_cities(country)
            for city in city_list:  
              category_list = []
              response_JSON = self._get_all_category_from(country, city)
              response_status = response_JSON['message_action']
              if response_status == 'DEAL_CATEGORY_RETRIEVE_SUCCESS':
                category_deal_list = response_JSON['category_deal_list']

              for category_deal in category_deal_list:
                category_name  = category_deal['blp_category_display']
                category_list.append(str(category_name))
              redis_key_1 = country + '_' + city
              UVCache().hset(redis_key_1, 'categories', category_list)



        def get_countries(self):
          res_list = UVCache().hget('blip', 'countries')
          if res_list is None:
            res_list = []
          else:
            res_list = eval(res_list) 
          return res_list  


        def get_cities(self, country):       
          res_list = UVCache().hget('cities', country)
          if res_list is None:
            res_list = []
          else:
            res_list = eval(res_list)  
          return res_list  


        def get_categories(self,country, city):
          redis_key = country + '_' + city
          res_list = UVCache().hget(redis_key, 'categories')
          if res_list is None:
            res_list = []
          else:
            res_list = eval(res_list)  
          return res_list  
        


if __name__ == '__main__':
        conf = UVConfig()
        conf.init('/home/uvadmin/dealsBucket/conf/deals_bucket.conf') 

	sample = LoadBlipDeals()
        sample.init()  
        #sample.load_all_deals_by_country_city() 
        sample.load_deals_by_category_country_city() 
