# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

class PloneboardNotificationSystemView(BrowserView):
    """View for the form that dump contents in a valid FSS format onto server filesystem"""
    
    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        request.set('disable_border', True)
    
    