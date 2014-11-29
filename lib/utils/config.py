import ConfigParser
from sys import *
import os, os.path



class Config:
    """
        Main config classe for the application
    """
    configFile = None
    configParser = None
    filePath = "./config.ini"
	forceProxyOff = False

    def __init__(self,loggerInput):
        self.loggerConfig = loggerInput
        self.initializeConfigFile()

    def initializeConfigFile(self):
        """
            Try to open configFile or create a new one if necessary
        """
        self.configParser = ConfigParser.ConfigParser(allow_no_value = True)

        #If file exists
        if os.path.exists(self.filePath):
            print self.loggerConfig.getTimedHeader() + "config::initializeConfigFile::. [INFO] ConfigFile detected in main directory"
            configFile = self.configParser.read(self.filePath)
        else :
            print self.loggerConfig.getTimedHeader() + "config::initializeConfigFile::. [INFO] ConfigFile is not present, generating it"
            self.rewriteNewConfigFile()

    def rewriteNewConfigFile(self):
        """
            Write a new config File on demand
        """
        cfgFile = open(self.filePath,'w')

        self.configParser.add_section('network')
        self.configParser.set('network','#useproxy(1) or not (0)')
        self.configParser.set('network','useProxy', 0)
        self.configParser.set('network','#The hostname of your proxy or the IP @example - proxy.enib.fr')
        self.configParser.set('network','hostname', "ProxyHostnameHere")
        self.configParser.set('network','#The port where your proxy listen @example - 3128')
        self.configParser.set('network','port', "ProxyPorthere")
        self.configParser.set('network','#Your username for authentification with the proxy @example - krisscut')
        self.configParser.set('network','username', "YourUsernameHere")
        self.configParser.set('network','#Your password @example -  doyoureallyhopethatiwillgiveyoumypassword')
        self.configParser.set('network','password', "Yourpassword here")
        self.configParser.write(cfgFile)
        cfgFile.close()


    def ConfigSectionMap(self,section):
        """
            Name = ConfigSectionMap("SectionOne")['name']
            Age = ConfigSectionMap("SectionOne")['age']
        """
        dict1 = {}
        options = self.configParser.options(section)
        for option in options:
            try:
                dict1[option] = self.configParser.get(section, option)
                if dict1[option] == -1:
                    DebugPrint("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1



if __name__ == "__main__":

  if argv[1] == "-h":
    print "Usage : \n -o : Overwrite configFile OR -r readConfigFile  \n"
    exit(0)

  # get the maze size from program arguments
  command = argv[1]
  config = Config()
  config.rewriteNewConfigFile();


  # if ( argv[5] == 'T'):
  #   main_function(rows, cols, False,sizeCell ,sizeWall )
  # else :
  #   main_function(rows, cols, True, sizeCell ,sizeWall)