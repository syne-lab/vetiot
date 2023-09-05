import string
import time
import requests
import util
import httpUtil
import json
import re
import ruleInstaller
from pathlib import Path
# import sshConnectionUtil

REGEX_DICT = {
    'datetime':re.compile(r'(?P<beginquote>")(?P<dateTimeString>.*?)(?P<endquote>")'),
    'hsb': re.compile(r'\s*(?P<h>[0-9]+)\s*,\s*(?P<s>[0-9]+)\s*,\s*(?P<b>[0-9]+)\s*', re.IGNORECASE),
    'point': re.compile(r'\s*(?P<lat>(-)?[0-9]+\.[0-9]+)\s*,\s*(?P<long>(-)?[0-9]+\.[0-9]+)\s*', re.IGNORECASE),
    'decimal': re.compile(r'\s*(?P<decimalValue>[0-9]+\.[0-9]+)\s*',re.IGNORECASE),
    'integer': re.compile(r'\s*(?P<intValue>[0-9]+)\s*', re.IGNORECASE)
}
delayTotalTime = 0
def parseValue(value):
    # print("start matching")
    for key, rx in REGEX_DICT.items():
        match = rx.match(value)
        # print(match)
        if match:
            return key, match
    return None, None

def isDeviceInstalled(testbed: list, itemName:string):
    for item in testbed:
        if item['name'] == itemName:
            return True, item['type']
    return None, None

def isValidEvent(supportedEvents:dict, itemType:string, eventType:string, valueType:string)->bool:
    listOfValidValues = supportedEvents[itemType][eventType]
    if valueType in listOfValidValues:
        return True
    else:
        return False

def checkValueRange(valueType:string,match)->bool:
    if valueType == 'point':
        lat = match.group('lat')
        long = match.group('long')
        print('lat '+ lat + 'long' + long)
        return True
    elif valueType == 'decimal':
        decValue = match.group('decimalValue')
        print('decimal value '+decValue)
        d = float(decValue)
        return True
        # if d>=0 and d<=100:
        #     return True
        # else:
        #     return False
    elif valueType == 'integer':
        intVal = match.group('intValue')
        print('integer value '+intVal)
        i = int(intVal)
        if i>=0 and i<=100:
            return True
        else:
            return False
    elif valueType == 'hsb':
        h = match.group('h')
        s = match.group('s')
        b = match.group('b')
        print('HSB value H:'+h+' S:'+s+' B:'+b)
        if int(h) in range(360) and int(s) in range(101) and int(b) in range(101):
            return True
        else:
            return False
    elif valueType == 'datetime':
        return True

# def getItemStateRestAPI(itemName:string):
#     header = httpUtil.createDatalessHeader()
#     baseUrl = httpUtil.createBaseItemUrl()
#     itemUrl = baseUrl+'/'+itemName+'/state'
#     respose = requests.get(itemUrl,headers=header)
#     if respose.ok:
#         return respose.text
#     else:
#         print('http error while getting previous itemstate')
#         return None

def createDelay(duration: int):
    time.sleep(duration)
    if duration<=10:
        global delayTotalTime
        delayTotalTime = delayTotalTime+duration
    return

