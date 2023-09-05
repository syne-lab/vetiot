import util
import sshConnectionUtil

class FileBasedVTGen:
    def __init__(self, defense, activeHost) -> None:
        self.defense = defense
        self.copyThingsFile(activeHost)
        self.copyItemsFile(activeHost)
        util.createDelay(5)
        # self.copyRuleFiles()

    def copyThingsFile(self, hosttitle):
        projectRoot = util.getProjectRoot()
        thingsFileDir = projectRoot.joinpath('config').joinpath('things')
        thingsFiles = util.listDirectory(thingsFileDir, '*.things')
        for file in thingsFiles:
            filename = file.name
            destinationFile = '/etc/openhab/things/'+filename
            if hosttitle in filename:
                sshConnectionUtil.sendFile(hosttitle,file.__str__(), destinationFile)
            else:
                sshConnectionUtil.sendFile('au',file.__str__(), destinationFile)
    
    def copyItemsFile(self, hosttitle):
        projectRoot = util.getProjectRoot()
        thingsFileDir = projectRoot.joinpath('config').joinpath('items')
        thingsFiles = util.listDirectory(thingsFileDir, '*.items')
        for file in thingsFiles:
            filename = file.name
            destinationFile = '/etc/openhab/items/'+filename
            if hosttitle in filename:
                sshConnectionUtil.sendFile(hosttitle,file.__str__(), destinationFile)
            else:
                sshConnectionUtil.sendFile('au',file.__str__(), destinationFile)