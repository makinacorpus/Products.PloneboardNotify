Use of PloneboardNotify
=======================

We need to setup something before this file can became a real and working browser test for Plone.

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()
    >>> self.portal.error_log._ignored_exceptions = ()
    >>> from Products.PloneTestCase.setup import portal_owner, default_password


Configuration
-------------

To test later e-mail system, we put the notification in *debug mode*, so no real mail will be sent
but only printed to standard output.

    >>> self.portal.portal_properties.ploneboard_notify_properties.debug_mode = True

Now we are ready to load the Plone site where the product is installed.
We need to login before beeing able to start with creation of a forum.

    >>> browser.open(portal_url+'/login_form')
    >>> browser.getControl('Login Name').value = 'root'
    >>> browser.getControl('Password').value = 'secret'
    >>> browser.getControl('Log in').click()
    >>> 'You are now logged in' in browser.contents
    True

Let's create our first forum area.

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

To begin our tests we set a couple of e-mail address in the "Recipients" section. We can use here
the "*|bcc*" decoration after every value, to add the message to this recipients in *BCC*. 

    >>> browser.getControl('Recipients').value = """usera@mysite.org
    ... userb@mysite.org
    ... userc@mysite.org|bcc"""
    >>> browser.getControl('Save').click()

We used the "*General notify configuration*" section, so an e-mail will be delivered to all address
at every new message or discussion everywhere in the site. The last address is used for *BCC* section.


Using Ploneboard
----------------

Now we can go back to our forum and begin a new discussion.

    >>> browser.open(portal_url+'/our-forums/cool-music')
    >>> browser.getControl('Start a new Conversation').click()
    >>> browser.getControl('Title').value = 'Discussion 1'
    >>> browser.getControl('Body text').value = '<p>The <strong>cat</strong> is on the table</p>'

As soon as we confirm the post, an e-mail will be generated.

    >>> browser.getControl('Post comment').click()
    Message subject: New comment added on the forum: Cool Music
    Message text:
    <html>
    <body>
    <p>Message added by: The Admin</p>
    <BLANKLINE>
    <p>Argument is: Discussion 1</p>
    <p>The new message is:</p>
    <p>The <strong>cat</strong> is on the table</p>
    <BLANKLINE>
    <hr/>
    <p><a href="http://nohost/plone/our-forums/cool-music/...">http://nohost/plone/our-forums/cool-music/...</a></p>
    </body>
    </html>
    <BLANKLINE>
    Message sent to userb@mysite.org, usera@mysite.org (and to userc@mysite.org in bcc)

A similar message will be delivered also if the user add a response to an existing discussion.
First we need to go to the discussion itself, after that we can use the "Reply to this" command.

    >>> browser.getLink('Discussion 1').click()
    >>> browser.getControl('Reply to this', index=0).click()

Ploneabord quote text inserted before when replying, so we keep the text and add a new comment.

    >>> browser.getControl('Body text').value = browser.getControl('Body text').value + \
    ...                                         "\n<p>I don't think so. He is <em>under</em> it</p>"

Now posting this will generate a new e-mail.

    >>> browser.getControl('Post comment').click()
    Message subject: New comment added on the forum: Cool Music
    Message text:
    <html>
    <body>
    <p>Message added by: The Admin</p>
    <BLANKLINE>
    <p>Argument is: Discussion 1</p>
    <p>The new message is:</p>
    ...
    <p>I don't think so. He is <em>under</em> it</p>
    <BLANKLINE>
    <hr/>
    <p><a href="http://nohost/plone/our-forums/cool-music/...">http://nohost/plone/our-forums/cool-music/...</a></p>
    </body>
    </html>
    <BLANKLINE>
    Message sent to userb@mysite.org, usera@mysite.org (and to userc@mysite.org in bcc)

The e-mail structure is the same (the quoted text is optional as the commenter can remove it).

Play with users of the portal
-----------------------------

PloneboardNotify can also use e-mail address taken from the portal users. Use of e-mail address or user ids
can be combined, also with the *BCC* feature.

Let's we change something in the configuration.

    >>> browser.open(portal_url+'/@@ploneboard_notification')
    >>> browser.getControl('Recipients').value = """usera@mysite.org
    ... root|bcc
    ... member"""
    >>> browser.getControl('Save').click()

We added the *root* user in *BCC* and also another simple member (called *member*). To test this we can
go back to our forum and add another conversation.

    >>> browser.open(portal_url+'/our-forums/cool-music')
    >>> browser.getControl('Start a new Conversation').click()
    >>> browser.getControl('Title').value = 'Discussion 2'
    >>> browser.getControl('Body text').value = '<p>I will not fear</p>'

