# -*- coding: utf-8 -*-


import traceback    # trace the errors

from time import sleep

import Queue
import threading

# time_out --> can co cach reload tu dong
CONFIG = [
    {'site_name' : 'webtretho.com', 'class_name' : 'webtretho_com', 'time_out': 60}
    ,{'site_name' : 'lamchame.com', 'class_name' : 'lamchame_com', 'time_out': 60}
    ,{'site_name' : 'otofun.net', 'class_name' : 'otofun_net', 'time_out': 60}
    ]

#define a worker function --> process data from each site
def worker(queue):
    queue_full = True
    while queue_full:
        try:
            #get your data off the queue, and do some work
            site = queue.get(False)
            objectName =  site['class_name']
            print objectName
            sleep(1)
            try :
                commandImport = "from sites." + objectName + " import " + objectName
                commandInit = objectName + "()"
                exec commandImport
                #print 'Excecute: ' + commandImport
                #sleep(1)
                
                siteObj = eval(commandInit)
                #print 'Init object: '
                #print siteObj
                #sleep(1)
                
                topics = siteObj.getAllTopics()
                for topic in topics:
                    print 'TOPIC: ', topic
                    print '==============='
                    
                    # get total papge in each topic
                    #totalPageInTopic = siteObj.getTotalPageInTopic(topic)
                    #print 'Total page in topic: ', totalPageInTopic
                    #sleep(1)
                    topicPages = siteObj.getPagesInTopic(topic)
                    sleep(1)
                    
                    for topicPage in topicPages:
                        print 'TOPIC PAGE: ', topicPage
                        print '--------'
                        sleep(1)
                        
                        threads = siteObj.getThreadsInTopic(topicPage)
                        for thread in threads:
                            print 'Thread: ', thread                            
                            detail = siteObj.getThreadDetail(thread)
                            print "DETAIL: ", detail
                            print '--------------'
                            sleep(1)
                                                
                    
                #content = site_obj.refine_content(content)
                #return content
            except Exception:
                tb = traceback.format_exc()
                print tb
                #logger.error(tb)            
                #logger.fatal("Co loi khi import: " + object_name)
                
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
    print 'done'
        
