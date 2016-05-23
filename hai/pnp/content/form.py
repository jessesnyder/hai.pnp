""" Definition of the Form content type
"""
from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import file

from hai.pnp import pnpMessageFactory as _
from hai.pnp.interfaces import IForm
from hai.pnp.config import PROJECTNAME
from hai.pnp.config import FUNCTIONAL_AREA_CODES
from hai.pnp.content.basecontent import BasePandPContent, BasePandPSchema

FormSchema = file.ATFileSchema.copy() + BasePandPSchema.copy() + atapi.Schema((
    # -*- Your Archetypes field definitions here ... -*-
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

# Set storage on fields copied from ATFileSchema, making sure
# they work well with the python bridge properties.
FormSchema['title'].storage = atapi.AnnotationStorage()
FormSchema['description'].storage = atapi.AnnotationStorage()

# Hide some fields
FormSchema["location"].widget.visible = False
FormSchema["creators"].widget.visible = {"edit": "invisible", "view": "visible"}
FormSchema["contributors"].widget.visible = False
FormSchema["relatedItems"].widget.visible = False

# Set up relationships
FormSchema['forms'].relationship = 'forma_formb'
FormSchema['policies'].relationship = 'forms_policies'
FormSchema['procedures'].relationship = 'forms_procedures'
FormSchema['howtos'].relationship = 'forms_howtos'

# Move field
FormSchema.moveField('functionalAreaCode', after='theatreOfOpsCode')

class Form(file.ATFile, BasePandPContent):
    """A standard file that supports a procedure"""
    implements(IForm)

    meta_type = "Form"
    schema = FormSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    def _renameAfterCreation(self, check_auto_id=False):
        return BasePandPContent._renameAfterCreation(self, check_auto_id)
    


atapi.registerType(Form, PROJECTNAME)