Let's see what result will be generated.

    >>> browser.getControl('Post comment').click()
    Message subject: New comment added on the forum: Cool Music
    Message text:
    <html>
    <body>
    <p>Message added by: The Admin</p>
    <BLANKLINE>
    <p>Argument is: Discussion 2</p>
    <p>The new message is:</p>
    <p>I will not fear</p>
    <BLANKLINE>
    <hr/>
    <p><a href="http://nohost/plone/our-forums/cool-music/...">http://nohost/plone/our-forums/cool-music/...</a></p>
    </body>
    </html>
    <BLANKLINE>
    Message sent to user@mysite.org, usera@mysite.org (and to admin@mysite.org in bcc)

Another option available in the configuration panel is a control to send notification to *all* users of
the site. This can be very helpful if the site is mainly a forum resource (but can also became a nasty
spam source!).

For privacy reason, when using this feature all e-mail will be delivered using *BCC*.

    >>> browser.open(portal_url+'/@@ploneboard_notification')
    >>> browser.getControl('Send to all?').click()
    >>> browser.getControl('Save').click()

To test what is changed right now we will add a response to the discussion above.

    >>> browser.open(portal_url+'/our-forums/cool-music')
    >>> browser.getLink('Discussion 2').click()
    >>> browser.getControl('Reply to this', index=0).click()
    >>> browser.getControl('Body text').value = "Fear is the mind-killer"
    >>> browser.getControl('Post comment').click()
    Message subject: New comment added on the forum: Cool Music
    Message text:
    <html>
    <body>
    <p>Message added by: The Admin</p>
    <BLANKLINE>
    <p>Argument is: Discussion 2</p>
    <p>The new message is:</p>
    Fear is the mind-killer
    <BLANKLINE>
    <hr/>
    <p><a href="http://nohost/plone/our-forums/cool-music/...">http://nohost/plone/our-forums/cool-music/...</a></p>
    </body>
    </html>
    <BLANKLINE>
    Message sent to usera@mysite.org (and to admin@mysite.org, user@mysite.org, another@mysite.org in bcc)

Please note that the e-mail "*usera@mysite.org*" is still included as before.


Manage notification for a single forum
--------------------------------------

If our Plone site keep a lot of message boards and/or a lot of forums (even if inside the same board),
the global notification preference can be difficult to be managed.

Maybe we need to notify all users of the portal for a single (public) forum, but notify only some special
members for one or more private forums, and different forum may need different notification address
group...

All those needs can be reached configuring the notification also for a forum instead of using the global
notification setting we used.
In facts the global notification settings can be ignored and never used.

We can manage the per-forum configuration going back to the "Ploneboard notification" panel.

    >>> browser.open(portal_url+'/@@ploneboard_notification')

There, we will see all message boards and all forums inside them. Forum that have already a local settings
are marked with a special image.

Let's change the notification settings adding a local preference for our "*Cool Music*" forum.

    >>> browser.getLink('Cool Music').click()
    >>> 'Ploneboard notifications - Cool Music' in browser.contents
    True

The options there are the same used in global configuration. We can here change (and this time, only for
the "*Cool Music*" forum the notification settings.

Let's make this forum send notification only to a webmaster address.

    >>> browser.getControl('Recipients').value = 'webmaster@mysite.org'
    >>> browser.getControl('Save').click()
    >>> browser.url == portal_url+"/our-forums/cool-music/@@ploneboard_notification"
    True
    >>> browser.getControl('Recipients').value
    'webmaster@mysite.org'

Now we simply need to see what is changed, starting a new discussion inside our forum.

    >>> browser.open(portal_url+'/our-forums/cool-music')
    >>> browser.getControl('Start a new Conversation').click()
    >>> browser.getControl('Title').value = "Talking to webmaster"
    >>> browser.getControl('Body text').value = "<p>This will be sent only to Webmaster!</p>"
    >>> browser.getControl('Post comment').click()
    Message subject: New comment added on the forum: Cool Music
    Message text:
    <html>
    <body>
    <p>Message added by: The Admin</p>
    <BLANKLINE>
    <p>Argument is: Talking to webmaster</p>
    <p>The new message is:</p>
    <p>This will be sent only to Webmaster!</p>
    <BLANKLINE>
    <hr/>
    <p><a href="http://nohost/plone/our-forums/cool-music/...">http://nohost/plone/our-forums/cool-music/...</a></p>
    </body>
    </html>
    <BLANKLINE>
    Message sent to webmaster@mysite.org (and to no-one in bcc)

We can see that no global setting has been taken there. This forum now lives on his own.


Handle Kupu/TinyMCE internal links
----------------------------------

todo