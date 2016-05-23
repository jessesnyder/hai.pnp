import unittest
from DateTime import DateTime
from zope.component import getMultiAdapter
from zope.interface import alsoProvides

from hai.pnp.tests.base import TestCase
from hai.pnp import interfaces

class TestBaseView(TestCase):
    
    def afterSetUp(self):
        self.viewname = 'metadata-view'
        self.setRoles(('Manager',))
        self.folder.invokeFactory("Policy", "policy")
        self.policy = self.folder.policy
        self.policy.setFunctionalAreaCode = 'foo'
        self.policy.setTheatreOfOpsCode = 'foo'
        self.yesterday = DateTime() - 1
        self.policy.setActiveDate(self.yesterday)
        self.policy.setContact('foo')
        alsoProvides(self.app.REQUEST, interfaces.IHAIPolicyProcedureLayer)
    
    def test_view_available(self):
        view = getMultiAdapter((self.policy, self.app.REQUEST), name=self.viewname)
        self.failUnless(view is not None)
    

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
