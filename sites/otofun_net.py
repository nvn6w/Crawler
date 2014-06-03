# -*- coding: utf-8 -*-
'''
Created on Mar 10, 2014

@author: kimphuc
'''
from utils.Request import Request
from bs4 import BeautifulSoup
import MySQLdb
from MySQLdb.cursors import *
import time
import re
from sites.ISite import ISite

class otofun_net(object):
    '''
    classdocs
    '''

    listUrl = []
    listPostId = []

    def getAllTopics(self):
        res = []
        
        baseUrl  ='http://www.otofun.net/'
        url = 'http://www.otofun.net/forum.php'
        
        html = Request.get_page_content(url)
        soup = BeautifulSoup(html)
        links = soup.findAll('a')
        for link in links:
            if link['href'].startswith('forums/'):
                u = link['href']
                pos = u.find('?s=')
                if pos != -1:
                    u = u[0:pos]
                u = baseUrl + u                
                res.append(u)
        return res  
    
    def getTotalPageInTopic(self, topicUrl):
        '''
            Lay tong so page trong 1 topic
        '''        
        total = 0
        html = Request.get_page_content(topicUrl)
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
            return topicUrl + 'page' + str(nextPage) + "?order=desc"
        else:
            return topicUrl + '/page' + str(nextPage) + "?order=desc"
    
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
    
    def getThreadsInTopic(self, topicUrl):
        '''
        Get all threads in a topic
        '''

        res = []
        html = Request.get_page_content(topicUrl)
        soup = BeautifulSoup(html)
        
        threads = soup.find('ol', {'id' : 'threads'})        
        if threads:
            #find thread
            for thread in threads.findAll('h3', {'class' : 'threadtitle'}):
                #print thread
                tLink = thread.find('a', {'class' : 'title'})
                if (tLink) :
                    tUrl  = tLink['href']
                    pos = tUrl.find('?s=')
                    if pos:
                        tUrl = tUrl[0:pos]
                    tUrl = 'http://www.otofun.net/forums/' + tUrl
                    if tUrl not in res:
                        res.append(tUrl)
        return res               
    
    def getThreadDetail(self, url):
        res = {}
        
        try :
            html = Request.get_page_content(url)
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
                postContent = re.sub('[\\r\\n]+', '\n', postContent)
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
    
if __name__ == '__main__':
    obj = otofun_net()
    #links = obj.getAllTopics()
    #for link in links:
    #    print link
    
    '''
    topics = obj.getAllTopics()
    count = 0
    for topic in topics:
        count += 1
        if (count > 10):
            break
        print '--------------------------------'
        print 'Topic Level-1: ', topic
        obj.getThreadsInTopic(topic)
        time.sleep(1)
    '''
    # Test get total page in thread
    
    '''
    # Test get thread in topic
    url = 'http://www.otofun.net/forums/63-clb-offroad'
    totalPage = obj.getTotalPageInTopic(url)
    print totalPage
    pages = obj.getPagesInTopic(url)
    for p in pages:
        print p
    '''
    
    '''
    # Test get Thread detail
    url = 'http://www.otofun.net/threads/531610-thong-tin-ve-viec-vinh-danh-cac-thanh-vien-of-co-cac-dong-gop-dac-biet'
    #url = 'http://www.otofun.net/threads/679592-e-xin-tai-lieu-ve-khao-sat-bo-dong-toc-tren-dong-co-diesel-dung-bom-cao-ap-bosch'    
    res = obj.getThreadDetail(url)
    print res['post']['content']
    comments = res['comments']
    for c in comments:
        print c['user']
        print c['date']
        print c['content']
        print '------------------'
    '''
    
    '''
    # Test thread detail
    url = 'http://www.otofun.net/forums/128-phong-truyen-thong-of'
    headers2 = {
            'Accept':'    text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            #'Origin': 'http://www.indiapost.gov.in',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:28.0) Gecko/20100101 Firefox/28.0',
            #'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'http://www.indiapost.gov.in/pin/',
            #'Accept-Encoding': 'gzip,deflate,sdch',
            #'Accept-Language': 'en-US,en;q=0.8',
            #'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'
        }
    html = Request.get_page_content(url);
    print html
    '''
    
            
