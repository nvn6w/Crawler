# -*- coding: utf-8 -*-


import traceback    # trace the errors

from time import sleep

import Queue
import threading
from utils.RedisQueue import RedisQueue
import json
import redis

# time_out --> can co cach reload tu dong
CONFIG = [
    {'site_name' : 'webtretho.com', 'class_name' : 'webtretho_com'}
    ,{'site_name' : 'lamchame.com', 'class_name' : 'lamchame_com'}
    ,{'site_name' : 'otofun.net', 'class_name' : 'otofun_net'}
    ]
DOWNLOAD_QUEUE = RedisQueue('DOWNLOAD', 'forum')

rc = redis.Redis()  # init redis client

#define a worker function --> process data from each site
def worker(queue):
    queue_full = True
    FINISHED = False
    
    while not FINISHED:
        try:
            #get your data off the queue, and do some work
            site = queue.get(False)
            objectName =  site['class_name']
            #print threading.current_thread().getName()
            sleep(1)
            try :
                commandImport = "from sites." + objectName + " import " + objectName
                commandInit = objectName + "()"
                exec commandImport                
                siteObj = eval(commandInit)
                                
                topics = siteObj.getAllTopics()
                for topic in topics:
                    postCounter = rc.get("forum:post_counter") # get total post and comment
                    if postCounter and (int(postCounter) > 1000000):
                        print 'Finish 1M Post!'
                        FINISHED = True
                        break
                        
                    print threading.current_thread().getName() , ' : TOPIC: ', topic
                    print '==============='
                    
                    topicPages = siteObj.getPagesInTopic(topic)
                    sleep(1)
                    
                    for topicPage in topicPages:
                        postCounter = rc.get("forum:post_counter") # get total post and comment
                        if postCounter and (int(postCounter) > 1000000):
                            print 'Finish 1M Post!'
                            FINISHED = True   
                            break               
                        print threading.current_thread().getName() , ' : TOPIC PAGE: ', topicPage
                        print '--------'
                        sleep(1)
                        
                        threads = siteObj.getThreadsInTopic(topicPage)
                        for thread in threads:
                            info = json.dumps({'class_name' : objectName, 'url' : thread})
                            DOWNLOAD_QUEUE.put(info)
                            print threading.current_thread().getName() , ' : Thread: ', thread                                                        
                            print '--------------'
                            sleep(1)                                            
            except Exception:
                tb = traceback.format_exc()
                print tb
                
        except Queue.Empty:
            queue_full = False            

if __name__ == '__main__':

    #load up a queue with your data, this will handle locking
    queueSites = Queue.Queue()
        
    for site in CONFIG:
        #put site --> queue
        queueSites.put(site)        

    #create as many thread as total site from config
    threadCount = len(CONFIG)
    for i in range(threadCount):
        t = threading.Thread(target=worker, args = (queueSites,))
        t.start()
        
