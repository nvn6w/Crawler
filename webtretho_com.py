# -*- coding: utf-8 -*-
'''
Created on Mar 11, 2014

@author: kimphuc
'''
from exceptions import Exception
from bs4 import BeautifulSoup
from utils.Request import Request
import time

class webtretho_com(object):    
    
    def getAllTopics(self):
        '''
        Get all topic in forum
        '''
        res = []
        
        baseUrl = 'http://www.webtretho.com/forum/f'
        
        url = 'http://www.webtretho.com/forum/search.php?search_type=1&contenttype=vBForum_Post'
        html = Request.get_page_content(url)
        soup = BeautifulSoup(html)
        
        soupCates = soup.find('select', {'id' : 'forumchoice'})
        cates = soupCates.findAll('option')
        for cate in cates:
            topicNumber = cate['value']
            
            if topicNumber.isdigit():                
                topicUrl = baseUrl + topicNumber + '/'
                res.append(topicUrl)
                #title = cate.string.strip()
                #print topicUrl
                #print '--------------'
        return res
                
    def getTotalPageInTopic(self, topicUrl):
        '''
        Get total page in a topic
        '''
        total = 0
        html = Request.get_page_content(topicUrl)
        soup = BeautifulSoup(html)
        pageNav = soup.find('div', {'class' : 'threadpagenav'})
        if pageNav:
            lastPage = pageNav.find('span', {'class' : 'first_last1'})
            if lastPage:
                #print lastPage.string
                total = int(lastPage.string)
        
        return total
    
    
    def getNextPageUrlInTopic(self, topicUrl, nextPage):
        '''
        Get next page in a topic
        '''
        return topicUrl + 'index' + str(nextPage) + '.html'
    
    
    def getThreadsInTopic(self, topicUrl):
        '''
        Get all threads in a topic
        '''
        res = {}
        html = Request.get_page_content(topicUrl)
        soup = BeautifulSoup(html)
        
        threads = soup.find('ul', {'id' : 'threads'})
        print threads
        if threads:        
            for thread in threads: #.findAll('h3', {'class' : 'threadtitle'}):
                print thread
                try:
                    tLink = thread.find('a', {'class' : 'title'})
                    if (tLink) :
                        print tLink['href']
                        #print tLink.string
                    print '-----------'
                except Exception,e:
                    print e.message;
        return res


    def getThreadDetail(self, url):
        '''
        Get thread detail info
        '''
        res = {}
        html = Request.get_page_content(url);
        soup = BeautifulSoup(html)        
        
        return res
    
    
if __name__ == '__main__':
    
    obj = webtretho_com()
    
    # test get topics
    #obj.getAllTopics()
    
    # test get all thread in topic
    #topicUrl  = 'http://www.webtretho.com/forum/f3814/'
    #obj.getThreadsInTopic(topicUrl)
    
    topics = obj.getAllTopics()
    count = 0
    for topic in topics:
        count += 1
        if (count > 10):
            break
        print '--------------------------------'
        print 'Topic: ', topic
        obj.getThreadsInTopic(topic)
        time.sleep(10)
    
    url = 'http://www.webtretho.com/forum/f3775/chong-doi-lay-vo-khac-khi-da-co-3-dua-con-phai-lam-sao-1855059/'
    
    print 'DOne'