def compareSystemStates(expResultDir:Path, profiler):
    if profiler != None:
        profiler.startProfiling('comparator')
    # dirPath = util.getProjectRoot().joinpath('generated').joinpath(expName)
    dirPath = expResultDir
    if util.doesFileExists(dirPath.__str__()) == False:
        return None, None
    S_path = dirPath.joinpath('S.json')
    if util.doesFileExists(S_path.__str__()) == False:
        return None, None
    Oracle_path = dirPath.joinpath('Oracle.json')
    if util.doesFileExists(Oracle_path.__str__()) == False:
        return None, None
    S_Prime_path = dirPath.joinpath('S_prime.json')
    if util.doesFileExists(S_Prime_path.__str__()) == False:
        return None, None
    with open(S_path.__str__(), 'r') as S_file:
        S = json.load(S_file)
    with open(Oracle_path.__str__(),'r') as Oracle_file:
        Oracle = json.load(Oracle_file)
    with open(S_Prime_path.__str__(),'r') as SPrime_file:
        S_Prime = json.load(SPrime_file)

    outputFilePath = dirPath.joinpath('output.txt')
    violationCount = 0
    indeterMinateCount = 0
    with open(outputFilePath.__str__(),'w') as outputFile:
        for item_Oracle,item_SPrime in zip(Oracle, S_Prime):
            if item_Oracle['name'] == item_SPrime['name'] and item_Oracle['state']!=item_SPrime['state']:
                print('mismatch in oracle and S_prime found')
                for item_S in S:
                    if item_S['name'] == item_SPrime['name']:
                        if item_S['state'] == item_SPrime['state']:
                            violationCount = violationCount + 1
                            content = 'Manual inspection not necessary. Policy blocked ' + item_S['name'] + ' to change from ' + item_S['state'] + ' to ' + item_Oracle['state'] 
                            print(content)
                            outputFile.write(content + '\n')
                        else:
                            indeterMinateCount = indeterMinateCount + 1
                            content = 'manual inspection necessary for item ' + item_S['name']
                            print(content)
                            outputFile.write(content + '\n')
                        break
        outputFile.write('PolicyViolationCount: '+str(violationCount)+ ' indeterminate case: '+str(indeterMinateCount))

    S_file.close()
    Oracle_file.close()
    SPrime_file.close()    
    if profiler is not None:
        profiler.endProfiling('comparator')
    return violationCount,indeterMinateCount

def printJsonToFile(jsonObject, fileName:str, fileDir:Path):
    if util.doesFileExists(fileDir)==False or util.isDirectory(fileDir)==False:
        print('directory setup is not done')
        return
    filePath = fileDir.joinpath(fileName)
    with open(filePath, 'w') as outfile:
        json.dump(jsonObject, outfile,indent=4)
        outfile.flush()
        outfile.close()
    return

# def createExpDirectory():
#     root_dir = util.PROJECT_ROOT
#     eventDirPath = root_dir.__str__()+'/config/exps/'
#     expDir = root_dir.__str__()+'/generated'
#     for path in util.getPath(eventDirPath).glob('*.events'):
#         fileName = path.name.split(sep='.')[0]
        
#         expDirName = expDir + '/' + fileName
#         print('creating directory'+expDirName)
#         util.createDir(expDirName)
#     # installConfigRules()
#     return


# def copyRuleFiles():
#     projectRoot = util.getProjectRoot()
#     thingsFileDir = projectRoot.joinpath('config').joinpath('rules')
#     thingsFiles = util.listDirectory(thingsFileDir, '*.rules')
#     for file in thingsFiles:
#         filename = file.name
#         destinationFile = '/etc/openhab/rules/'+filename
#         if 'proxy' in filename:
#             sshConnectionUtil.sendFile('proxy',file.__str__(), destinationFile)
#         else:
#             sshConnectionUtil.sendFile('au',file.__str__(), destinationFile)

