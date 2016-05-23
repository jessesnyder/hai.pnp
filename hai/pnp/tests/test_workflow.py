import unittest
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException

from hai.pnp.tests.base import TestCase

class TestWorkflow(TestCase):

    def afterSetUp(self):
        self.setRoles(['Manager',])
        self.folder.invokeFactory("Policy", "policy")
        self.policy = self.folder.policy
        self.policy.invokeFactory("Procedure", "procedure")
        self.procedure = self.policy.procedure
        self.procedure.invokeFactory("Form", "form")
        self.form = self.procedure.form
        self.form.invokeFactory('Howto', 'howto')
        self.howto = self.form.howto
        self.objectset = (self.policy, self.procedure, self.form, self.howto)
        self.portal_workflow = getToolByName(self.portal, 'portal_workflow')

    def beforeTearDown(self):
        pass

    def test_initial_state(self):
        for obj in self.objectset:
            self.assertEqual(self.portal_workflow.getInfoFor(obj,
                                                'review_state'), 'draft')

    def test_transitions_from_draft(self):
        for obj in self.objectset:
            transitions = set([t['id'] for t in
                    self.portal_workflow.getTransitionsFor(obj)])
            intended = set(['make_provisional', 'make_official'])
            diff = intended.difference(transitions)
            self.failIf(diff, diff)

    def test_move_to_provisional(self):
        for obj in self.objectset:
            self.portal_workflow.doActionFor(obj, 'make_provisional')
            self.assertEqual(self.portal_workflow.getInfoFor(obj,
                                'review_state'), 'provisional')
            transitions = set([t['id'] for t in
                    self.portal_workflow.getTransitionsFor(obj)])
            intended = set(['make_draft', 'make_official', 'retire'])
            diff = intended.difference(transitions)
            self.failIf(diff, diff)

    def test_move_to_official(self):
        for obj in self.objectset:
            self.portal_workflow.doActionFor(obj, 'make_provisional')
            self.portal_workflow.doActionFor(obj, 'make_official')
            self.assertEqual(self.portal_workflow.getInfoFor(obj,
                                'review_state'), 'official')
            transitions = set([t['id'] for t in
                    self.portal_workflow.getTransitionsFor(obj)])
            intended = set(['make_draft', 'make_provisional',
                            'deprecate', 'retire'])
            diff = intended.difference(transitions)
            self.failIf(diff, diff)

    def test_move_to_deprecated(self):
        for obj in self.objectset:
            self.portal_workflow.doActionFor(obj, 'make_provisional')
            self.portal_workflow.doActionFor(obj, 'make_official')
            self.portal_workflow.doActionFor(obj, 'deprecate')
            self.assertEqual(self.portal_workflow.getInfoFor(obj,
                                'review_state'), 'deprecated')
            transitions = set([t['id'] for t in
                    self.portal_workflow.getTransitionsFor(obj)])
            intended = set(['make_official', 'make_provisional', 'retire'])
            diff = intended.difference(transitions)
            self.failIf(diff, diff)

    def test_move_to_retired(self):
        for obj in self.objectset:
            self.portal_workflow.doActionFor(obj, 'make_provisional')
            self.portal_workflow.doActionFor(obj, 'make_official')
            self.portal_workflow.doActionFor(obj, 'deprecate')
            self.portal_workflow.doActionFor(obj, 'retire')
            self.assertEqual(self.portal_workflow.getInfoFor(obj,
                                'review_state'), 'retired')
            transitions = set([t['id'] for t in
                    self.portal_workflow.getTransitionsFor(obj)])
            intended = set(['deprecate'])
            diff = intended.difference(transitions)
            self.failIf(diff, diff)



def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
