# -*- coding: utf-8 -*-
'''
Created on Mar 11, 2014

@author: kimphuc
'''
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))


from exceptions import Exception
from bs4 import BeautifulSoup
from utils.Request import Request
import re
from sites.ISite import ISite

import traceback    # trace the errors

class webtretho_com(ISite):    
    
    def getAllTopics(self):
        '''
        Lay ds cac topic co trong forum
        '''
        res = []
        try:
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
        except Exception, e:
            print e.message;
            tb = traceback.format_exc()
            print tb
            pass
        return res
                
    def getTotalPageInTopic(self, topicUrl):
        '''
        Get total page in a topic
        '''
        total = 0
        try:
            html = Request.get_page_content(topicUrl)
            soup = BeautifulSoup(html)
            pageNav = soup.find('div', {'class' : 'threadpagenav'})
            if pageNav:
                lastPage = pageNav.find('span', {'class' : 'first_last1'})
                if lastPage:
                    #print lastPage.string
                    total = int(lastPage.string)
        except:
            print 'Error when get total page'
            pass            
        
        return total
        
    def getNextPageUrlInTopic(self, topicUrl, nextPage):
        '''
            Get next page in a topic
        '''
        return topicUrl + 'index' + str(nextPage) + '.html'
    
    def getPagesInTopic(self, topicUrl):
        '''
            Lay tat ca cac page (co phan trang) tu 1 topic
        '''
        res = []
        try:
            totalPage = self.getTotalPageInTopic(topicUrl)
            if totalPage == 0:
                res.append(topicUrl)
            else :
                for nextPage in range(1, totalPage + 1):
                    page = self.getNextPageInTopic(topicUrl, nextPage)
                    res.append(page)
        except:
            print 'Error when get pages in topic'
            pass
        return res                
    
    def getThreadsInTopic(self, topicUrl):
        '''
        Lay tat ca cac thread goc co trong 1 topic
        '''
        res = []
        try:
            html = Request.get_page_content(topicUrl)
            soup = BeautifulSoup(html)
            ulThread = soup.find('ul', {'id' : 'threads'})
            #print ulThread
            if ulThread:
                threads = ulThread.findAll('li', {'class' : 'threadbit_nam_fix_select'})    
                if threads:                 
                    for thread in threads:
                        try:
                            #import pdb
                            #pdb.set_trace()
                            #print thread
                            tLink = thread.find('a', {'class' : 'title'})
                            if (tLink) :
                                tUrl = tLink['href']
                                res.append(tUrl)
                                #print tUrl
                                #print '--------------------'
                        except Exception,e:
                            print e.message;
                            tb = traceback.format_exc()
                            print tb
        except Exception, e:
            print e.message;
            tb = traceback.format_exc()
            print tb
            pass
        return res
    
    def getTotalPageInThread(self, url):
        '''
            Lay tong so page co trong 1 thread
        '''
        total = 1
        html = Request.get_page_content(url);
        soup = BeautifulSoup(html)
        pageInfo = soup.find('div', {'class' : 'pageRefix'})
        if pageInfo:
            lastPage = pageInfo.find('a', {'class' : 'arrowLstPage'})
            if lastPage:
                #print lastPage
                link = lastPage['href']
                #print link
                pos = link.index('.html')
                
                if pos != False:
                    p = re.compile("index(\d+).html")
                    a =  p.search(link)
                    #print link[pos-1:]
                    total = a.group(1)
                    total = int(total)
                    #print total
        return total

    def getPagesInThread(self, url):
        '''
            Lay ds cac page cua 1 thread
        '''
        totalPage = self.getTotalPageInThread(url)
        for i in range (1, totalPage+1):
            if i == 1:
                page = url
                pass
            else:
                if '/' == url[-1]:
                    page = url + 'index' + str(i)+ '.html'
                else :
                    page = url + '/index' + str(i)+ '.html'
            print page
        
    def getThreadDetail(self, url):
        '''
            Lay thong tin chi tiet cua 1 thread
        '''
        #res = { 'post' : {'user' : '', 'title': '', 'date' : '', 'content' : ''}, 'comments' : [{'user' : '', 'date': '', 'content' : ''}] }
        res = {}
        try:
            html = Request.get_page_content(url);
            soup = BeautifulSoup(html)        
            soupPost = soup.find('ol', {'id' : 'posts'})
            
            title = soup.find('div', {'id' : 'widgetRefix'}).find('h1').get_text().strip()
            #print title
                
            # list posts
            posts = soupPost.findAll('li', {'class' : 'postbit postbitim postcontainer'})
            #print posts
            #print len(posts)
            #print posts.size()            
            count = 0
            comments = []
                        
            for post in posts:
                
                #print post
                count += 1 
                                   
                postContent = post.find('blockquote', {'class' : 'postcontent restore'})
                #postContent = postContent.renderContents()
                postContent = postContent.get_text()
                #print postContent
                #print '----------------------'
                postContent = re.sub('[\t]+', ' ', postContent)
                postContent = re.sub('[ ]+', ' ', postContent)
                postContent = re.sub('[\\r\\n]+', '\n', postContent)
                postContent = postContent.strip()
                #print soup2.get_text().strip()
                
                #print postContent
                
                # date infomation
                dateInfo = post.find('span', {'class' : 'postdate'}).get_text().strip()
                dateInfo = re.sub('\s+', ' ', dateInfo)
                #print dateInfo

                # user infomation
                userInfo = post.find('div', {'class' : 'username_container'}).get_text().strip()
                #print userInfo
                
                info = {'user' : userInfo, 'date': dateInfo, 'content' : postContent}
                
                if count == 1: # post
                    postInfo = info;
                    postInfo['title'] = title
                    res['post']= postInfo
                else :
                    comments.append(info)
                #print '--------------------------------'
                
            res['comments'] = comments
            #print res
            
        except Exception, e:
            print e.message;
            tb = traceback.format_exc()
            print tb
            pass
        return res
    
    
if __name__ == '__main__':
    
    obj = webtretho_com()
    
    # test get topics
    #obj.getAllTopics()
    
    # test get all thread in topic
    topicUrl  = 'http://www.webtretho.com/forum/f2120/'
    obj.getThreadsInTopic(topicUrl)

    '''
    # test check total page in thread
    url = 'http://www.webtretho.com/forum/f3267/chi-dich-danh-72-thuc-pham-giam-can-doc-hai-1736763/'
    #url = 'http://www.webtretho.com/forum/f171/min-oi-mo-khoa-nick-gium-to-duoc-khong-1263996/'
    obj.getPagesInThread(url)
    '''
    
    '''
    # test parse thread
    url = 'http://www.webtretho.com/forum/f3267/chi-dich-danh-72-thuc-pham-giam-can-doc-hai-1736763/'
    url = 'http://www.webtretho.com/forum/f3267/chi-dich-danh-72-thuc-pham-giam-can-doc-hai-1736763/'
    obj.getThreadDetail(url)
    '''
    
    '''
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
    '''
    
    url = 'http://www.webtretho.com/forum/f3775/chong-doi-lay-vo-khac-khi-da-co-3-dua-con-phai-lam-sao-1855059/'
    obj.getThreadDetail(url)
    print '=========  DONE  =========='
