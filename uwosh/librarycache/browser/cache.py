
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.theme.interfaces import IDefaultPloneLayer

from operator import itemgetter

class ILibraryCacheMarker(Interface):
    """ Marker """

class LibraryCache(BrowserView):
    implements(IDefaultPloneLayer)
    template = ViewPageTemplateFile('templates/cache.pt')

    def __call__(self):
        if self.checkPermissions():
            return self.template()
        return ""
    
    def checkPermissions(self):
        if self.context.portal_membership.checkPermission('Modify portal content', self.context):
            return True
        return False

    def render(self):
        return self.template()
    
    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()