class EventSimulation:
    ohSupportedEvents: dict
    httpUtility: httpUtil.httpConnectionUtility
    testbed_oh: list
    testbed_vt: list
    isDebug: bool
    targetDefense: str
    activeHost: str
    hostTitles: list

    def __init__(self, defense, evalDirPath, activeHost, OH_Supported_Events, debug, evalConfig=0, profiler=None) -> None:
        self.targetDefense = defense
        self.activeHost = activeHost
        self.evalDirPath = evalDirPath
        self.ohSupportedEvents = OH_Supported_Events
        self.httpUtility = httpUtil.httpConnectionUtility(evalDirPath, self.activeHost)
        self.testbed_oh=util.getTestBed(self.httpUtility)
        self.profiler = profiler
        # print(self.testbed_oh)
        savedTestbedPath = evalDirPath.joinpath('testbed.json')
        with open(savedTestbedPath,'r') as fp:
            self.testbed_vt = json.load(fp)
            fp.close() 
        # interactiveSimulation(testBed,ohSupportedEvents)
        self.isDebug = debug
        self.fileSimulation(evalConfig)

    def fileSimulation(self, evalConfig):
        print('start simulation from files')
        root_dir = util.PROJECT_ROOT
        if evalConfig!=0:
            expDir = self.evalDirPath.joinpath('TestSuite-'+str(evalConfig))
            eventDirPath = root_dir.joinpath('config').joinpath('exps').joinpath('TestSuite-'+str(evalConfig))
            if util.createDir(expDir) == False:
                print('evaluation directory creation failed.')
                return
        else:
            expDir = self.evalDirPath
            eventDirPath = root_dir.joinpath('config').joinpath('exps')
        # filePaths = util.getPath(eventDirPath).glob('*.events')
        # print(filePaths)
        outputFileName = 'result.json'
        #with open(outputFilePath.__str__(),'w') as outputFile:
        eventFiles = util.listDirectory(eventDirPath, '*.events')
        numberOfExperiments = eventFiles.__len__()
        # numberOfExperiments = length - 1 #skipping readme.txt file
        resultDict = {}
        progressCount = 0
        for path in eventFiles:
            # path = util.getPath(eventFilePath)
            fileNameSplit = path.name.split(sep='.')
            fileExt = fileNameSplit[1]
            if fileExt!='events':
                print('not an event file')
                continue
            fileName = fileNameSplit[0]
            expDirName = expDir.joinpath(fileName)
            expNo = fileName.split(sep='_')[1]
            print('creating directory'+ expDirName.__str__())
            util.createDir(expDirName)
            print('Setting up default environment for '+fileName)
            self.createDefaultEnvironment(expNo)
            self.enableVanilaTestEnviroment()
            self.runExperiment(path, expDir, True, self.isDebug) #generating Oracle
            print('Experiment:: '+ fileName + ' for oracleGeneration ended')
            self.createDefaultEnvironment(expNo)
            self.enableProtectiveTestEnviroment()
            violationCount, inderminateCount = self.runExperiment(path, expDir, False, self.isDebug) #generating S_prime
            print('Experiment:: '+fileName+' for S_Prime generation ended')
            if violationCount!=None and inderminateCount!=None:
                if violationCount!=0 or inderminateCount!=0:
                    mal_case = {}
                    mal_case['policyViolation'] = violationCount
                    mal_case['indeterminate'] = inderminateCount
                    resultDict[fileName] = mal_case
            progressCount = progressCount +1
            print('Progress: {}/{}'.format(progressCount,numberOfExperiments))
        printJsonToFile(resultDict, outputFileName, expDir)
        return
    
    def createDefaultEnvironment(self, expNo):
        self.installConfigRules()
        createDelay(10)
        event = 'Reset;command;OFF'
        self.oneInteraction(event)
        createDelay(3)
        event = 'Reset;command;ON'
        self.oneInteraction(event)
        createDelay(6)
        event = 'Reset;command;OFF'
        self.oneInteraction(event)
        createDelay(3)
        self.unInstallConfigRules()
        self.additionalSystemReset(expNo)
        return
    
    # def createDefaultEnvironment(self, expNo):
    #     for item in self.testbed_oh:
    #         itemName = item['name']
    #         if itemName in self.testbed_vt:
    #             item = self.testbed_vt[itemName]
    #             defaultState = item['DefaultState'].__str__()
    #             eventType = 'update'
    #             self.sendEventRestAPI(itemName,eventType,defaultState)
    #     self.additionalSystemReset(expNo)
    #     return
    
    def oneInteraction(self, event: string):
        lineElement = event.split(';')
        if lineElement.__len__() < 2:
            print('ill formated event')
            return
        
        if lineElement.__len__() == 2:
            specialEventName = lineElement[0].strip()
            specialEventParam = lineElement[1].strip()
            if specialEventName.lower() == 'delay':
                if specialEventParam.isnumeric():
                    delayTime = specialEventParam
                    print('delay;'+str(delayTime))
                    createDelay(int(delayTime))
            return
        
        itemName = lineElement[0].strip()
        eventType = lineElement[1].strip()
        value = lineElement[2].strip()
        
        found, itemType = isDeviceInstalled(self.testbed_oh, itemName)
        
        if found == None:
            print('Device is not in the testbed')
            return
        
        if eventType!='command' and eventType!='update':
            print("Invalid event type. It has to be command or update")
            return 
        
        valueType, match = parseValue(value)
        if valueType == None:
            if value.isupper():
                valueType = value
            else:
                valueType = 'string'
        
        isValid = isValidEvent(self.ohSupportedEvents, itemType, eventType.lower(), valueType)
        isValidRange=checkValueRange(valueType,match)
        if isValid==False:
            print('Not a valid item value')
            return
        if isValidRange==False:
            print('Item value not in range')
            return
        
        if valueType == 'datetime':
            value = match.group('dateTimeString')
            print('datetime value is: '+value)
        print(itemName+';'+eventType+';'+value)
        response=self.sendEventRestAPI(itemName,eventType,value)
        if response.ok==False:
            print('http error while sending the event')
            print(response.text)
            print(response.status_code)
            return
        return
    
    def runExperiment(self, filePath:Path, outputPath:Path, isOracleGeneration:bool, isDebug: bool):
        # path = util.getPath(filePath)
        expName = filePath.name.split('.')[0]
        expResultDir = outputPath.joinpath(expName)
        if isOracleGeneration == False:
            createDelay(1)
            S_json = self.getSystemState()
            if(S_json == None):
                print('System state collection failed')
            printJsonToFile(S_json,'S.json',expResultDir)
        
        with open(filePath, 'r') as f:
            events=f.readlines()
            index = 0
            for event in events:
                if isDebug:
                    self.collectDebugData(expResultDir, index, isOracleGeneration, False)
                self.oneInteraction(event)
                createDelay(5)
                if isDebug:
                    self.collectDebugData(expResultDir, index, isOracleGeneration, True)
                index = index + 1

        if isOracleGeneration == False:
            outputFileName = 'S_prime.json'
        else:
            outputFileName = 'Oracle.json'
        createDelay(1)
        S_prime_json = self.getSystemState()
        if(S_prime_json == None):
            print('System state collection failed')
            return None, None
        printJsonToFile(S_prime_json,outputFileName,expResultDir)
        if isOracleGeneration == False:
            return compareSystemStates(expResultDir, self.profiler)
        else:
            return None, None
        
    def sendEventRestAPI(self, itemName:string, eventType:string, itemValue:string):
        header = self.httpUtility.createHeader('text/plain')
        baseUrl = self.httpUtility.createBaseItemUrl()
        itemUrl = baseUrl+'/'+itemName
        data = itemValue.strip()
        if eventType == 'command':
            response =  requests.post(itemUrl,headers=header,data=data)
            return response
        elif eventType == 'update':
            response = requests.put(itemUrl+'/state',headers=header,data=data)
            return response
        
    def getSystemState(self):
        header = self.httpUtility.createDatalessHeader()
        baseUrl = self.httpUtility.createBaseItemUrl()
        params:dict = {'recurssive':'false', 'fields':'name,state'}
        response = requests.get(baseUrl,headers=header,params=params)
        if response.status_code == 200:
            # print('System state collected')
            S_json = response.json()
            # print(S_json)
            return S_json
        else:
            return None
        
    def collectDebugData(self, expResultDir: Path, eventNo: int, isOracle:bool, isS_Prime:bool):
        eventResultDirName = 'event' + '_' + str(eventNo)
        evtResultDir = expResultDir.joinpath(eventResultDirName)
        dirExists = util.doesFileExists(evtResultDir)
        if dirExists == False:
            isSuccess = util.createDir(evtResultDir)
        systemState = self.getSystemState()
        if isOracle == True and isS_Prime == False:
            fileName = 'Oracle_S.json'
        elif isOracle == True and isS_Prime == True:
            fileName = 'Oracle_S_Prime.json'
        elif isOracle == False and isS_Prime == False:
            fileName = 'S.json'
        elif isOracle == False and isS_Prime == True:
            fileName = 'S_Prime.json'
        
        if dirExists == True or isSuccess == True:
            printJsonToFile(systemState, fileName, evtResultDir)
        return
    
    

    def interactiveSimulation(self):
        S_json = self.getSystemState()
        
        if(S_json == None):
            print('System state collection failed')
        
        event = input('<ItemName>,<Command/Update>,<value>')
        while(event != 'quit'):
            self.oneInteraction(self.testbed_oh, self.ohSupportedEvents, event)
            event = input('<ItemName>,<Command/Update>,<value>')
        S_prime_json = self.getSystemState()
        # compareSystemStates(S_json,S_prime_json)
        return
    
    def enableVanilaTestEnviroment(self):
        self.installRules()
        util.createDelay(10)
        #Additional 
        # util.createDelay(5)
        # if self.targetDefense == 'maverick':
        #     connection = sshConnectionUtil.getConnection(self.activeHost)
        #     connection.run('sudo systemctl stop mosquitto.service')
        #     # connection.run('sudo systemctl disable mosquitto.service')
        #     connection.run('sudo systemctl stop maverick.service')
        #     # connection.run('sudo systemctl disable maverick.service')
        #     # connection.run('sudo systemctl enable mosquitto.service')
        #     connection.run('sudo systemctl start mosquitto.service')
        #     connection.close()
        # if self.targetDefense == 'maverick':
        #     util.createDelay(15)
        # else:
        #     util.createDelay(5)

    def enableProtectiveTestEnviroment(self):
        self.installSecureRules()
        util.createDelay(10)
        # if self.targetDefense == 'maverick':
        #     connection = sshConnectionUtil.getConnection(self.activeHost)
        #     connection.run('sudo systemctl stop mosquitto.service')
        #     # connection.run('sudo systemctl disable mosquitto.service')
        #     connection.run('sudo systemctl stop maverick.service')
        #     # connection.run('sudo systemctl disable maverick.service')
        #     # connection.run('sudo systemctl enable maverick.service')
        #     connection.run('sudo systemctl start maverick.service')
        #     connection.close()
        #     util.createDelay(16)
        # else:
        #     switchRules(self.activeHost)
        #     util.createDelay(5)
    # def stopAllService()
    def additionalSystemReset(self, expNo):
        self.resetTargetDefense(expNo)

    def resetTargetDefense(self, expNo):
        installedDeviceFilePath = self.evalDirPath.joinpath('defense-info.json')
        with open(installedDeviceFilePath, 'r') as f:
            defenseInfo = json.load(f)
            name = defenseInfo['name']
            if name=='iotguard':
                self.sendResetRequestToIoTGuardServer(defenseInfo['connectionInfo'], expNo)
        return

    def sendResetRequestToIoTGuardServer(self, connInfo, expNo):
        protocol = connInfo['protocol']
        ipAddress = connInfo['ip-address']
        port = connInfo['port']
        url = protocol+'://'+ipAddress+':'+str(port)

        header={
            'accept': '*/*',
            'Content-Type': 'application/json'
        }

        data={}
        data["reset"] = "true"
        data['exp-no'] = expNo
        response = requests.post(url, headers=header, json=data)
        if response.ok:
            print("INFO: Reseting IoTGuard server successfull")
        else:
            print("ERROR: Error in reseting IoTGuard server")

    def installConfigRules(self):
        print('installing config rules')
        ohConfigDir = self.httpUtility.getOhDirectory()
        ohRuleDir = util.PROJECT_ROOT.joinpath(ohConfigDir).joinpath('rules')
        rulesDir = util.PROJECT_ROOT.joinpath('config').joinpath('config_rules')
        installer = ruleInstaller.RuleInstaller(self.activeHost, rulesDir, ohRuleDir)
        installer.unInstallRules()
        util.createDelay(3)
        installer.installRules()
        return
    
    def unInstallConfigRules(self):
        ohConfigDir = self.httpUtility.getOhDirectory()
        ohRuleDir = util.PROJECT_ROOT.joinpath(ohConfigDir).joinpath('rules')
        rulesDir = util.PROJECT_ROOT.joinpath('config').joinpath('config_rules')
        installer = ruleInstaller.RuleInstaller(self.activeHost, rulesDir, ohRuleDir)
        installer.unInstallRules()
        util.createDelay(3)
        print('uninstalling config rules')
        return

    def installRules(self):
        print('installing uninstrumented Rules')
        ohConfigDir = self.httpUtility.getOhDirectory()
        ohRuleDir = util.PROJECT_ROOT.joinpath(ohConfigDir).joinpath('rules')
        rulesDir = util.PROJECT_ROOT.joinpath('config').joinpath('rules')
        installer = ruleInstaller.RuleInstaller(self.activeHost,rulesDir,ohRuleDir)
        installer.unInstallRules()
        util.createDelay(3)
        installer.installRules()
        return

    def installSecureRules(self):
        print('switching rules to instrumented rules')
        ohConfigDir = self.httpUtility.getOhDirectory()
        ohRuleDir = util.PROJECT_ROOT.joinpath(ohConfigDir).joinpath('rules')
        inst_rulesDir = util.PROJECT_ROOT.joinpath('config').joinpath('inst_rules')
        installer = ruleInstaller.RuleInstaller(self.activeHost, inst_rulesDir, ohRuleDir)
        installer.unInstallRules()
        util.createDelay(3)
        installer.installRules()
        return
