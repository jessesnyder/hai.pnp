# -*- coding: utf-8 -*-

import unittest
from Products.CMFCore.utils import getToolByName

from hai.pnp.tests.base import TestCase
from hai.pnp import interfaces

class TestIDGeneration(TestCase):
    
    def afterSetUp(self):
        self.setRoles(['Manager',])
        self.portal_workflow = getToolByName(self.portal, 'portal_workflow')
        self.folder.invokeFactory("Policy", "policy")
        self.policy = self.folder.policy
        self.policy.invokeFactory("Procedure", "procedure")
        self.procedure = self.policy.procedure
        self.procedure.invokeFactory("Form", "form")
        self.form = self.procedure.form
        self.form.invokeFactory('Howto', 'howto')
        self.howto = self.form.howto
        self.objectset = (self.policy, self.procedure, self.form, self.howto)
    
    def beforeTearDown(self):
        pass

    def test_custom_ids(self):
        for obj in self.objectset:
            obj.setTitle(unicode("My's Fañcy Title", 'utf-8'))
            obj.setTheatreOfOpsCode('SEA')
            obj.setFunctionalAreaCode('IST')
            ptype = obj.portal_type
            obj._renameAfterCreation()
            self.assertEqual('SEA-IST-%s-MysFancyTitle' % ptype, 
                    obj.getId())
    
    def test_approvedBy(self):
        self.portal_workflow.doActionFor(self.policy, 'make_provisional')
        self.assertEqual('', self.policy.approvedBy())
        self.portal_workflow.doActionFor(self.policy, 'make_official')
        self.assertEqual('test_user_1_', self.policy.approvedBy())
        
    def test_interface(self):
        for obj in self.objectset:
            self.failUnless(interfaces.IPolicyProcedure.providedBy(obj))
    
    def test_schema_fields(self):
        schema = self.policy.Schema()
        base_fields = ('theatreOfOpsCode', 
                       'functionalAreaCode', 
                       'contact', 
                       'activeDate')
        for addl_field in base_fields:
            self.failUnless(addl_field in schema,
                'Schema %s missing %s after marker interface applied' 
                    % (schema, addl_field))        

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
