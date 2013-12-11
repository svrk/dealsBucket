import os

from redis import Redis
from config import UVConfig
from decorators import *

@singleton
class UVCache(Redis):
  def __init__(self):
    Redis.__init__(self, UVConfig().get_config_value("platform", "redis_server"))

if __name__ == "__main__":
  conf = UVConfig()
  conf.init("/home/uvadmin/dealsBucket/conf/deals_bucket.conf")

  print UVCache().hset("fadsfldasl-adfgaf0a-dsf", "channel",'1')
