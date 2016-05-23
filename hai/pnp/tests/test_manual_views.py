import unittest
from hai.pnp.content import basecontent

from hai.pnp.tests.base import TestCase

class TestTreeRenderer(TestCase):
    
    def afterSetUp(self):
        self.setRoles(['Manager',])
        self.folder.invokeFactory("Manual", "manual1", title="Manual 1")
        self.manual1 = self.folder.manual1
        self.folder.invokeFactory("Manual", "manual2", title="Manual 2")
        self.manual2 = self.folder.manual2
        
        self.folder.invokeFactory("Policy", "policy1", title="Policy 1")
        self.policy1 = self.folder.policy1
        self.folder.invokeFactory("Policy", "policy2", title="Policy 2")
        self.policy2 = self.folder.policy2
        
        self.folder.invokeFactory("Procedure", "procedure1", title="Procedure 1")
        self.procedure1 = self.folder.procedure1
        
        self.folder.invokeFactory("Form", "form1", title="Form 1")
        self.form1 = self.folder.form1
        
        self.folder.invokeFactory('Howto', 'howto1', title="Howto 1")
        self.howto1 = self.folder.howto1
        
        self.renderer = basecontent.TreeRenderer(leaf_renderer=basecontent.BaseLeafRenderer())
    
    def beforeTearDown(self):
        pass
    
    def test_manual_only(self):
        toc = self.renderer.render(self.manual1)
        self.assertEquals('', toc)
    
    def test_one_item(self):
        self.manual1.setRelatedItems((self.policy1,))
        toc = self.renderer.render(self.manual1)
        self.assertEqual("<div>1. Policy 1</div>", toc)
    
    def test_two_items(self):
        self.manual1.setRelatedItems((self.policy1, self.procedure1))
        toc = self.renderer.render(self.manual1)
        self.assertEqual("<div>1. Policy 1</div><div>2. Procedure 1</div>", toc)
    
    def test_duplicate_item(self):
        self.manual1.setRelatedItems((self.policy1, self.procedure1, self.policy1))
        toc = self.renderer.render(self.manual1)
        # order is unpredictable(?) so just check number of divs
        self.assertEqual(2, toc.count('</div>'))
    
    def test_one_subitem(self):
        self.policy1.setProcedures((self.procedure1,))
        self.manual1.setRelatedItems((self.policy1,))
        toc = self.renderer.render(self.manual1)
        self.assertEqual("<div>1. Policy 1<div>1.1. Procedure 1</div></div>",
                        toc)
    
    def test_two_subitems(self):
        self.policy1.setProcedures((self.procedure1,))
        self.policy1.setHowtos((self.howto1,))
        self.manual1.setRelatedItems((self.policy1,))
        toc = self.renderer.render(self.manual1)
        self.assertEqual("<div>1. Policy 1<div>1.1. Procedure 1</div><div>1.2. Howto 1</div></div>",
                        toc)    

    def test_circular_reference_top_and_child(self):
        # procedure1 is pulled in both through its relationship with policy1...
        self.policy1.setProcedures((self.procedure1,))
        self.policy1.setHowtos((self.howto1,))
        # .. and because it's related directly to the manual
        self.manual1.setRelatedItems((self.policy1, self.procedure1))
        toc = self.renderer.render(self.manual1)
        # but we should only list it once, on the first depth-first traversal
        self.assertEqual("<div>1. Policy 1<div>1.1. Procedure 1</div><div>1.2. Howto 1</div></div>",
                        toc)
    
    def test_circular_reference_two_children(self):
        self.howto1.setProcedures((self.procedure1,))
        self.policy1.setProcedures((self.procedure1,))
        self.policy1.setHowtos((self.howto1,))
        self.manual1.setRelatedItems((self.policy1))
        toc = self.renderer.render(self.manual1)
        # because we go depth-first, we'll now have 3 levels, but no dups
        self.assertEqual("<div>1. Policy 1<div>1.1. Procedure 1<div>1.1.1. Howto 1</div></div></div>",
                        toc)    
    
    def test_two_levels_pops_up(self):
        # Make sure we fold out levels correctly 
        self.policy1.setProcedures((self.procedure1,))
        self.policy1.setHowtos((self.howto1,))
        self.manual1.setRelatedItems((self.policy1, self.policy2))
        toc = self.renderer.render(self.manual1)        
        self.assertEqual("<div>1. Policy 1<div>1.1. Procedure 1</div><div>1.2. Howto 1</div></div><div>2. Policy 2</div>",
                        toc)
    
    def test_related_manual(self):
        self.policy1.setProcedures((self.procedure1,))
        self.policy1.setHowtos((self.howto1,))
        self.manual2.setRelatedItems((self.policy1, self.policy2))
        self.manual1.setRelatedItems((self.manual2,))
        toc = self.renderer.render(self.manual1)
        self.assertEqual("<div>1. Manual 2<div>1.1. Policy 1<div>1.1.1. Procedure 1</div><div>1.1.2. Howto 1</div></div><div>1.2. Policy 2</div></div>", toc)
    

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
