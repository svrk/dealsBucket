import base64
import PySQLPool
from uv_decorators import *
from uvjson_util import JsonParser
#from config import UVConfig


@singleton
class DBPool:
  def __init__(self):
    self.db_user_name = "root"
    self.db_user_password = "root"
    self.db_max_connections = "10"
    self.db_server = "127.0.0.1"
    #self.db_user_password = base64.b64decode(self.db_user_password)

    PySQLPool.getNewPool().maxActiveConnections = self.db_max_connections


  def execute_query(self, p_query, p_dbname):
    try:
      #logger.debug("query {0} dbname {1}".format(p_query, p_dbname))
      l_connection = PySQLPool.getNewConnection(username=self.db_user_name, password=self.db_user_password, host=self.db_server, db=p_dbname,  charset = "utf8")
      l_query = PySQLPool.getNewQuery(l_connection, True)
      l_retval = l_query.Query(p_query)
      #print l_query.affectedRows
      return True, l_retval, l_query.record
    except:
      #logger.exception("query [{0}] failed to execute. p_dbname {1}".format(p_query, p_dbname))
      return False, None, None
 
  def execute_insert_query(self, p_query, p_dbname):
    try:
      #logger.debug("query {0} dbname {1}".format(p_query, p_dbname))
      l_connection = PySQLPool.getNewConnection(username=self.db_user_name, password=self.db_user_password, host=self.db_server, db=p_dbname,  charset = "utf8")
      l_query = PySQLPool.getNewQuery(l_connection, True)
      l_retval = l_query.Query(p_query)
      return True, l_retval, l_query.lastInsertID
    except:
      #logger.exception("query [{0}] failed to execute. p_dbname {1}".format(p_query, p_dbname))
      return False, None, None
 
if __name__ == "__main__":
  #Run unit tests
  l_dbpool = DBPool()

  print "\n\n"
  l_res, l_numrows, l_rows = l_dbpool.execute_query("select * from tb_uvdeals", 'deals_api' )
  if(l_res): 
    print("Num of rows {0}".format(l_numrows))
    print("rows {0}".format(l_rows))
  else:
    print "failed to run query"
  print "\n\n"

  
  json_deals = JsonParser().convert_uvjson(l_rows)

  print type(json_deals)
 

