import unittest
from Products.CMFCore.utils import getToolByName

from hai.pnp.tests.base import TestCase

class TestSetup(TestCase):

    def afterSetUp(self):
        self.portal_skins = getToolByName(self.portal, 'portal_skins')
        self.portal_css = getToolByName(self.portal, 'portal_css')
        self.portal_types = getToolByName(self.portal, 'portal_types')
        self.portal_properties = getToolByName(self.portal, 
                                                'portal_properties')
        self.portal_quickinstaller = getToolByName(self.portal, 
                                                'portal_quickinstaller')
    
    def test_product_installed(self):
        self.failUnless(self.portal_quickinstaller.isProductInstalled('hai.pnp'))
    
    def test_relations_installed(self):
        self.failUnless(self.portal_quickinstaller.isProductInstalled('Relations'))
    
    def test_relations_config_imported(self):
        relations = getToolByName(self.portal, 'relations_library')
        self.failUnless('HAIPoliciesAndProcedures' in relations.objectIds())
    
    def test_relations_config_plays_well_with_others(self):
        config = """<?xml version="1.0" ?>
<RelationsLibrary>
    <RulesetCollection id="SomeOtherID" title="Some Other Title" uid="cefd914e1166b94298f2907d08aaaaaaa">
      <Ruleset id="foobar" title="foobar" uid="982def69845871304c9175982be44444">
        <about> </about>
      </Ruleset>
    </RulesetCollection>
</RelationsLibrary>"""
        
        relations = getToolByName(self.portal, 'relations_library')
        self.setRoles(['Manager',])
        relations.importXML(config)
        self.portal_quickinstaller.reinstallProducts(['hai.pnp',])
        self.failUnless('SomeOtherID' in relations.objectIds())
        self.failUnless('HAIPoliciesAndProcedures' in relations.objectIds())

    def test_append_view_to_forms(self):
        site_props = self.portal_properties.site_properties
        use_view = site_props.typesUseViewActionInListings
        self.failUnless('Form' in use_view)
        # Make sure we don't break anything
        self.failUnless('File' in use_view)
    
    # def test_tinymce_config(self):
    #     """ This test won't run under roadrunner, so skip it."""
    #     pnp_types = ('Manual', 'Policy', 'Procedure', 'Howto', 'Form')
    #     for ptype in pnp_types:
    #         self.failUnless(ptype in self.tinymce.linkable, 
    #                 "%s not linkable in TinyMCE" % ptype)
    #     # Make sure we don't break defaults
    #     self.failUnless('Document' in self.tinymce.linkable)
    
def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
