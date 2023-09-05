import psutil, os, tracemalloc, inspect, time
import json
import util
from pathlib import Path

dataFileName = util.getProjectRoot().__str__() + '/generated/time-space-usage.json'

def whoCalledParent():
    stack = inspect.stack()[2]
    completeFileName = stack.filename
    fileName = util.getPath(completeFileName).name
    functionName = stack.function
    return fileName, functionName

def saveData(fileName, functionName, key, value):
    global dataFileName
    node = {}
    node[key] = value
    if not util.doesFileExists(dataFileName):
        data = {}
        data[fileName] = {}
        data[fileName][functionName] = {}
        data[fileName][functionName][key] = value
        fp = open(dataFileName, 'w')
        json.dump(data,fp,indent=4)
        fp.close()
        return
    else:
        fp = open(dataFileName, 'r')
        previousData = json.load(fp)
        fp.close()
        if fileName not in previousData:
            previousData[fileName] = {}
            previousData[fileName][functionName] = {}
            previousData[fileName][functionName][key] = value
        
        elif functionName not in previousData[fileName]:
            previousData[fileName][functionName] = {}
            previousData[fileName][functionName][key] = value 
        else:
            if key in previousData[fileName][functionName]:
                previousValue = previousData[fileName][functionName][key]
                if key == 'time':
                    cumulitiveValue = previousValue + value
                else:
                    cumulitiveValue = max(float(previousValue), float(value))
            else:
                cumulitiveValue = value
            previousData[fileName][functionName][key] = cumulitiveValue 
        fp = open(dataFileName, 'w')
        json.dump(previousData,fp, indent=4)
        fp.close()
        return

def endCPUtime(startTime):
    procCPUtime = psutil.Process(os.getpid()).cpu_times()
    totalTime = procCPUtime.user + procCPUtime.system
    # totalTime = time.time()
    elapsedTime = totalTime - startTime
    fileName, functionName = whoCalledParent()
    saveData(fileName, functionName, 'time', elapsedTime)
    print('elapsed-time by function {} is {} seconds'.format(functionName, elapsedTime))

def startTraceMalloc():
    tracemalloc.start()

def stopTraceMalloc():
    tracemalloc.stop()

def startCPUtime():
    procCPUtime = psutil.Process(os.getpid()).cpu_times()
    totalTime = procCPUtime.user + procCPUtime.system
    return totalTime

def traceMem():
    currmem, peakMem = tracemalloc.get_traced_memory()
    return peakMem

def countRequiredMemory(initMem):
    currMem, peakMem = tracemalloc.get_traced_memory()
    increasedMemory = peakMem - initMem
    memoryIncrease = increasedMemory >> 10 #Memory in Kbytes
    peakMem = peakMem >> 10 #Memory in Kbytes
    fileName, functionName = whoCalledParent()
    saveData(fileName, functionName, 'peakMem', peakMem)
    print('required memory by function: {}, PeakMem increased {} kB, peak memory usage {} kB'.format(functionName, memoryIncrease, peakMem))

class Profiler:
    data:dict

    def __init__(self) -> None:
        self.data = {}
        pass

    def startProfiling(self,componentName):
        self.data[componentName]={}
        currentAbsoluteTime = time.time()
        self.data[componentName]['abs_time'] = currentAbsoluteTime

        cuurentCPUtime = self.getCPUtime()
        self.data[componentName]['cpu_time'] = cuurentCPUtime
        
        tracemalloc.start()
        currmem, peakMem = tracemalloc.get_traced_memory()
        self.data[componentName]['peak_mem'] = peakMem

        pass

    def endProfiling(self, componentName):
        previousAbsTime = self.data[componentName]['abs_time']
        currentAbsTime = time.time()
        self.data[componentName]['abs_time'] = currentAbsTime - previousAbsTime

        previousCPUtime = self.data[componentName]['cpu_time']
        currentCPUTime = self.getCPUtime()
        self.data[componentName]['cpu_time'] = currentCPUTime-previousCPUtime

        previousPeakMem = self.data[componentName]['peak_mem']
        currmem, peakMem = tracemalloc.get_traced_memory()
        
        if peakMem > previousPeakMem:
            peakMem = peakMem
        else:
            peakMem = previousPeakMem

        self.data[componentName]['peak_mem'] = peakMem
        tracemalloc.stop()
        pass

    def getCPUtime(self):
        procCPUtime = psutil.Process(os.getpid()).cpu_times()
        cuurentCPUtime = procCPUtime.user + procCPUtime.system
        return cuurentCPUtime

    def saveData(self, storePath, fileName):
        if util.doesFileExists(storePath.__str__()) == False:
            print('Output Directory Does not exist. printing in console')
            print(self.data)
            return
        
        outputFile = storePath.joinpath(fileName)
        with open(outputFile, 'w') as fp:
            json.dump(self.data, fp=fp, indent=4)
        pass
