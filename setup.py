from setuptools import setup, find_packages
import os

version = '0.4.0'

tests_require=['zope.testing']

setup(name='Products.PloneboardNotify',
      version=version,
      description="A configurable Plone product for sending e-mails when new message is added on Ploneboard forum",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='ploneboard forum notify email',
      author='keul',
      author_email='luca.fabbri@redturtle.net',
      url='http://svn.plone.org/svn/collective/Products.PloneboardNotify',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.Ploneboard',
          # -*- Extra requirements: -*-
      ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'Products.PloneboardNotify.tests.test_doctest.test_suite',
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      paster_plugins = ["ZopeSkel"],
      )
