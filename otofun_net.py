# -*- coding: utf-8 -*-
'''
Created on Mar 10, 2014

@author: kimphuc
'''
from utils.Request import Request
from bs4 import BeautifulSoup
import time
import re

class otofun_net(object):
    '''
    classdocs
    '''
    COUNT_TOPIC = 0
    baseUrl  ='http://www.otofun.net/'
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
        
    def getThreadsInTopic(self, topicUrl):
        '''
        Get all threads in a topic
        '''

        res = {}
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
                    print 'Thread ',tUrl
                    print tLink.string
                    print '==========================='
                    # self.getThreadDetail(tUrl)
                    self.COUNT_TOPIC += 1
                    print 'Topic number: ', self.COUNT_TOPIC
                    time.sleep(1)
                print '-----------'

        #find sub-topic
        topics = soup.find('ol', {'class' : 'subforumlist'})
        if topics:
            for topic in topics.findAll('li', {'class' : 'subforum'}):
                tLink = topic.find('a')
                if (tLink) :
                    tUrl  = tLink['href']
                    if 'http://' not in tUrl:
                        tUrl = self.baseUrl + tUrl
                    print 'Topic Level-2 ', tUrl
                    print tLink.string
                    self.getThreadsInTopic(tUrl)
                print '-----------'
        return res

    def writeFile(self, filename, data):
        file_doc = open(filename, 'w')
        file_doc.write(data.encode('utf-8'))
        file_doc.close()

    def getThreadDetail(self, url):

        res = ()
        html = ''
        try:
            html = Request.get_page_content(url);
        except Exception, e:
            return None
        soup = BeautifulSoup(html)
        threadTitle = soup.find('span', {'class' : 'threadtitle'}).get_text()
        #print threadTitle
        #print '============================='
        
        htmlPosts = soup.find('ol', {'id' : 'posts'})
        posts = htmlPosts.findAll('li', {'class' : 'postbit postbitim postcontainer'})
        #print posts
        fileContent = u"<topic>\n"
        count = 0
        for post in posts:
            p = {}
            count += 1
            if (count == 1):
                title = post.find('div', {'class' : 'postrow'}).find('h2').get_text()
                title = title.strip()
                print '------------------'
                fileContent += u"\t<post>\n\t\t<title>" + title + "</title>"
            else:
                fileContent += u"\t<comment>"
                
            userName = post.find('div', {'class': 'username_container'}).find('a').find('strong').get_text()
            #print userName
            #print unicode.encode(userName, 'utf-8')
            
            date = post.find('div', {'class' : 'posthead'}).find('span', {'class' : 'date'}).get_text()
            #print date
            #print unicode.encode(date, 'utf-8')
            #print repr(date)
            

            content = post.find('div', {'class' : 'content'}).find('blockquote').renderContents()
            content = re.sub('<[^<]+?>', '', content)
            content = re.sub('\[[^\[]+?\]', '', content)
            content = re.sub('[\r\n]+', '\n', content)
            content = re.sub('[\t]+', ' ', content)
            content = re.sub('  ', ' ', content)
            content = content.strip()
            fileContent += u"\n\t\t<datetime>"+date+"</datetime>\n\t\t<username>"+userName+"</username>\n\t\t<content>"+content.decode('utf8')+"</content>\n"

            if (count == 1):
                fileContent += u"\t</post>\n"
            else:
                fileContent += u"\t</comment>\n"
            #print post.select('div  div  .content blockquote')[0]
            #print content
            #print post
        #return res
        fileContent += u"</topic>"
        filename = 'data/topic-' + str(self.COUNT_TOPIC).zfill(6) + '.xml'
        self.writeFile(filename, fileContent)
        self.COUNT_TOPIC += 1
        # print fileContent
        print '---------------------------'
        # print ' '
        print ' '
        print 'Topic number: ', self.COUNT_TOPIC

    

if __name__ == '__main__':
    obj = otofun_net()
    #links = obj.getAllTopics()
    #for link in links:
    #    print link
    
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
        
    #url = 'http://www.otofun.net/threads/531610-thong-tin-ve-viec-vinh-danh-cac-thanh-vien-of-co-cac-dong-gop-dac-biet'
    #url = 'http://www.otofun.net/threads/644366-nhung-chiec-suv-dang-mua-nhat'    
    #obj.getThreadDetail(url)
            
