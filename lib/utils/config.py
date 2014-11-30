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


        mode = 0;
        #If file exists
        if os.path.exists(self.filePath):
            configFile = self.configParser.read(self.filePath)
        else :
            
            self.rewriteNewConfigFile()
            mode = 1;

        #set logging parameters
        self.loggerConfig.setVariableFromConfig(self.ConfigSectionMap("logs")['logmode'],self.ConfigSectionMap("logs")['pathtofile'])
        if mode == 0 : self.loggerConfig.logIt (fromModule = "config - initializeConfigFile" , tag = "INFO", content = "ConfigFile detected in main directory" )
        else : self.loggerConfig.logIt (fromModule = "config - initializeConfigFile" , tag = "WARNING", content = "ConfigFile is not present, generating it..." )

    def rewriteNewConfigFile(self):
        """
            Write a new config File on demand
        """
        cfgFile = open(self.filePath,'w')

        self.configParser.add_section('network')
        self.configParser.set('network','#useproxy(1) or not (0)')
        self.configParser.set('network','useproxy', 0)
        self.configParser.set('network','#The hostname of your proxy or the IP @example - proxy.enib.fr')
        self.configParser.set('network','hostname', "ProxyHostnameHere")
        self.configParser.set('network','#The port where your proxy listen @example - 3128')
        self.configParser.set('network','port', "ProxyPorthere")
        self.configParser.set('network','#Your username for authentification with the proxy @example - krisscut')
        self.configParser.set('network','username', "YourUsernameHere")
        self.configParser.set('network','#Your password @example -  doyoureallyhopethatiwillgiveyoumypassword')
        self.configParser.set('network','password', "Yourpassword here")

        self.configParser.add_section('logs')
        self.configParser.set('logs','#logmode : 3 = Console + logs, 2 = log only, 1 = console only, 0 = no logs')
        self.configParser.set('logs','logmode', 3)
        self.configParser.set('logs','#pathtoFile is the path from the main directory for your logs, all directory need to exist. default path is datas/logs/')
        self.configParser.set('logs','pathtoFile' ,'datas/logs/')

        self.configParser.write(cfgFile)
        cfgFile.close()

        configFile = self.configParser.read(self.filePath)

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