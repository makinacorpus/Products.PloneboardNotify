# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from Products.Ploneboard.interfaces import IPloneboard
from Products.PloneboardNotify.interfaces import ILocalBoardNotify

class PloneboardNotificationSystemView(BrowserView):
    """View for the form that dump contents in a valid FSS format onto server filesystem"""
    
    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        request.set('disable_border', True)
    
    @property
    def portal_boards(self):
        """Perform a catalog search for all ploneboard objects in the portal"""
        catalog = getToolByName(self.context, 'portal_catalog')
        return catalog(object_provides=IPloneboard.__identifier__)
        