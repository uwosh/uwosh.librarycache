from zope.interface import Interface, implements
from zope.component import adapts

class ICachable(Interface):
    """ Adapter Interface """
    
class ICacheMarker(Interface):
    """ Marker Interface """
    

class CacheMarker(object):
    implements(ICacheMarker)
    """ Adapter Marker """

class CacheCore(object):
    implements(ICachable)
    adapts(ICacheMarker)
    
    def __init__(self,context):
        """ Sets up context so it is transparent. """
        self.context = context
    
    def setContext(self,context):
        self.context = context

    def build(self):
        """ Method must be implemented in extending class """
        raise Exception('Must be implemented')