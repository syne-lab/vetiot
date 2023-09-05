import argparse
import util
import clean
import toml_parser
# import fileBasedVtGen
import randomEventGen
import httpUtil
import requests
import pytomlpp as tomlparser
import restApiBasedVTgen
import eventSimulation
import time_space
import json

def setup_args():
    arg_parser = argparse.ArgumentParser(description="VetIoT - Evaluate IoT defenses")
    arg_parser.add_argument('testbedConfigStyle', help='choose how to you want to configure your testbed', choices=['file', 'rest'])
    arg_parser.add_argument('testCaseGenerationType', help='choose A to generate testcases automatically or M to use your own testcases', choices=['A', 'M'])
    arg_parser.add_argument('testCaseCount', help="For stress testing or differential testing you can specify test case count or you can put zero.")
    arg_parser.add_argument('experimentName', help="Provide the name of the config which is stored in the test-configs directory")
    args = arg_parser.parse_args()
    print(args)
    return args

def getTestBed(httpUtility: httpUtil.httpConnectionUtility):
    header = httpUtility.createDatalessHeader()
    baseUrl = httpUtility.createBaseItemUrl()
    params:dict = {'recurssive':'false', 'fields':'name,type'}
    response = requests.get(baseUrl,headers=header,params=params)
    print(response)
    if response.status_code == 200:
        # print('System state collected')
        S_json = response.json()
        # print(S_json)
        return list(S_json)
    else:
        return None

def main():
    args = setup_args()
    configStyle = args.testbedConfigStyle
    testCaseGenType = args.testCaseGenerationType
    experimentName = args.experimentName
    testCaseCount = args.testCaseCount
    profiler = time_space.Profiler()
    # profiler.startProfiling('total')
    profiler.startProfiling('config_parser')
    expConfig = toml_parser.InputParser(experimentName)
    if expConfig == None:
        print("Error while parsing toml files")
        return
    
    defenseName = expConfig.defenseName
    hostTitles = expConfig.hostTitles
    evalDirPath = expConfig.evalDirPath
    profiler.endProfiling('config_parser')
    
    if hostTitles.__len__() == 1:
        activeHost = 'au'
    else:
        print('Add support for evaluating defenses based on multiple hosts')
        return

    expId = 0
    seedList = [100, 200, 300, 400, 500, 600]
    expConfig = [5, 10, 15, 25, 35, 50]
    eventCountCap = 15

    while True:
        profiler.startProfiling('testbed_gen')
        clean.Cleaner(evalDirPath, hostTitles)
    
        if configStyle == 'file':
            # fileBasedVtGen.FileBasedVTGen(defenseName, activeHost)
            print('file based testbed gen is temporarily disabled')
        else:
            restApiBasedVTgen.RestAPIbasedVTGen(evalDirPath, activeHost)
    
        httpUtility = httpUtil.httpConnectionUtility(evalDirPath, activeHost)
        testBed = util.getTestBed(httpUtility)
        rootDir = util.getProjectRoot()
        # fp = open(evalDirPath.joinpath('temp-testbed.json').__str__(), 'w')
        # json.dump(testBed, fp=fp, indent=4)
        # return
        # if evluationType=='DT':
        #     filePath = rootDir.joinpath('config').joinpath('testbed-order-expat.json')
        #     fp = open(filePath, 'r')
        #     testBed = json.load(fp)
        # else:
        #     testBed = util.getTestBed(httpUtility)
        

        paltformSetupFilePath = rootDir.joinpath('src').joinpath('platformSetup.toml')
        supportedEvents = tomlparser.load(paltformSetupFilePath.__str__())
        ohSupportedEvents = dict(supportedEvents['OHItems'])
        
        eventDir = rootDir.joinpath('config').joinpath('exps')
        profiler.endProfiling('testbed_gen')

        if testCaseGenType == 'M':
            profiler.startProfiling('event_sim')
            eventSimulation.EventSimulation(defenseName, evalDirPath, activeHost, ohSupportedEvents, False, profiler=profiler)
            profiler.endProfiling('event_sim')
            profiler.saveData(evalDirPath, 'time-space-usage.json')
            return
        else:
            profiler.startProfiling('event_sim')
            seedForRandomGenerator = seedList[expId]
            expCount = expConfig[expId]
            if testCaseCount != 0:
                try:
                    index = expConfig.index(int(testCaseCount))
                except ValueError as ve:
                    print('Testcase count does not match preconfigured test-suites')
                    return
                expCount = expConfig[index]
                seedForRandomGenerator = seedList[index]            
            testCaseDir = eventDir.joinpath('TestSuite-'+str(expCount))
            if util.createDir(testCaseDir) == False:
                print('event directory creation failed for experiment '+str(expCount))
                return
            
            eventGenerator = randomEventGen.RandomEventGenerator(seedForRandomGenerator,testBed, ohSupportedEvents, testCaseDir.__str__())
            eventGenerator.generateExperments('randomExp',expCount, eventCountCap)
            eventSimulation.EventSimulation(defenseName, evalDirPath, activeHost, ohSupportedEvents, False, evalConfig=expCount, profiler=profiler)
            profiler.endProfiling('event_sim')
            profilerOuputDir = evalDirPath.joinpath('TestSuite-'+str(expCount))
            profiler.saveData(profilerOuputDir, 'time-space-usage.json')
            expId = expId+1
            if testCaseCount!=0 or expId == 6:
                return

if __name__ == "__main__":
    main()

