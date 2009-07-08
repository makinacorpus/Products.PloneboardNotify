# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile # Plone 2.5 compatibility
from Products.CMFCore.utils import getToolByName

from Products.Ploneboard.interfaces import IPloneboard, IForum
from Products.PloneboardNotify.interfaces import ILocalBoardNotify

class PloneboardNotificationSystemView(BrowserView):
    """View for managing Ploneboard notification system in control panel"""
    
    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        request.set('disable_border', True)
        
    def __call__(self):
        request = self.request
        if request.form.get("pbn_save"):
            self._updateConfiguration(request.form)
            request.response.redirect(self.context.absolute_url()+"/@@ploneboard_notification")
        return self.template()
    
    template = ZopeTwoPageTemplateFile("ploneboard_notification_forum.pt")

    def _updateConfiguration(self, form):
        """Update saved configuration data"""
        context = self.context
        forum_sendto_values = context.getProperty('forum_sendto_values', [])
        sendto_values = [x.strip() for x in form.get("sendto_values").replace("\r","").split("\n") if x]
        # An empty value remove the property AND the provided interface

    def load_sendto_values(self):
        """Load the local forum_sendto_values value"""
        context = self.context
        return "\n".join(context.getProperty('forum_sendto_values', []))



