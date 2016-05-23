""" Definition of the Policy content type
"""
from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import document

from hai.pnp import pnpMessageFactory as _
from hai.pnp.interfaces import IPolicy
from hai.pnp.config import PROJECTNAME
from hai.pnp.config import FUNCTIONAL_AREA_CODES
from hai.pnp.content.basecontent import BasePandPContent, BasePandPSchema


PolicySchema = document.ATDocumentSchema.copy() + BasePandPSchema.copy() + atapi.Schema((

    atapi.StringField(
        'functionalAreaCode',
        schemata='categorization',
        storage=atapi.AnnotationStorage(),
        vocabulary=FUNCTIONAL_AREA_CODES,
        enforce_vocabulary=True,
        widget=atapi.SelectionWidget(
            label=_(u"Functional Area Code"),
            description=_(u"The department or function that governs this content"),
        ),
        required=True,
    ),
       
))

# Set storage on fields copied from ATDocumentSchema, making sure
# they work well with the python bridge properties.
PolicySchema['title'].storage = atapi.AnnotationStorage()
PolicySchema['description'].storage = atapi.AnnotationStorage()

# Hide some fields
PolicySchema["location"].widget.visible = False
PolicySchema["creators"].widget.visible = {"edit": "invisible", "view": "visible"}
PolicySchema["contributors"].widget.visible = False
PolicySchema["relatedItems"].widget.visible = False

# Set up relationships
PolicySchema['policies'].relationship = 'policya_policyb'
PolicySchema['procedures'].relationship = 'policies_procedures'
PolicySchema['forms'].relationship = 'policies_forms'
PolicySchema['howtos'].relationship = 'policies_howtos'

# Move field
PolicySchema.moveField('functionalAreaCode', after='theatreOfOpsCode')

class Policy(document.ATDocument, BasePandPContent):
    """A statement of standard, approved behavior or operating principle"""
    implements(IPolicy)

    meta_type = "Policy"
    schema = PolicySchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    def _renameAfterCreation(self, check_auto_id=False):
        return BasePandPContent._renameAfterCreation(self, check_auto_id)
    
    
atapi.registerType(Policy, PROJECTNAME)
