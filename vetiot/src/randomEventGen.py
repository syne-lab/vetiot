import string
import random
from typing import Any
import requests
import util
import httpUtil
import pytomlpp as tomlParser
import argparse
import time_space

class RandomEventGenerator:

    testBed: list
    platformSupport: dict
    eventDir: str
    seedForEventGen: int
    def __init__(self, seed:int, testBed:Any, platformSupport:dict, eventDir:str) -> None:
        if util.doesFileExists(eventDir)==False:
            print("source directory of rule doesn't exist")
        else:
            self.eventDir = eventDir
            self.testBed = testBed
            self.platformSupport = platformSupport
            self.seedForEventGen = seed
            random.seed(self.seedForEventGen)
        return None

    def generateOneEvent(self) -> str:
        randomItem:dict = dict(random.choice(self.testBed))
        while randomItem['name'] == 'Reset':
            randomItem:dict = dict(random.choice(self.testBed))
        itemName = randomItem['name']
        itemType = randomItem['type']
        eventType = getEventType()
        supportedValueList = self.platformSupport[itemType][eventType]
        if len(supportedValueList) == 0:
            return 'not a valid event selection\n'
        itemValue = random.choice(supportedValueList)
        
        if itemValue == 'datetime':
            eItemValue = self.generateRandomDateTime()
        elif itemValue == 'hsb':
            eItemValue = self.generateRandomHSB()
        elif itemValue == 'point':
            eItemValue = self.generateRandomPoint()
        elif itemValue == 'decimal':
            eItemValue = random.uniform(0,400)
        elif itemValue == 'integer':
            eItemValue = random.randint(0,100)
        elif itemValue == 'string':
            eItemValue = self.generateRandomString()
        else:
            eItemValue = itemValue
        eventString = itemName+';'+eventType+';'+str(eItemValue) + '\n'
        return eventString
    
    def generateDelayEvent(self):
        itemType = 'delay'
        delayDuration = random.randint(0,60)
        return itemType+';'+str(delayDuration)+'\n'

    def generateRandomDateTime(self) -> str:
        year = random.randint(1000,9999)
        month = random.randint(1,12)
        date = random.randint(1,31)
        hour = random.randint(0,23)
        min = random.randint(0,59)
        sec = random.randint(0,59)
        dateString = str(year) + '-' + padZeroIfNeeded(month) + '-' + padZeroIfNeeded(date)
        timeString = padZeroIfNeeded(hour) + ':' +padZeroIfNeeded(min) + ':' + padZeroIfNeeded(sec)
        dateTimeString = '"' + dateString + 'T' + timeString + '"' 
        return dateTimeString

    def generateRandomHSB(self)-> str:
        h = random.randint(0,359)
        s = random.randint(0, 100)
        b = random.randint(0,100)
        hsbString = str(h) + ',' + str(s) + ',' + str(b)
        return hsbString

    def generateRandomPoint(self) -> str:
        lat = random.uniform(-90,90)
        long = random.uniform(-180, 180)
        latLongstr = str(lat)+','+str(long)
        return latLongstr

    def generateRandomString(self) -> str:
        length:int = random.randint(1,100)
        randomString = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=length))
        return randomString

    def createExperimentFile(self, expName: str, expNo: int, eventCount: int):
        fileName: str = expName + '_' + str(expNo) + '.events'
        eventFileName = self.eventDir +'/'+fileName
        print(eventFileName)
        with open(eventFileName, 'w') as f:        
            for i in range(eventCount):
                delayProbability = random.randint(1,100)
                if delayProbability < 3:
                    eventString = self.generateDelayEvent()
                else: 
                    eventString = self.generateOneEvent()
                f.write(eventString)
            f.flush()
            f.close()
        return

    def generateExperments(self, expName:str, expCount: int, eventCountCap: int):
        for i in range(1,expCount+1):
            actualEventCount = random.randint(1,eventCountCap)
            self.createExperimentFile(expName, i, actualEventCount)
        return

    

def padZeroIfNeeded(value: int)->str:
    s: str
    if value<10:
        s = '0' + str(value)
    else:
        s = str(value)
    return s

def getEventType()->str:
    tossResult = coinToss()
    if tossResult == 0:
        eventType = 'command'
    else:
        eventType = 'update'
    return eventType

def coinToss()->int:
    return random.randint(0,1)

def getTestBed(httpUtility: httpUtil.httpConnectionUtility):
    header = httpUtility.createDatalessHeader()
    baseUrl = httpUtility.createBaseItemUrl()
    params:dict = {'recurssive':'false', 'fields':'name,type'}
    response = requests.get(baseUrl,headers=header,params=params)
    if response.status_code == 200:
        # print('System state collected')
        S_json = response.json()
        # print(S_json)
        return list(S_json)
    else:
        return None

def setup_args():
    arg_parser = argparse.ArgumentParser(description="RandomEventGenerator - Generate random events based on testbed and put it in events folder")
    arg_parser.add_argument('seed',help='any acceptable integer, keep the integer same for same event sequence')
    arg_parser.add_argument('eventCount', choices=['5','10', '15'])
    arg_parser.add_argument('experimentCount', choices=['5', '10', '15', '25', '35', '50'])
    args = arg_parser.parse_args()
    print(args)
    return args

def main():
    startTime = time_space.startCPUtime()
    time_space.startTraceMalloc()
    initMemory = time_space.traceMem()
    args = setup_args()
    httpUtility = httpUtil.httpConnectionUtility()
    testBed = getTestBed(httpUtility)
    rootDir = util.getProjectRoot()
    paltformSetupFilePath = rootDir.joinpath('src').joinpath('platformSetup.toml')
    supportedEvents = tomlParser.load(paltformSetupFilePath.__str__())
    ohSupportedEvents = dict(supportedEvents['OHItems'])
    eventDir = rootDir.joinpath('config').joinpath('exps')
    seedForRandomGenerator = int(args.seed)
    eventGenerator = RandomEventGenerator(seedForRandomGenerator,testBed, ohSupportedEvents, eventDir.__str__())
    # print(eventGenerator.generateRandomDateTime())
    expCount = int(args.experimentCount)
    eventCountCap = int(args.eventCount)
    eventGenerator.generateExperments('randomExp',expCount, eventCountCap)
    time_space.endCPUtime(startTime)
    time_space.countRequiredMemory(initMemory)
    time_space.stopTraceMalloc()

if __name__ == "__main__":
    main()