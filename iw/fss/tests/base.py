# -*- coding: utf-8 -*-
# Copyright (c) 2008 Ingeniweb

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING. If not, write to the
# Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

# $Id$

"""Defines a test class and its Plone Site layer for plone tests"""

import os

from Testing import ZopeTestCase as ztc

from zope.interface import classImplements
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.CMFPlone.Portal import PloneSite
from Products.CMFPlone.interfaces import ITestCasePloneSiteRoot
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup

import iw.fss
from iw.fss.config import INSTALL_EXAMPLE_TYPES_ENVIRONMENT_VARIABLE

# Install FSS Example types
os.environ[INSTALL_EXAMPLE_TYPES_ENVIRONMENT_VARIABLE] = 'True'

# Make the test fixture extension profile active
classImplements(PloneSite, ITestCasePloneSiteRoot)

@onsetup
def setup_fss():
    """Set up the additional products required for fss.

    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer.
    """
    ztc.installPackage('iw.fss')

# setting up plone site
setup_fss()
ptc.setupPloneSite(products=['iw.fss'],
                   extension_profiles=['iw.fss:iw.fss.testfixtures'])

# fake mailhost
from Products.MailHost import MailHost

class TestMailHost(MailHost.MailHost):

    def _send(self, mfrom, mto, messageText ):
        """Fake sender"""
        print messageText

class TestCase(ptc.FunctionalTestCase):
    """test case used in tests"""

    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml', iw.fss)
            fiveconfigure.debug_mode = False
            cls._old = MailHost.MailHost
            MailHost.MailHost = TestMailHost

        @classmethod
        def tearDown(cls):
            MailHost.MailHost = cls._old