import os
from App.Common import package_home

from Products.CMFCore.utils import getToolByName

from hai.pnp.config import PRODUCT_GLOBALS

def install_relations(portal):
    qi = getToolByName(portal, 'portal_quickinstaller')
    if not qi.isProductInstalled('Relations'):
        qi.installProduct('Relations')
        
def import_relationship_config(portal):
    # configuration for Relations
    relations_tool = getToolByName(portal,'relations_library')
    if 'HAIPoliciesAndProcedures' not in relations_tool.objectIds():
        xmlpath = os.path.join(package_home(PRODUCT_GLOBALS),'relations.xml')
        f = open(xmlpath)
        xml = f.read()
        f.close()
        relations_tool.importXML(xml)    

def setupVarious(context):
    if context.readDataFile('hai.pnp_various.txt') is None:
        return

    # Add additional setup code here
    site = context.getSite()
    install_relations(site)
    import_relationship_config(site)

