# -*- coding: utf-8 -*-
'''
Created on Mar 11, 2014

@author: kimphuc
'''
from bs4 import BeautifulSoup
from utils.Request import Request
import time

class lamchame_com(object):
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
                res.append(topicUrl)
                #print title
                #print topicUrl
                #print '--------------'
        return res

        
    def getThreadsInTopic(self, topicUrl):
        '''
        Get all threads in a topic
        '''
        res = {}
        html = Request.get_page_content(topicUrl)
        soup = BeautifulSoup(html)
        
        threads = soup.find('div', {'id' : 'forumbits'})        
        if threads:        
            for thread in threads.findAll('h2', {'class' : 'forumtitle'}):
                print thread
                tLink = thread.find('a')  
                if (tLink) :    
                    
                    tUrl  = tLink['href']
                    #tUrl = 'http://www.otofun.net/forums/' + tUrl
                    print tUrl
                    print tLink.string 
                print '-----------'
        return res
        
        
        return res
    
    def getTheadDetail(self, url):
        headers = { 
               'Host' : 'www.lamchame.com',
               'Accept-Language' : 'en-US,en;q=0.5',
               'User-Agent' : '    Mozilla/5.0 (Windows NT 6.1; rv:28.0) Gecko/20100101 Firefox/28.0' ,
               'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
               'Referer': '',
              }
        html = Request.get_page_content(url, {}, headers)
        soup = BeautifulSoup(html)
        #print soup
        postContainer = soup.find('ol', {'id' : 'posts'})
        print postContainer
        
        #posts = postContainer.findAll('li')
        #for post in posts:
        #    print post.id        
                
    
if __name__ == '__main__':
    obj = lamchame_com()
    
    url = 'http://www.lamchame.com/forum/showthread.php/1299426-Khoe-các-mẹ-ảnh-2-nhóc-nhà-mình'
    
    obj.getTheadDetail(url)
    exit(0)
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
        obj.getThreadsInTopic(topic)
        
    
    # Test get total page in a topic
    #topicUrl = 'http://www.webtretho.com/forum/f3512/'
    #topicUrl  ='http://www.webtretho.com/forum/f199/'
    #total = obj.getTotalPageInTopic(topicUrl)
    #print total
    
    
        