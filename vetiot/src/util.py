from distutils.log import error
from pathlib import Path
import os
import shutil
import httpUtil
import requests
import time

PROJECT_ROOT = Path(__file__).parent.parent

def getProjectRoot() -> Path:
    return Path(__file__).parent.parent
    
def doesFileExists(filePath: str) -> bool:
    return Path(filePath).exists()

def isDirectory(filePath:str)->bool:
    return Path(filePath).is_dir()

def getPath(stringPath:str):
    return Path(stringPath)


def copyFile(src:str, dest: str):
    try:
        shutil.copy(src,dest)
    except shutil.SameFileError:
        print('Source file and destination file is same')
    except IsADirectoryError:
        print('Destination is a directory')
    except PermissionError:
        print('Permission Denied')
    except:
        print('Error occurred while copying file')
    return

def deleteFile(filePath:str)->bool:
    try:
        Path(filePath).unlink(True)
    except FileNotFoundError:
        print('file Not found')
        return False
    except:
        print('unknown error')
        return False
    return True

def createDir(dirPath:Path)->bool:
    path = Path(dirPath)
    try:
        path.mkdir()
    except FileNotFoundError:
        print('Directory creation failed'+ FileNotFoundError)
        return False
    except FileExistsError:
        for file_name in os.listdir(path.__str__()):
            # construct full file path
            file = path.__str__() + '/' + file_name
            if os.path.isfile(file):
                print('Deleting file:', file)
                os.remove(file)
    return True

def listDirectory(dirPath: Path, pattern: str) -> list:
    path = Path(dirPath)
    try:
        pathlist = []
        for path in path.glob(pattern):
            pathlist.append(path)
        return pathlist
    except NotADirectoryError:
        print("The path is not a directory")
        return []
    
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
        itemList = list(S_json)
        itemList.sort(key=lambda x:x['name'])
        return list(S_json)
    else:
        return None
    
def createDelay(duration: int):
    time.sleep(duration)
    # if duration<=10:
    #     global delayTotalTime
    #     delayTotalTime = delayTotalTime+duration
    return