from fabric import Connection
import util
import json

def getConnection(hostname):
    rootDir = util.getProjectRoot()
    sshConfigFileDir = rootDir.joinpath('env-setup').joinpath('sshconfig')
    sshConfigFilePath = sshConfigFileDir.joinpath(hostname+'.json')
    if not util.doesFileExists(sshConfigFilePath.__str__()):
        print('ssh config file does not exist for this hostname.')
        return None
    with open(sshConfigFilePath) as fp:
        sshConfig = json.load(fp)
        host = sshConfig['HostName']
        port = sshConfig['Port']
        user = sshConfig['User']
        sshKeyDict = {}
        sshKeyDict['key_filename'] = sshConfig['IdentityFile']
        connection = Connection(host=host, port=port, user=user, connect_kwargs=sshKeyDict)
        return connection
    
def sendFile(hostname, src, dest) -> bool:
    rootDir = util.getProjectRoot()
    sshConfigFileDir = rootDir.joinpath('env-setup').joinpath('sshconfig')
    sshConfigFilePath = sshConfigFileDir.joinpath(hostname+'.json')
    if not util.doesFileExists(sshConfigFilePath.__str__()):
        print('ssh config file does not exist for this hostname.')
        return None
    with open(sshConfigFilePath) as fp:
        sshConfig = json.load(fp)
        host = sshConfig['HostName']
        port = sshConfig['Port']
        user = sshConfig['User']
        sshKeyDict = {}
        sshKeyDict['key_filename'] = sshConfig['IdentityFile']
        connection = Connection(host=host, port=port, user=user, connect_kwargs=sshKeyDict)
        result = connection.put(src, dest)
        
        if result.remote is not None:
            return True
        else:
            return False

