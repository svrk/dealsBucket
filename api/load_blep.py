import  sys
import  os
import  re
import  urllib
import  json
from config import UVConfig
from cache_server import UVCache 

"""
	Sample code to demonstrate the BlipADeal API
	
	Written By By: Sido.B - 13th JULY 2012
	
	For further information please visit : www.blipadeal.com/dev-api
	For Online working demo please visit : webapi.blipadeal.com/webapi
	For support or help please email     : support@blipadeal.com 

"""

class Blipadeal_API:


	def __init__(self):
		pass


	"""
		"Generic function to send the request to the API"
	"""
	def _call_function(self, function_name, json_object):

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
	def _get_deals_of_category_type_in_given_location(self, country, city):
		json_request = {
			'free_text' : urllib.quote('I want to buy a Cheap ipod or iPhone & maybe a computer')
		}
		response_JSON = self._call_function(
			'api_get_category_type',
			json_request
		)
		response_status    = response_JSON['message_action']
		preferred_category = None

		if response_status == 'GET_CATEGORY_TYPE_SUCCESS':
			category_array = response_JSON['api_category_type' ]
			category_num   = response_JSON['api_category_count']
			if category_num > 1:
				print 'Preferred Category 1 = ' + category_array[0][0]
				print 'Preferred Category 2 = ' + category_array[1][0]
			else:
				print 'Only One Preferred Category = ' + category_array[0][0]
			# end if
			preferred_category = category_array[0][0]
		# end if

		"""
			Now lets look for all the items that match this category and
			find them all in Sydney
		"""

		json_request_2 = {
			"city_select"    : city,
			"country_select" : country,
			"category_list"  : [preferred_category],
			"sort_method"    : "bought"
		}
                response_JSON_2 = self._call_function(
                        'api_get_category_deals',
                        json_request_2
                )

		response_status_2 = response_JSON_2['message_action']
		if response_status_2 == 'DEAL_RETRIEVE_SUCCESS':
			deals_from_sydney = response_JSON_2['deal_list']
			print 
			print "------------------- DEALS FROM "+city+" -------------------"
			# just print out the first 50 deal summaries
			count = 0
			for deal in deals_from_sydney[0:50]:
				# truncate the string
				count = count + 1
				print str(count) + '		' + deal['blp_main_deal_summary'][0:100] + '...'
		return response_JSON_2

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
	def _get_deals_given_keywords(self, country, city):
		json_request = {
			'param_city'         : city,
			'param_country'      : country ,
			'param_keyword_list' : [
							urllib.quote("holiday"),
							urllib.quote("bali"   ),
							urllib.quote("relax"  )
				],
			'param_sort_method'  : "bought"
		}					
                response_JSON   = self._call_function(
                        'api_keyword_search',
                        json_request
                )
		return response_JSON

	def load_all_deals_by_country_and_city(self):
          """
          LOADS ALL DEALS FROM BLEP A DEAL INTO THE REDIS
          """
          #find the countries in blep api
           
          response_JSON = self._get_all_countries()
          response_status = response_JSON['message_action']
          if response_status == 'COUNTRY_RETRIEVE_SUCCESS':
            country_list = response_JSON['country_list']
            for country in country_list:
              country_name = country['blp_main_deal_detail_country_location']
              
              #get all cities from their countries 
              city_list_response_JSON = self._get_all_cities_from_a_country(country_name)
              city_response_status = city_list_response_JSON['message_action']

              if city_response_status == 'CITY_RETRIEVE_SUCCESS':
                city_list = city_list_response_JSON['location_list']
                for city in city_list:
                  city_name    = city['deal_location']
                  country_name = city['deal_country' ]
                              
                  deals_response_JSON = self._get_deals_given_keywords(country_name, city_name)           
                  deals_response_status = deals_response_JSON['message_action']
                  #TODO
                  UVCache().hset(country_name, city_name, '')   

                  if deals_response_status == 'DEAL_RETRIEVE_SUCCESS':
                    deals_list = deals_response_JSON['deal_list']
                    uv_deal = {}

                    for deal in deals_list:
                      uv_deal['deal_img_ref'] = deal['blp_main_deal_img_ref']
                      uv_deal['deal_url'] = deal['blp_main_deal_url_ref']
                      uv_deal['deal_price'] = deal['blp_main_deal_deal_price']
                      uv_deal['deal_discount'] = deal['blp_main_deal_savings']
                     
                      UVCache().hset(country_name, city_name, str(UVCache().hget(country_name, city_name)) +','+ str(uv_deal))
          print "completed"            





"""
	START TEST PROGRAM...
"""
if __name__ == '__main__':
	sample = Blipadeal_API()
	#sample._start()
        conf = UVConfig()
        conf.init('/home/uvadmin/dealsBucket/conf/deals_bucket.conf') 
        sample.load_all_deals_by_country_and_city() 
# end if
