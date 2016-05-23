"""Definition of the Howto content type
"""
from zope.interface import implements
from Products.Archetypes import atapi

from hai.pnp import pnpMessageFactory as _
from hai.pnp.interfaces import IHowto
from hai.pnp.config import PROJECTNAME
from hai.pnp.config import FUNCTIONAL_AREA_CODES
from hai.pnp.content.basecontent import BasePandPContent, BasePandPSchema, makeNumericString

HowtoSchema = BasePandPSchema.copy() + atapi.Schema((

    atapi.TextField(
        name='text',
        storage = atapi.AnnotationStorage(),
        required=False,
        searchable=1,
        validators = ('isTidyHtmlWithCleanup',),
        default_output_type = 'text/x-html-safe',
        widget=atapi.RichWidget(
            label=_(u"Howto Text"),
            description=_(u"Detailed text of this Policy"),
        ),
    ),
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

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.
HowtoSchema['title'].storage = atapi.AnnotationStorage()
HowtoSchema['description'].storage = atapi.AnnotationStorage()

# Hide some fields
HowtoSchema["location"].widget.visible = False
HowtoSchema["creators"].widget.visible = {"edit": "invisible", "view": "visible"}
HowtoSchema["contributors"].widget.visible = False
HowtoSchema["relatedItems"].widget.visible = False

# Set up relationships
HowtoSchema['howtos'].relationship = 'howtoa_howtob'
HowtoSchema['policies'].relationship = 'howtos_policies'
HowtoSchema['procedures'].relationship = 'howtos_procedures'
HowtoSchema['forms'].relationship = 'howtos_forms'

# Move field
HowtoSchema.moveField('functionalAreaCode', after='theatreOfOpsCode')

class Howto(BasePandPContent):
    """A job aid targeted at a specific staff audience"""
    implements(IHowto)

    meta_type = "Howto"
    schema = HowtoSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')


atapi.registerType(Howto, PROJECTNAME)
