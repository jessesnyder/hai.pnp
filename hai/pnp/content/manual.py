"""Definition of the Manual content type
"""
import logging
from DateTime import DateTime

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import document

from hai.pnp import pnpMessageFactory as _
from hai.pnp.interfaces import IManual
from hai.pnp import config
from basecontent import BasePandPContent

logger = logging.getLogger('hai.pnp')


ManualSchema = document.ATDocumentSchema.copy() + atapi.Schema((

    atapi.StringField(
        'theatreOfOpsCode',
        schemata='categorization',
        storage=atapi.AnnotationStorage(),
        vocabulary=config.THEATRE_OPS_CODES,
        enforce_vocabulary=True,
        widget=atapi.SelectionWidget(
            label=_(u"Theatre of Operations Code"),
            description=_(u"Represents the HAI country program where this content is applicable"),
        ),
        required=True,
    ),
    
    atapi.DateTimeField(
        'activeDate',
        schemata='dates',
        default = DateTime(DateTime().strftime("%Y/%m/%d")),
        storage=atapi.AnnotationStorage(),
        widget=atapi.CalendarWidget(
            label=_(u"Active Date"),
            description=_(u"The date this content is active"),
            show_hm = False,
        ),
        validators=('isValidDate'),
    ),
    
    atapi.StringField(
        'contact',
        schemata='ownership',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Contact"),
            description=_(u"The staff member responsible for maintaining this content"),
        ),
    ),    
))

# Set storage on fields copied from ATDocumentSchema, making sure
# they work well with the python bridge properties.
ManualSchema['title'].storage = atapi.AnnotationStorage()
ManualSchema['description'].storage = atapi.AnnotationStorage()

# Hide some fields
ManualSchema["location"].widget.visible = False
ManualSchema["creators"].widget.visible = {"edit": "invisible", "view": "visible"}
ManualSchema["contributors"].widget.visible = False
ManualSchema["relatedItems"].widget.visible = True



class Manual(document.ATDocument, BasePandPContent):
    """A complete collection of policies and procedures, often specific to a
       HAI theatre of operation (Seattle HQ, Mozambique, etc).
    """
    implements(IManual)

    meta_type = "Manual"
    schema = ManualSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
       
    def children(self):
        """ Returns related items that behave logically as sub-items when 
            rendering a set of P&P objects as a hierarchy (toc, print view).
            
            Manuals use their Related Items list.
        """
        return self.getRelatedItems()
    


atapi.registerType(Manual, config.PROJECTNAME)
