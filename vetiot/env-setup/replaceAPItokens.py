from pathlib import Path
import pytomlpp as tomlParser

newTokenFile = open('restapitoken.txt')
newAPItoken = newTokenFile.readline()
tokenString = str(newAPItoken).strip()

PROJECT_ROOT = Path(__file__).parent.parent

testConfigDir = PROJECT_ROOT.joinpath('test-configs')

for filePath in testConfigDir.glob('**/platform-config.toml'):
    platformConfig = tomlParser.load(filePath)
    filePath.unlink(True)
    # newConfig = platformConfig['au']
    config = platformConfig['au']
    config['api-token'] = tokenString
    config['oh-config-dir'] = 'env-setup/openhab-3.2.0/conf/'
    newDict = dict()
    newDict['au'] = config
    tomlParser.dump(newDict, filePath)

