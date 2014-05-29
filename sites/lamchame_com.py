# -*- coding: utf-8 -*-
'''
Created on Mar 11, 2014

@author: kimphuc
'''
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from bs4 import BeautifulSoup
from utils.Request import Request
import urllib
import re
from sites.ISite import ISite

class lamchame_com(ISite):
    '''
    classdocs
    '''

    def getAllTopics(self):
        res = []
        
        baseUrl = 'http://www.lamchame.com/forum/forumdisplay.php/'
        
        searchUrl = 'http://www.lamchame.com/forum/search.php?search_type=1&contenttype=vBForum_Post'
        html = Request.get_page_content(searchUrl)
        soup = BeautifulSoup(html)
        
        soupCates = soup.find('select', {'id' : 'forumchoice'})
        cates = soupCates.findAll('option')
        for cate in cates:
            topicNumber = cate['value']            
            if topicNumber.isdigit():                
                title = cate.string.strip()
                topicUrl = baseUrl + topicNumber + '-' + title.replace(' ', '-')
                res.append(topicUrl.encode('utf-8'))
        return res
        
    def getThreadsInTopic(self, topicUrl):
        '''
        Get all threads in a topic
        '''
        
        res = []
        #html = Request.get_page_content(topicUrl)
        html = urllib.urlopen(topicUrl)
        soup = BeautifulSoup(html)
        
        threads = soup.find('ol', {'id' : 'threads'})        
        if threads:                    
            for thread in threads.findAll('li', {'class' : 'threadbit '}):                            
                tLink = thread.find('a', {'class' : 'title'})  
                if tLink :                        
                    tUrl  = tLink['href']
                    if tUrl:
                        pos = tUrl.find('?s=') # loai bo chuoi ?s= .....
                        if pos != -1:
                            tUrl = tUrl[0:pos]
                        
                        # them base URL    
                        tUrl = 'http://www.lamchame.com/forum/' + tUrl
                        
                        res.append(tUrl)
                        #print tUrl 
                        #print '-----------'
        return res
    
    def getTotalPageInTopic(self, topicUrl):
        '''
            Lay tong so page trong 1 topic
        '''        
        total = 0
        html = urllib.urlopen(topicUrl)
        soup = BeautifulSoup(html)
        nav = soup.find('div', {'class' : 'threadpagenav'})
        if nav:
            lastPage = nav.find('span', {'class' : 'first_last'})
            if lastPage:
                aLink = lastPage.find('a')
                if aLink:
                    url = aLink['href']
                    pos1 = url.find('/page')
                    pos2 = url.find('?s=')
                    if pos1 != -1:
                        if pos2 != -1: # ton tai ?s=
                            page = url[pos1+5:pos2]
                        else :
                            page = url[pos1+5:]
                        total = int(page)                                           
        return total
    
    def getNextPageInTopic(self, topicUrl, nextPage):
        '''
            Get next page in a topic            
            @topicUrl: URL of topic
            @nextPage: end with /            
        '''        
        if topicUrl.endswith('/') :
            return topicUrl + 'page' + str(nextPage)
        else:
            return topicUrl + '/page' + str(nextPage)
    
    def getPagesInTopic(self, topicUrl):
        '''
            Lay tat ca cac page (co phan trang) tu 1 topic
        '''
        res = []
        totalPage = self.getTotalPageInTopic(topicUrl)
        if totalPage == 0:
            res.append(topicUrl)
        else :
            for nextPage in range(1, totalPage + 1):
                page = self.getNextPageInTopic(topicUrl, nextPage)
                res.append(page)
        return res    
    
    def getThreadDetail(self, url):
        res = {}
        
        try :
            html = urllib.urlopen(url)
            soup = BeautifulSoup(html)
            #print soup
            postContainer = soup.find('ol', {'id' : 'posts'})
            
            title = soup.find('span', {'class' : 'threadtitle'}).get_text().strip()
            
            posts = postContainer.findAll('li', {'class' : 'postbit postbitim postcontainer'})
            
            count = 0
            comments = []
            for post in posts:
                
                #print post
                count += 1 
                                   
                postContent = post.find('blockquote', {'class' : 'postcontent restore'})
                postContent = postContent.get_text()
                #postContent = re.sub('<br/>+', '_NEW_LINE_', postContent)
                postContent = re.sub('[\t]+', ' ', postContent)
                postContent = re.sub('[ ]+', ' ', postContent)
                postContent = re.sub('[\r\n]+', '\r\n', postContent)
                postContent = postContent.strip()            
                
                # date infomation
                dateInfo = post.find('span', {'class' : 'postdate'}).get_text().strip()
                dateInfo = re.sub('\s+', ' ', dateInfo)

                # user infomation
                userInfo = post.find('div', {'class' : 'username_container'}).find('strong').get_text().strip()
                
                info = {'user' : userInfo, 'date': dateInfo, 'content' : postContent}
                
                if count == 1: # post
                    postInfo = info;
                    postInfo['title'] = title
                    res['post']= postInfo
                else :  # comment
                    comments.append(info)
                    
            res['comments'] = comments
            
        except:
            print 'ERROR when crawling URL : ' , url
            pass
        
        return res
        
        #posts = postContainer.findAll('li')
        #for post in posts:
        #    print post.id        
                
    
if __name__ == '__main__':
    obj = lamchame_com()
    
    '''    
    url = 'http://www.lamchame.com/forum/showthread.php/1299426-Khoe-các-mẹ-ảnh-2-nhóc-nhà-mình'
    import urllib

    html = urllib.urlopen(url).read()
    print html
    '''
    
    # test get all threads in topic
    #topicUrl = 'http://www.lamchame.com/forum/forumdisplay.php/205-Quy-định-&-Hướng-dẫn-sử-dụng'
    
    
    #obj.getTheadDetail(url)
    
    '''
    # test total page in topic
    url = 'http://www.lamchame.com/forum/forumdisplay.php/639-CU%E1%BB%98C-THI-%E2%80%9CGI%C3%9AP-B%C3%89-%C4%82N-RAU-QU%E1%BA%A2%E2%80%9D'
    url = 'http://www.lamchame.com/forum/forumdisplay.php/239-S%E1%BB%AFa-cho-b%C3%A9'
    obj.getTotalPageInTopic(url)
    pages = obj.getPagesInTopic(url)
    for p in pages:
        print p
        print '-------------------'    
    '''
    
    '''
    # Test get all topic
    topics = obj.getAllTopics()
    count = 0
    
    for topic in topics:
        time.sleep(1)
        count += 1
        if (count > 10):
            break
        print '--------------------------------'
        print 'Topic: ', topic
        #obj.getThreadsInTopic(topic)
        topicPages = obj.getPagesInTopic(topic)
        for p in topicPages:
            print 'PAGE: ' , p
    
    '''
    
    # test get thread detail
    url = 'http://www.lamchame.com/forum/showthread.php/1352606-Gi%C3%BAp-em-c%C3%A0i-%C4%91%E1%BA%B7t-ahamai'
    res = obj.getThreadDetail(url)
    
    comments = res['comments']
    for c in comments:
        print c['content']
        print '-----------------'
    
    
        
