What is this?
=============

An event based Plone product.
Add some configuration to your Plone site for sending e-mail on new messages or replies
added on forums.

You also need `Ploneboard`__ product to be installed.

__ http://pypi.python.org/pypi/Products.Ploneboard

Tested on
---------

* Plone 2.5 (Ploneboard 1.0)
* Plone 3.3 (Ploneboard 2.1)

Plone 2.5: still live
---------------------

Yes, this is done to be compatible with Plone 2.5 and older versions of Ploneboard.
To install this for Plone 2.5 just copy the *PloneboardNotify* directory in the *Products* directory
provided by older Zope releases.

**Please note** that you need `Five`__ 1.4 to run tests on Plone 2.5.

__ http://codespeak.net/z3/five/release/

Thanks to
---------

* **Nicolas Laurance** for giving french translation and for helping adding HTML e-mail feature.

TODO and know issues
--------------------

* Current version support global configuration and forum specific ones; the long-term
  plan wanna reach also forum area configurations
* Also manipulate the FROM part of the mail, configurable globally, for single forum, etc
* A complete, clean uninstall procedure that remove all unwanted stuff
* Give a simple way to manipulate the notification message format
* Not able to send HTML e-mail with Plone 2.5... to be fixed

