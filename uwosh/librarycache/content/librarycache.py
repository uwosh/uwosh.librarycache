#from zope import schema 
#from zope.app.container.constraints import contains
#from zope.app.container.constraints import containers

from zope.interface import implements, directlyProvides, Interface
from Products.Archetypes import atapi
from Products.ATContentTypes.content import base, folder, schemata
from Products.Archetypes.atapi import SelectionWidget,StringField

from Products.CMFCore.utils import getToolByName

from uwosh.librarycache import librarycacheMessageFactory as _
from uwosh.librarycache.config import PROJECTNAME

from Products.CMFCore.permissions import View
from AccessControl import ClassSecurityInfo

from zope.component import getAdapter
from uwosh.librarycache.core import CacheMarker,ICachable
from DateTime import DateTime

class ILibraryCache(Interface):
    """ Interface """
    

"""
This is a basic Content type, one field for Class Type Referencing.
"""
LibraryCacheSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((                                                        
                                                                         
        StringField('cacheReference',
            required=False,
            searchable=False,
            multiValued=False,
            mutator="setCacheReference",
            vocabulary="getCacheReferences",
            enforceVocabulary=True,
            widget = SelectionWidget(
                description = "Reference the Class location for your Cache Object.",
                label = _(u'Select Type of Cache', default=u'Select Type of Cache'),
                format="select",
            )),                                           
                                                               
))

LibraryCacheSchema['title'].storage = atapi.AnnotationStorage()
LibraryCacheSchema['description'].storage = atapi.AnnotationStorage()
LibraryCacheSchema['cacheReference'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(LibraryCacheSchema, moveDiscussion=False)


class LibraryCache(base.ATCTContent):
    """
    Library Cache ContentType.  This will adapt to any CacheCore Object and 
    store its content in this ContentType.
    
    See example.py to make your own adaptable object.
    
    @note: This is a cache, it will not have up-to-date results.  It is built once
    a day and this Object is used for storage.
    
    @author: David Hietpas
    @version: 1.1
    """
    
    
    implements(ILibraryCache)

    meta_type = "LibraryCache"
    schema = LibraryCacheSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    masterCache = None
    
    def getCacheReference(self):
        """
        Returns the cache Type.
        @return: String, representation of Class Type
        """
        return self.getField('cacheReference').get(self)
    
    def getCacheReferences(self):
        """
        Returns a list of possible cache Types that can be created.
        @return: List, of Class Type
        """
        props = getToolByName(self, "portal_properties")
        references = props.cache_objects.getProperty("cache_types")
        results = []
        for i in references:
            tup = str(i),str(i) # Setup Tuple.
            results.append(tup)
        return results
    
    def setCacheReference(self,value):
        """
        This sets the Class Type for this cache object.
        """
        if len(value) != 0:
            self.getField('cacheReference').set(self,value)
            self._buildCache(str(value))
    
    
    def rebuildCache(self):
        """
        This can be called at will to rebuild the cache at any time the user 
        wishes.  This can be called through Cron-Jobs or custom cache controls.
        """
        self._buildCache(self.getCacheReference())
    
    
    def _buildCache(self,type):
        """
        Builds Object to be stored in this Content Type.  Gets Adapter
        and sets the marker interfaces for calling the Objects factory.
        @param: type, is type of cache to be built.
        """
        marker = CacheMarker()
        adapter = getAdapter(marker,ICachable,name=unicode(type))
        adapter.setContext(self)
        self.setUpdateTime()
        self.masterCache = adapter.build()

    def getCache(self):
        """
        Returns LibraryCache Object for usage.
        @return: Object
        """
        return self.masterCache

    
    def getReference(self):
        """ Used for cataloging. """
        return self.getField('cacheReference').get(self)
     
    
    def setUpdateTime(self):
        """ String Representation for last time updated.  Good for noting Automated Updating """
        self.setModificationDate(DateTime())
        self.reindexObject()
        

atapi.registerType(LibraryCache, PROJECTNAME)