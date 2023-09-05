
import string
import util
import json

apiToken: string
ipAddress: string
ohInstallationDir: string
port: int  
protocol: string = 'http'
mandatory_keys = {'Name', 'Label'}

def setConnectionParameters(connectionInfo):
    global apiToken
    apiToken = connectionInfo['api-token']
    global ipAddress
    ipAddress = connectionInfo['ip-address']
    global port
    port = connectionInfo['port']
    global ohInstallationDir
    ohInstallationDir = connectionInfo['oh-installation-dir']
    return

def createHeader(contentType):
    header={
        'accept': '*/*',
        'Content-Type': contentType,
        'Authorization': 'Bearer ' + apiToken
    }
    return header

def createDatalessHeader():
    header={
        'accept': '*/*',
        'Authorization': 'Bearer ' + apiToken
    }
    return header

def createBaseItemUrl():
    url = protocol+'://'+ipAddress+':'+str(port)+'/rest/'+'items'
    return url

def getOhDirectory():
    return ohInstallationDir


class httpConnectionUtility:
    apiToken: string
    ipAddress: string
    ohConfigDir: string
    port: int  
    protocol: string = 'http'
    mandatory_keys = {'Name', 'Label'}

    def __init__(self, evalDirPath, hosttitle):
        rootDir = util.getProjectRoot()
        configFilePath = evalDirPath.joinpath(hosttitle+'-rest-api-config.json')
        configFileName = configFilePath.__str__()
        if util.doesFileExists(configFilePath) == False:
            print('Config file is found, try running toml_parser.py first')
            return None
        with open(configFileName, 'r') as f:
            data = json.load(f)
        self.apiToken = data['api-token']
        self.ipAddress = data['ip-address']
        self.port = data['port']
        self.ohConfigDir = data['oh-config-dir']
        return

    def createHeader(self,contentType):
        header={
            'accept': '*/*',
            'Content-Type': contentType,
            'Authorization': 'Bearer ' + self.apiToken
        }
        return header

    def createDatalessHeader(self):
        header={
            'accept': '*/*',
            'Authorization': 'Bearer ' + self.apiToken
        }
        return header

    def createBaseItemUrl(self):
        url = self.protocol+'://'+self.ipAddress+':'+str(self.port)+'/rest/'+'items'
        return url

    def getOhDirectory(self):
        return self.ohConfigDir