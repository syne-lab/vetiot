import util
# import sshConnectionUtil
from pathlib import Path
class RuleInstaller:
    rulesDir: Path
    ohRulesDir:Path
    host:str
    def __init__(self, host, srcDir:Path, destinationDir:Path) -> None:
        self.host = host
        if util.doesFileExists(srcDir)==False:
            print("source directory of rule doesn't exist")
            return None
        else:
            self.rulesDir = srcDir
        
        if host=='au':
            if util.doesFileExists(destinationDir)==False:
                print("Destiation Directory of rule doesn't exist")
                return None
        self.ohRulesDir = destinationDir

    def installRules(self):
        # print('copying rules from ' + self.rulesDir.__str__() + ' to ' + self.ohRulesDir.__str__())
        destinationDir = util.getPath(self.ohRulesDir)
        for path in util.listDirectory(self.rulesDir, '*.rules'):
            util.copyFile(path.__str__(),destinationDir.__str__())
        return
    
    # def installRulesSSH(self):
    #     for path in util.getPath(self.rulesDir).glob('**/*.rules'):
    #         fileName = path.name
    #         if self.host in fileName:
    #             sshConnectionUtil.sendFile(self.host, path.__str__(), self.ohRulesDir.__str__())
    #         else:
    #             sshConnectionUtil.sendFile('au', path.__str__(), self.ohRulesDir.__str__())

    def unInstallRules(self):
        # print('uninstalling rules from ' + self.rulesDir.__str__() + ' to ' + self.ohRulesDir.__str__())
        destinationDir = util.getPath(self.ohRulesDir)
        for path in util.listDirectory(destinationDir, '*.rules'): #util.getPath(destinationDir).glob('**/*.rules'):
            util.deleteFile(path.__str__())
        return

    # def unInstallRulesSSH(self):
    #     connection = sshConnectionUtil.getConnection(self.host)
    #     with connection.cd(self.ohRulesDir.__str__()):
    #         connection.run('rm *.rules || true')
    #     connection.close()
    #     return


def main():
    rulesDir = util.PROJECT_ROOT.__str__() + '/config/rules/'
    ohInstallationDir = '/Users/akib0112/Downloads/openhab-3.2.0/'
    ruleInstaller = RuleInstaller(rulesDir,ohInstallationDir)
    ruleInstaller.installRules()

if __name__ == "__main__":
    main()