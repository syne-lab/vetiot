from ast import arg
import util
import json
import argparse
import time_space
class PostProcessing:
    expName: str
    
    expFilePath: str
    eventList: list[str] 
    eventCount: int

    expResultDirPath: str 

    def __init__(self, expName: str):
        self.expName = expName
        return
    
    def checkIfExpFileExists(self, expName: str)-> bool:
        filePath = util.getProjectRoot().joinpath('config').joinpath('exps').joinpath(expName+'.events')
        if util.doesFileExists(filePath.__str__()):
            self.expFilePath = filePath
            return True
        else:
            self.expFilePath = ''
            return False


    def readExpFile(self, expName: str) -> bool:
        if self.checkIfExpFileExists(expName) == False:
            print('No experiment named '+expName)
            return False
        with open(self.expFilePath, 'r') as eventFile:
            self.eventList = eventFile.readlines()
            self.eventCount = self.eventList.__len__()
        eventFile.close()
        return True
    
    def checkIfDebugDataResultExists(self, expName: str):
        expResultDir = util.getProjectRoot().joinpath('generated').joinpath(expName)
        filePath = expResultDir.joinpath('output.txt')
        if util.doesFileExists(filePath.__str__()) == False:
            print('Experiment result does not exist')
            return False
        lastEventIndex = self.eventCount -1
        eventResultDirName = 'event_'+str(lastEventIndex)
        filePath = util.getProjectRoot().joinpath('generated').joinpath(expName).joinpath(eventResultDirName).joinpath('S_Prime.json')
        # print(filePath)
        if util.doesFileExists(filePath):
            self.expResultDirPath = expResultDir.__str__()
            return True
        else:
            print('Experiment was not run with debug enabled.')
            return False

    def perEventSystemStateDiff(self, expName: str):
        differenceFileName = 'perEventDiff.json'
        diff = {}
        for i in range(self.eventCount):
            # print(self.eventList[i])
            key = self.eventList[i].strip()
            diffItemList = self.compareSystemStates(eventNo = i, expName = self.expName)
            diff[key] = diffItemList
        differenceFilePath = util.getProjectRoot().joinpath('generated').joinpath(expName).joinpath(differenceFileName)
        with open(differenceFilePath, 'w') as outfile:
            json.dump(diff, outfile, indent=4)
            outfile.flush()
            outfile.close()
        return

    def perEventItemTrace(self, expName:str, itemName: str):
        differenceFileName = itemName+'_trace.json'
        diff = {}
        for i in range(self.eventCount):
            # print(self.eventList[i])
            key = self.eventList[i].strip()
            diffItemList = self.traceItem(eventNo = i, expName = self.expName, itemName=itemName)
            diff[key] = diffItemList
        differenceFilePath = util.getProjectRoot().joinpath('generated').joinpath(expName).joinpath(differenceFileName)
        with open(differenceFilePath, 'w') as outfile:
            json.dump(diff, outfile, indent=4)
            outfile.flush()
            outfile.close()
        return
    
    def compareSystemStates(self, eventNo:int, expName:str) -> list[dict]:
        expResultDirectoryPath = util.getPath(self.expResultDirPath)
        eventName = 'event_'+str(eventNo)
        eventResultDirPath = expResultDirectoryPath.joinpath(eventName)
        
        S_Prime_path = eventResultDirPath.joinpath('S_Prime.json')        
        Oracle_S_Prime_path = eventResultDirPath.joinpath('Oracle_S_Prime.json')
        
        with open(S_Prime_path.__str__(), 'r') as S_Prime_file:
            S_Prime = json.load(S_Prime_file)
        with open(Oracle_S_Prime_path.__str__(),'r') as Oracle_S_Prime_file:
            Oracle_S_Prime = json.load(Oracle_S_Prime_file)
        diffItemList = []
        for item_Oracle,item_SPrime in zip(Oracle_S_Prime, S_Prime):
            if item_Oracle['name'] == item_SPrime['name'] and item_Oracle['state']!=item_SPrime['state']:
                item=dict()
                item['name'] = item_Oracle['name']
                item['State_With_Uninstrumented_Rules'] = item_Oracle['state']
                item['State_With_Instrumented_Rules'] = item_SPrime['state']
                diffItemList.append(item)
        return diffItemList

    def traceItem(self, eventNo: int, expName: str, itemName: str) -> dict:
        expResultDirectoryPath = util.getPath(self.expResultDirPath)
        eventName = 'event_'+str(eventNo)
        eventResultDirPath = expResultDirectoryPath.joinpath(eventName)
        
        S_Prime_path = eventResultDirPath.joinpath('S_Prime.json')        
        Oracle_S_Prime_path = eventResultDirPath.joinpath('Oracle_S_Prime.json')
        
        with open(S_Prime_path.__str__(), 'r') as S_Prime_file:
            S_Prime = json.load(S_Prime_file)
        with open(Oracle_S_Prime_path.__str__(),'r') as Oracle_S_Prime_file:
            Oracle_S_Prime = json.load(Oracle_S_Prime_file)
        item=dict()
        item['name'] = itemName
        ifFound = False
        for item_Oracle in Oracle_S_Prime:
            if item_Oracle['name'] == itemName:
                ifFound = True
                item['State_With_Uninstrumented_Rules'] = item_Oracle['state']
                break
        if not ifFound:
            item['name'] = 'item Not Found'
            return item
        for item_SPrime in S_Prime:
            if item_SPrime['name'] == itemName:
                item['State_With_Instrumented_Rules'] = item_SPrime['state']
                break
        return item

    def doSystemStateDiff(self):
        if not self.checkIfExpFileExists(self.expName):
            print('Experiment file does not exist')
            return
        if not self.readExpFile(self.expName):
            print('unable to read event file')
            return
        if not self.checkIfDebugDataResultExists(self.expName):
            return
        self.perEventSystemStateDiff(self.expName)
        return

    def doTrace(self, itemName: str):
        if not self.checkIfExpFileExists(self.expName):
            print('Experiment file does not exist')
            return
        if not self.readExpFile(self.expName):
            print('unable to read event file')
            return
        if not self.checkIfDebugDataResultExists(self.expName):
            return
        self.perEventItemTrace(self.expName, itemName)



def setup_args():
    arg_parser = argparse.ArgumentParser(description="PostProcessing of debug data - Create a diff file which will show the difference of system sates as each event is pushed.")
    arg_parser.add_argument('experimentName', help='Just give the name of the experiment file without extension.')
    arg_parser.add_argument('traceItem', nargs='?', help='Give the itemName you want to trace')
    args = arg_parser.parse_args()
    return args

def main():
    startTime = time_space.startCPUtime()
    time_space.startTraceMalloc()
    initMemory = time_space.traceMem()
    args = setup_args()
    postProcessor = PostProcessing(args.experimentName)
    postProcessor.doSystemStateDiff()
    if args.traceItem:
        postProcessor.doTrace(args.traceItem)
    time_space.endCPUtime(startTime)
    time_space.countRequiredMemory(initMemory)
    time_space.stopTraceMalloc()

if __name__ == "__main__":
    main()

