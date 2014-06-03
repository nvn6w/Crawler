'''
Created on May 30, 2014

@author: kimphuc
'''

import requests

class homesub_vn(object):
    '''
    classdocs
    '''
    
    def login(self):
        client = requests.Session()
        data = {'register' : 0, 'password' : '123456', 'login' : 'kimxuanphuc@gmail.com', 'remember' : 1}
        loginUrl = 'http://homesub.vn/login/login'
        r = client.post(loginUrl, data = data)
        return client
                
    def getThreadDetail(self, client, threadUrl):
        r2 = client.get(threadUrl)
        html = r2.text.encode('utf-8')
        f = open('d:/test10.html', 'w')
        f.write(html)
        f.close()
        
if __name__ == '__main__':
    
    obj = homesub_vn()    
    url = 'http://homesub.vn/threads/non-stop-2014-1080p-bluray-dts-x264-wiki-khong-dung-lai-sub-viet.10981/'
    client = obj.login()
    obj.getThreadDetail(client, url)
    
    
    
    