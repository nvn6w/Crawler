'''
Created on May 28, 2014

@author: kimphuc
'''
from abc import ABCMeta, abstractmethod

class ISite(object):
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def getAllTopics(self):        
        pass
    
    @abstractmethod
    def getPagesInTopic(self, topicUrl):
        pass
    
    @abstractmethod
    def getThreadDetail(self, threadUrl):
        pass    
    