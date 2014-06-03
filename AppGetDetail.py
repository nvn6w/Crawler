# -*- coding: utf-8 -*-
'''
Created on Jun 1, 2014

@author: kimphuc
'''
import os
import socket
from utils.RedisQueue import RedisQueue
from time import sleep
import redis
import json
import Config

CRAWLED_URL = RedisQueue('CRAWLED_URL', 'forum')
DOWNLOAD_QUEUE = RedisQueue('DOWNLOAD', 'forum')

rc = redis.Redis()
 
def getWorkerName():
    return socket.gethostname() + '_' +  str(os.getpid())

def getFolder(index):
    index = int(index)
    folder = index/500  # 500 file per folder    
    fullPath = Config.DATA_DIR + str(folder).zfill(3) + '/'
    d = os.path.dirname(fullPath)
    if not os.path.exists(d):
        os.makedirs(d)
    return fullPath

def writeThread(threadDetail, cur):
    folder = getFolder(cur)
    
    xml = '<topic>\n'
    if 'post' in threadDetail:
        postInfo = threadDetail['post']
        post = '<post>\n'
        post += '\t<topic-title>' + postInfo['title'] + '</topic-title>\n'
        post += '\t<user-name>' + postInfo['user'] + '</user-name>\n'
        post += '\t<date-time>' + postInfo['date'] + '</date-time>\n'
        post += '\t<post-content>' + postInfo['content'] + '</post-content>\n'
        post += '</post>\n'
        xml += post
        rc.incr("forum:post_counter")
    if 'comments' in threadDetail:
        comments = threadDetail['comments']
        for c in comments:
            comment = '<comment>\n'
            comment += '\t<user-name>' + c['user'] + '</user-name>\n'
            comment += '\t<date-time>' + c['date'] + '</date-time>\n'
            comment += '\t<comment-content>' + c['content'] + '</comment-content>\n'
            comment += '</comment>\n'
            xml += comment
            rc.incr("forum:post_counter")
    xml += '</topic>'
    file = folder + str(cur).zfill(3) + '.xml'
    f = open(file, 'w')
    f.write(xml.encode('utf-8'))
    f.close()
    print 'Write --> ' + file

if __name__ == '__main__':
    workerName = getWorkerName()
    rc = redis.Redis()
    FINISHED  = False
    
    while not DOWNLOAD_QUEUE.empty() and not FINISHED:     
        postCounter = rc.get("forum:post_counter") # get total post and comment
        if postCounter and (int(postCounter) > 115):
            print 'Finish 1M Post!'
            FINISHED = True
            break
           
        threadInfo = json.loads(DOWNLOAD_QUEUE.get(True, workerName, 0))
        threadUrl = threadInfo['url'].encode('utf-8')
        try :
            
            className = threadInfo['class_name']
            objectName =  className
            commandImport = "from sites." + className + " import " + className
            commandInit = objectName + "()"
            exec commandImport                
            siteObj = eval(commandInit)
            
            threadDetail = siteObj.getThreadDetail(threadUrl)
            if threadDetail:                
                CRAWLED_URL.put(threadUrl)
                cur = rc.incr("forum:thread_counter"); # increase thread counter                
                writeThread(threadDetail, cur)                                
        except:
            print 'Error --> fetch URL : ', threadUrl
            pass
        print 'Thread URL: ', threadUrl
        print '-------------------------'
        sleep(1)
        
    
    # Delete temp queue of this worker
    DOWNLOAD_QUEUE.delete(workerName)
    print 'Done'