from ConfigParser import SafeConfigParser
import os.path
import codecs
import logging
import logging.config
from decorators import *


@singleton
class UVConfig(object):
  """ This class used for initilizing the configuration parameters for UCP application """
  def __init__(self):
    """ 
    Constructior for UVConfig. It initilizes the class member m_initialized to zero.
    if m_initialized is "0" then no configuration parameters are initialized from configuration file.
    This variable would be made it to "1" after initializing the configuration parameters 
    """
    self.m_initialized = 0

  def reload(self):
    self.m_initialized = 0
    self.init(self.conf_filename)

  def init(self, p_filename='ucp.conf'):
    """
    Description : Method to initialize the configuration parameters from configuration file
    Input       : 
      p_filename - Configuration file name along with file path
    Output      : none
    Algoritham  :
      1) Initialize the member variable conf_filename with input file name. 
      2) Validate the file name. It should not be null. And path and file should be valid. 
         If it is invalid through an error and raise the exception.
      3) Initialize the member variable parser with object SafeConfigParser.
      4) Open the file in read mode and parse the content of file.
      5) Initialize the member variable m_initialized with "1".
    """
    self.conf_filename = p_filename
    print p_filename
    try:
      assert (len(self.conf_filename) != 0 and os.path.isfile(self.conf_filename) ) , "config file {0} is not valid".format(self.conf_filename)
    except AssertionError:
      raise


    self.parser = SafeConfigParser()
    with codecs.open(self.conf_filename, 'r', encoding='utf-8') as file_des:
      self.parser.readfp(file_des)

    self.m_initialized = 1


  def get_config_value(self, p_section_name, p_key):
    """
    Description : Method to get the configuration parameter value
    Input       : 
      p_section_name - Configuration section name
      p_key          - Configuration parameter name
    Output      :
      If input configuration parameter present rerutn configuration value else none.
    Algoritham  :
      1) Verify wether the configuration parameters are initilized or not. If not raise an error.
      2) Verify wether the configuration section and key present or not. If present return the 
         configuration parameter value. else return none.
    """
    try:
      assert self.m_initialized == 1, "UVConfig class has not yet initialized with config file"
    except AssertionError:
      raise
        
    if self.parser.has_option(p_section_name, p_key):
      return self.parser.get(p_section_name, p_key)
    else:
      return None


if __name__ == "__main__":
  conf = UVConfig()
  conf.init("/root/ucp/ucp/conf/ucp.conf")
  
  
  print "Start testing"
  print conf.get_config_value("core","logfile_name")
  print conf.get_config_value("database","db_user_name")
  print conf.get_config_value("database","logfile_path")
  print conf.get_config_value("database","db_name.core")
  print conf.get_config_value("database", "db_user")
 
