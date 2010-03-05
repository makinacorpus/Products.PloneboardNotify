Use of PloneboardNotify
=======================

Welcome to the guide of the use of PloneboardNotify.
We need to setup something before this file can became a real and working browser test for Plone.

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()
    >>> self.portal.error_log._ignored_exceptions = ()
    >>> from Products.PloneTestCase.setup import portal_owner, default_password

To test later e-mail system, we put the notification in *debug mode*, so no real mail will be sent
but only printed to standard output.

    >>> self.portal.portal_properties.ploneboard_notify_properties.debug_mode = True

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

    >>> # browser.getLink('Site Setup').click()
    >>> # browser.getLink('Ploneboard notification system').click()    
    >>> # I go directly to the form due to an HTTP 500 error running test on Plone 2.5
    >>> browser.open(portal_url+'/@@ploneboard_notification')
    >>> 'Ploneboard notifications' in browser.contents
    True

To begin our test we set a couple of email address in the "Recipients" section. We can use here
the "*|bcc*" decoration after every value, to add the message to this recipient in *BCC*. 

    >>> browser.getControl('Recipients').value = 'usera@mysite.org\n'
    ...                                          'userb@mysite.org|bcc'

We used the "*General notify configuration*" section, so a mail will be delivered to both address
at every new message or discussion in the site.

Now we can go back to our forum and begin a new discussion.

    >>> browser.open(portal_url+'/our-forums/cool-music')
    >>> browser.getControl('Start a new Conversation').click()
    >>> browser.getControl('Title').value = 'Discussion 1'
    >>> browser.getControl('Body text').value = '<p>The <strong>cat</strong> is on the table</p>'
    >>> browser.getControl('Post comment').click()

  
