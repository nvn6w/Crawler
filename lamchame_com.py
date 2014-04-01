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
    
if __name__ == '__main__':
    obj = lamchame_com()
    
    # Test get all topic
    #obj.getAllTopics()
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
    
    
        