# Redauntant code for individual module testing
# def main():
#     time_space.startTraceMalloc()
#     startTime = time_space.startCPUtime()
#     initMemory = time_space.traceMem()
#     args = setup_args()
#     rootDir = util.PROJECT_ROOT
#     print('project root directory'+rootDir.__str__())
#     supportedEvents = tomlParser.load(rootDir.__str__()+'/source/platformSetup.toml')
#     ohSupportedEvents = dict(supportedEvents['OHItems'])
#     print('----- Supported Items and Commands loaded-----')
#     # print(ohSupportedEvents)
#     installedDeviceFilePath = rootDir.__str__() + '/generated/testbed.json'
#     with open(installedDeviceFilePath, 'r') as f:
#         installedItems = json.load(f)
    
#     configFilePath = rootDir.joinpath('generated').joinpath('rest-api-config.json')
#     configFileName = configFilePath.__str__()
#     with open(configFileName, 'r') as configFile:
#         restAPIconf = json.load(configFile)

#     httpUtil.setConnectionParameters(dict(restAPIconf))
    
#     print('----- Installed Items ar loaded-----')
#     testBed=dict(installedItems)
#     # print(testBed)

#     # interactiveSimulation(testBed,ohSupportedEvents)
#     isDebug = False
#     if args.debug:
#         isDebug = True
#     fileSimulation(testBed,ohSupportedEvents, isDebug)
#     print('total time in delay {}'.format(delayTotalTime))
#     time_space.endCPUtime(startTime)
#     time_space.countRequiredMemory(initMemory)
#     time_space.stopTraceMalloc()
#     return

# def setup_args():
#     arg_parser = argparse.ArgumentParser(description="EventSimulation - Send events from exps directory and collect change in the system state.")
#     arg_parser.add_argument('debug', nargs='?',help='Use -D flag for Debug mode. Debug mode will create output files for each event for further analysis.')
#     args = arg_parser.parse_args()
#     return args

# if __name__ == "__main__":
#     main()
