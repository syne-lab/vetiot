import pytomlpp as tomlParser
import util
import json

class InputParser:
    def __init__(self, evluationType):
        rootDir = util.PROJECT_ROOT
        # print('project root directory'+rootDir.__str__())
        configPath = rootDir.joinpath('config')
        targetDefenseConfigPath = configPath.joinpath('target-defense-config.toml')
        targetDefense = tomlParser.load(targetDefenseConfigPath.__str__())
        self.defenseName = targetDefense['defense-info']['name']
        if not util.createDir(rootDir.joinpath('generated').__str__()):
            print("Directory creation failed. Major error")
            return None
        self.evalDirPath = rootDir.joinpath('generated').joinpath(self.defenseName+'-'+evluationType)
        if not util.createDir(self.evalDirPath.__str__()):
            print("Directory creation failed. Major error")
            return None

        restAPIOutJsonFilePath = self.evalDirPath.joinpath('defense-info.json')
        with open(restAPIOutJsonFilePath, 'w') as outfile:
            json.dump(targetDefense['defense-info'], outfile, indent=4)
        
        platformConfigPath = configPath.joinpath('platform-config.toml')
        platform = tomlParser.load(platformConfigPath.__str__())

        self.hostTitles = []
        for key in platform:
            restAPIOutJsonFilePath = self.evalDirPath.joinpath(key+'-rest-api-config.json')
            self.hostTitles.append(key)
            with open(restAPIOutJsonFilePath, 'w') as outfile:
                json.dump(platform[key], outfile, indent=4)

        testbed = tomlParser.load(rootDir.__str__() + '/config/testbed-config.toml')
        outputDictionary = self.fillJsonDB(testbed)
        outputJsonFilePath = self.evalDirPath.joinpath('testbed.json')
        with open(outputJsonFilePath, 'w') as outfile:
            json.dump(outputDictionary, outfile, indent=4)
        return
    
    def fillJsonDB(self, rawDictionary: dict):
        outputDictionary=dict()
        #initialize jsondb
        outputDictionary['Color'] = []
        outputDictionary['Contact'] = []
        outputDictionary['DateTime'] = []
        outputDictionary['Dimmer'] = []
        outputDictionary['Group'] = []
        outputDictionary['Image'] = []
        outputDictionary['Location'] = []
        outputDictionary['Number'] = []
        outputDictionary['Player'] = []
        outputDictionary['Rollershutter'] = []
        outputDictionary['String'] = []
        outputDictionary['Switch'] = []

        for itemName,itemConfig in rawDictionary.items():
            itemType = itemConfig['Type']
            itemLabel = itemConfig['Label']
            item = dict()
            item['Name'] = itemName
            item['Label'] = itemLabel       
            outputDictionary[itemType].append(item)
        return outputDictionary


# if __name__ == "__main__":
#     main()