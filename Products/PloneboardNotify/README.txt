Use of PloneboardNotify
=======================

Welcome to the guide of the use of PloneboardNotify.
We need to setup something before this file can became a real and working browser test for Plone.

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()
    >>> self.portal.error_log._ignored_exceptions = ()
    >>> from Products.PloneTestCase.setup import portal_owner, default_password

Ok, now we are ready to load the Plone site where this product is installed.
Now we need to login and begin with creation of some forum.

    >>> browser.open(portal_url+'/login_form')
    >>> browser.getControl('Login Name').value = 'root'
    >>> browser.getControl('Password').value = 'secret'
    >>> browser.getControl('Log in').click()
    >>> 'You are now logged in' in browser.contents
    True

Ok, now let's create our first forum area.

    >>> browser.open(portal_url)
    >>> browser.getLink('Message Board').click()
    >>> browser.getControl('Title').value = 'Our forums'
    >>> browser.getControl('Save').click()

Inside the *Message Board* we can add multiple forums. We start with one for now.

    >>> browser.getLink('Add Forum').click()
    >>> browser.getControl('Title').value = 'Cool Music'
    >>> browser.getControl('Save').click()
    >>> portal_url+'/our-forums/cool-music' in browser.url
    True

Now we can go to the "*Ploneboard notification system *".

    >>> # I go directly to the form due to an HTTP 500 error running test on Plone 2.5
    >>> browser.open(portal_url+'/@@ploneboard_notification')
    >>> 'Ploneboard notifications' in browser.contents
    True


