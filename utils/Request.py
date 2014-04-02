'''
Created on Oct 9, 2012

@author: kimphuc
'''
import traceback
import urllib2
import cookielib
import urllib

class Request(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    @staticmethod
    def get_page_content(url, params={}, headers={}):        
        headers2 = {
            'Accept':'    text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            #'Origin': 'http://www.indiapost.gov.in',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:28.0) Gecko/20100101 Firefox/28.0',
            #'Content-Type': 'application/x-www-form-urlencoded',
            #'Referer': 'http://www.indiapost.gov.in/pin/',
            #'Accept-Encoding': 'gzip,deflate,sdch',
            #'Accept-Language': 'en-US,en;q=0.8',
            #'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'
        }
        
        if (len(headers) == 0) :
            headers = headers2
        
        params = urllib.urlencode(params)
        request = urllib2.Request(url, params, headers)
        cookies = cookielib.CookieJar()
        ck_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
        #ck_opener = urllib2.build_opener()
        response = ck_opener.open(request)
        print response.info()
        html = response.read()
        return html
    
    
    def downloadFile(self, save_path, url):
        res = False
        try:
            f = open(save_path, "w")
        except:
            tb = traceback.format_exc()
            print tb
            return res
        
        try: 
            resp = urllib2.urlopen(url)
        except urllib2.HTTPError:
            tb = traceback.format_exc()
            print tb      
            return res  
                
        totalSize = int(resp.info().getheader('Content-Length').strip())
        currentSize = 0
        CHUNK_SIZE = 32768
        while True:
            data = resp.read(CHUNK_SIZE)
            if not data:                
                break
            currentSize += len(data)
            f.write(data)                            
            if currentSize >= totalSize:
                break
        f.close()
        res = True
        
        return res
    
