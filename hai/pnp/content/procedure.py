""" Definition of the Procedure content type
"""
from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import document

from Products.OrderableReferenceField import OrderableReferenceField
from Products.OrderableReferenceField import OrderableReferenceWidget

from hai.pnp import pnpMessageFactory as _
from hai.pnp.interfaces import IProcedure
from hai.pnp.config import FUNCTIONAL_AREA_CODES
from hai.pnp.config import PROJECTNAME
from hai.pnp.content.basecontent import BasePandPContent, BasePandPSchema

ProcedureSchema = document.ATDocumentSchema.copy() + BasePandPSchema.copy() + atapi.Schema((

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
    
    OrderableReferenceField(
        name="childItems",
        schemata="categorization",
        relationship='children',
        allowed_types = ('Howto', 'Form',),
        multiValued = 1,
        vocabulary_display_path_bound = None,
        widget=OrderableReferenceWidget(
            label=_(u"Child Items"),
            description=_(u"Items which will be rendered as children of this object in the TOC and printed versions of manuals."),
        )
    ),
))

# Set storage on fields copied from ATDocumentSchema, making sure
# they work well with the python bridge properties.
ProcedureSchema['title'].storage = atapi.AnnotationStorage()
ProcedureSchema['description'].storage = atapi.AnnotationStorage()

# Hide some fields
ProcedureSchema["location"].widget.visible = False
ProcedureSchema["creators"].widget.visible = {"edit": "invisible", "view": "visible"}
ProcedureSchema["contributors"].widget.visible = False
ProcedureSchema["relatedItems"].widget.visible = False

# Set up relationships
ProcedureSchema['procedures'].relationship = 'procedurea_procedureb'
ProcedureSchema['policies'].relationship = 'procedures_policies'
ProcedureSchema['forms'].relationship = 'procedures_forms'
ProcedureSchema['howtos'].relationship = 'procedures_howtos'

# Move field
ProcedureSchema.moveField('functionalAreaCode', after='theatreOfOpsCode')

class Procedure(document.ATDocument, BasePandPContent):
    """The process by which an organizational policy is implemented"""
    implements(IProcedure)

    meta_type = "Procedure"
    schema = ProcedureSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    def _renameAfterCreation(self, check_auto_id=False):
        return BasePandPContent._renameAfterCreation(self, check_auto_id)
    

atapi.registerType(Procedure, PROJECTNAME)
