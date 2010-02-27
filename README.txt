What is this?
=============

An event based Plone product.
Add some configuration to your Plone site for sending email on new messages or replies
added on forums.

You also need `Ploneboard`__ product to be installed.

__ http://pypi.python.org/pypi/Products.Ploneboard

Tested on
---------

* Plone 3.3 (Ploneboard 2.1)

Plone 2.5 no more?
------------------

Maybe that also this release works on Plone 2.5, but I'm not testing on it anymore. If you need it,
please use older version like `PloneboardNotify 0.3`__

__ http://pypi.python.org/pypi/Products.PloneboardNotify/0.3.0beta

Thanks to
---------

* **Nicolas Laurance** for giving french translation and for helping adding other features.

TODO
----

* Current version support global configuration and forum specific ones; the long-term
  plan wanna reach also forum area configurations.
* Also manipulate the FROM part of the mail, configurable globally, for single forum, etc.
* Forum outside the Forum Area are not supported by the configuration UI.
* Add user info to notification?
* A complete, clean uninstall procedure that remove all unwanted stuff.

