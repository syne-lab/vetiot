from tokenize import String
from typing import Any, List
import requests
import os
import json
import util
import sys
import ruleInstaller
import httpUtil
import time_space

class RestAPIbasedVTGen:
    def __init__(self, evalDirPath, activeHost ) -> None:
        self.httpUtility = httpUtil.httpConnectionUtility(evalDirPath, activeHost)
        print("Wellcome to VT-gen a virtual testbed generationa tool")
        file_name = evalDirPath.joinpath('testbed.json')
        # print('Loading testbed from file:'+file_name)
        with open(file_name.__str__(), 'r') as fp:
            data = json.load(fp)
            fp.close()
            self.parseDeviceConfig(data)
        pass

    def parseDeviceConfig(self, deviceConfig):
        self.createColorItems(deviceConfig['Color'])
        self.createContactItems(deviceConfig['Contact'])
        self.createDateTimeItems(deviceConfig['DateTime'])
        self.createDimmerItems(deviceConfig['Dimmer'])
        self.createGroupItems(deviceConfig['Group'])
        self.createImageItems(deviceConfig['Image'])
        self.createLocationItems(deviceConfig['Location'])
        self.createNumberItems(deviceConfig['Number'])
        self.createPlayerItems(deviceConfig['Player'])
        self.createRollerShutterItems(deviceConfig['Rollershutter'])
        self.createStringItems(deviceConfig['String'])
        self.createSwitchItems(deviceConfig['Switch'])
        return

    def createItem(self, type: String, name: String, label: String): 
        header = self.httpUtility.createHeader('application/json')
        data = {'type': type, 'name': name, 'label':label}
        itemUrl = self.httpUtility.createBaseItemUrl()
        itemUrl = itemUrl+'/'+name
        # print('----------Requesting with data--------')
        print(itemUrl)
        # print(header)
        # print(data)
        r = requests.put(itemUrl,headers=header,data=json.dumps(data))
        # print("request Result-------------")
        print(r)
        return



    #------------------

    # itemTypes

    def createColorItems(self, ColorItemList):
        # print(ColorItemList.__len__())
        for colorItem in ColorItemList:
            if httpUtil.mandatory_keys == colorItem.keys():
                self.createItem('Color', colorItem['Name'], colorItem['Label'])
        return

    def createContactItems(self, ContactItemList):
        # print(ContactItemList.__len__())
        for contactItem in ContactItemList:
            if httpUtil.mandatory_keys == contactItem.keys():
                self.createItem('Contact', contactItem['Name'], contactItem['Label'])
        return

    def createDateTimeItems(self, DateTimeItemList):
        # print(DateTimeItemList.__len__())
        for dateTimeItem in DateTimeItemList:
            if httpUtil.mandatory_keys == dateTimeItem.keys():
                self.createItem('DateTime', dateTimeItem['Name'], dateTimeItem['Label'])
        return

    def createDimmerItems(self, DimmerItemList):
        # print(DimmerItemList.__len__())
        for dimmerItem in DimmerItemList:
            if httpUtil.mandatory_keys == dimmerItem.keys():
                self.createItem('Dimmer',dimmerItem['Name'], dimmerItem['Label'])
        return

    def createGroupItems(self, GroupItemList):
        # print(GroupItemList.__len__())
        for groupItem in GroupItemList:
            if httpUtil.mandatory_keys == groupItem.keys():
                self.createItem('Group', groupItem['Name'], groupItem['Label'])
        return

    def createImageItems(self, ImageItemList):
        # print(ImageItemList.__len__())
        for imageItem in ImageItemList:
            if httpUtil.mandatory_keys == imageItem.keys():
                self.createItem('Image',imageItem['Name'], imageItem['Label'])
        return

    def createLocationItems(self, LocationItemList):
        # print(LocationItemList.__len__())
        for locationItem in LocationItemList:
            if httpUtil.mandatory_keys == locationItem.keys():
                self.createItem('Location',locationItem['Name'], locationItem['Label'])
        return

    def createNumberItems(self, NumberItemList):
        # print(NumberItemList.__len__())
        for numberItem in NumberItemList:
            if httpUtil.mandatory_keys == numberItem.keys():
                self.createItem('Number',numberItem['Name'], numberItem['Label'])
        return

    def createPlayerItems(self, PlayerItemList):
        # print(PlayerItemList.__len__())
        for playerItem in PlayerItemList:
            if httpUtil.mandatory_keys == playerItem.keys():
                self.createItem('Player',playerItem['Name'], playerItem['Label'])
        return

    def createRollerShutterItems(self, RollerShutterItemList):
        # print(RollerShutterItemList.__len__())
        for rollerShutterItem in RollerShutterItemList:
            if httpUtil.mandatory_keys == rollerShutterItem.keys():
                self.createItem('Rollershutter',rollerShutterItem['Name'], rollerShutterItem['Label'])
        return

    def createStringItems(self, StringItemList):
        # print(StringItemList.__len__())
        for stringItem in StringItemList:
            if httpUtil.mandatory_keys == stringItem.keys():
                self.createItem('String', stringItem['Name'], stringItem['Label'])
        return

    def createSwitchItems(self, SwitchItemList: List):
        # print(SwitchItemList.__len__())
        for switchItem in SwitchItemList:
            # print(switchItem)
            # print(httpUtil.mandatory_keys)
            # createSwitchItem(switchItem['Name'], switchItem['Label'])
            # print(switchItem.keys())
            if httpUtil.mandatory_keys == switchItem.keys():
                self.createItem('Switch', switchItem['Name'], switchItem['Label'])
        return

#----Controller-Code---


def installRules(ruleDir, installDir):
    util.copyFile(ruleDir,httpUtil.ohInstallationDir)
    return

# def main():
#     startTime = time_space.startCPUtime()
#     time_space.startTraceMalloc()
#     initMemory = time_space.traceMem()
#     print("Wellcome to VT-gen a virtual testbed generationa tool")
#     # root_dir = os.path.dirname(os.path.abspath('pyvenv.cfg'))
#     root_dir = util.PROJECT_ROOT
#     print('Project root directory is: '+root_dir.__str__())
#     file_name = root_dir.__str__() + '/generated/testbed.json'
#     print('Loading testbed from file:'+file_name)
#     with open(file_name, 'r') as f:
#         data = json.load(f)
    
#     configFilePath = root_dir.joinpath('generated').joinpath('rest-api-config.json')
#     configFileName = configFilePath.__str__()
#     with open(configFileName, 'r') as configFile:
#         restAPIconf = json.load(configFile)
    
#     connInfo = dict(restAPIconf)
#     # print(connInfo)


#     httpUtil.setConnectionParameters(connInfo)
    
#     parseDeviceConfig(data)
#     # setupRestApi(connInfo)
#     # Output: {'name': 'Bob', 'languages': ['English', 'French']}
#     # print(json.dumps(data, indent = 4))
#     time_space.endCPUtime(startTime)
#     time_space.countRequiredMemory(initMemory)
#     time_space.stopTraceMalloc()

# if __name__ == "__main__":
#     main()