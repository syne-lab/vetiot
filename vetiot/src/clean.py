import requests
import httpUtil

class Cleaner:
    def __init__(self, evalDirPath, hostTitles) -> None:
        # defenseInfoPath = util.getProjectRoot().joinpath('generated').joinpath(defense).joinpath('defense-info.json')
        # if not util.doesFileExists(defenseInfoPath.__str__()):
        #     print("Defense info not found. Cleaning aborted")
        #     return None
        # with open(defenseInfoPath, 'r') as f:
        #     defenseInfo = json.load(f)
        #     f.close()
        for title in hostTitles:
            utility = httpUtil.httpConnectionUtility(evalDirPath, title)
            self.cleanRestApiCreatedItems(utility)
            # self.cleanConfigFiles(title)

    pass

    def cleanRestApiCreatedItems(self, utility):
        header = utility.createHeader('application/json')
        baseUrl = utility.createBaseItemUrl()
        print('----------Requesting with data--------')
        print(baseUrl)
        print(header)
        params={'recursive': 'false'}
        r = requests.get(baseUrl,headers=header,params=params)
        print("request Result-------------")
        print(r)
        response = r.json()
        if 'error' in response:
            return
        for item in response:
            # print(item['name'])
            if 'Zigbee' in item['name']:
                continue
            elif 'Zwave' in item['name']:
                continue
            else:
                itemUrl=baseUrl+'/'+item['name']
                print('delete url ' + itemUrl)
                res = requests.delete(itemUrl, headers=header)
                print(res.text)
        return
    
    # def cleanConfigFiles(self, title):
    #     connection = sshConnectionUtil.getConnection(title)
    #     connection.run('hostname')
    #     ohDirectory = '/etc/openhab/'
    #     with connection.cd(ohDirectory):
    #         with connection.cd('./items'):
    #             connection.run('rm *.items || true')
    #         with connection.cd('./things'):
    #             connection.run('rm *.things || true')
    #         with connection.cd('./rules'):
    #             connection.run('rm *.rules || true')
    #     connection.close()



# def main():
#     pass

# if __name__ == "__main__":
#     main()