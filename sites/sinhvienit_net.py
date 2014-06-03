# -*- coding: utf-8 -*-
'''
Created on May 30, 2014

@author: kimphuc
'''
import requests

class sinhvienit_net(object):
    '''
    classdocs
    '''
    def byPassReferer(self):
        url  = 'http://sinhvienit.net/home/'
        headers = {
                'Referer': 'http://sinhvienit.net/home/',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; rv:29.0) Gecko/20100101 Firefox/29.0',
                'Host': 'sinhvienit.net',
                }
        
        url2 = 'http://sinhvienit.net/vtlai.php'
        data = {'vtlai_firewall_redirect' : '/home/', 'vtlai_firewall_postcontent' : ''}
        client = requests.Session()
        client.post(url2, data = data, headers = headers)
        
        #r = client.get(url, headers = headers)
        #print r.text.encode('utf-8')
        return client
    
if __name__ == '__main__':
    obj = sinhvienit_net()
    #client = obj.byPassReferer()
    url = 'http://sinhvienit.net/forum/download-powerdesigner-15-kem-cach-su-dung.49227.html'
    
    headers = {
                'Referer': 'http://sinhvienit.net/home/',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; rv:29.0) Gecko/20100101 Firefox/29.0',
                'Host': 'sinhvienit.net',
                }
    client = requests.Session()
    client.get('http://sinhvienit.net/home/', headers = headers)
    r = client.get(url, headers = headers)    
    html = r.text
    f = open('d:/tes11.html', 'w')
    f.write(html)
    f.close()
    print 'Done'
        