from DateTime import DateTime
import transaction
from AccessControl import ClassSecurityInfo

from Products.CMFCore.permissions import ModifyPortalContent
from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content import base
from Products.Relations.field import RelationField
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.OrderableReferenceField import OrderableReferenceField
from Products.OrderableReferenceField import OrderableReferenceWidget

from Products.CMFCore.utils import getToolByName
from plone.i18n.normalizer import IDNormalizer

from hai.pnp import pnpMessageFactory as _
from hai.pnp import config
from hai.pnp.pnputils import camelize


BasePandPSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

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
    
        RelationField(
        name='policies',
        widget=ReferenceBrowserWidget
        (
            label=_(u"haipnp_label_policies", default=u"Related Policies"),
            i18n_domain='hai.pnp',
            allow_browse = True,
            allow_search = True,
            show_results_without_query = False,
            base_query = '_search_policies',
        ),
        schemata="categorization",
        storage=atapi.AnnotationStorage(),
        multiValued=True,
        relationship='',
        allowed_types = ('Policy',),
    ),
        
    RelationField(
        name='procedures',
        widget=ReferenceBrowserWidget
        (
            label=_(u"haipnp_label_procedures", default=u"Related Procedures"),
            i18n_domain='hai.pnp',
            allow_browse = True,
            allow_search = True,
            show_results_without_query = False,
            base_query = '_search_procedures',
        ),
        schemata="categorization",
        storage=atapi.AnnotationStorage(),
        multiValued=True,
        relationship='',
        allowed_types = ('Procedure',),
    ),

    RelationField(
        name='forms',
        widget=ReferenceBrowserWidget
        (
            label=_(u"haipnp_label_forms", default=u"Related Forms/Templates"),
            i18n_domain='hai.pnp',
            allow_browse = True,
            allow_search = True,
            show_results_without_query = False,
            base_query = '_search_forms',
        ),
        schemata="categorization",
        storage=atapi.AnnotationStorage(),
        multiValued=True,
        relationship='',
        allowed_types = ('Form',),
    ),

    RelationField(
        name='howtos',
        widget=ReferenceBrowserWidget
        (
            label=_(u"haipnp_label_howtos", default=u"Related How-tos"),
            i18n_domain='hai.pnp',
            allow_browse = True,
            allow_search = True,
            show_results_without_query = False,
            base_query = '_search_howtos',
        ),
        schemata="categorization",
        storage=atapi.AnnotationStorage(),
        multiValued=True,
        relationship='',
        allowed_types = ('Howto',),
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

def makeNumericString(numbering):
   text = ''
   for number in numbering:
       text = text+str(number)+'.'

   return text

class TreeRenderer(object):
    """ Render a tree of objects, delegating to each object to return its own
        children
        
        This class encapsulates:
            1. node/leaf numbering and hierarchy
            2. enforcing that each node/leaf is only dealt with once
    """
    
    def __init__(self, leaf_renderer, css_class=None):
        self._leaf_renderer = leaf_renderer
        self._css_class = css_class
        self._visited_list = []
        self._numbering = []
    
    def render(self, obj):
        """ Render the whole system of related objects starting at the object
            passed as an arg.
        """
        text = ''
        if self._visited(obj):
            return text
        self._mark(obj)
        if self._is_child():
            self._increment()
            text = self.render_leaf(obj)
        children = obj.children()
        if children:
            self._new_level()
            for child in children:
                subtext = self.render(child)
                if subtext:
                    text += self._wrap_subtext(subtext)
            self._back_level()
        
        return text
    
    def render_leaf(self, obj):
        """ Render a single leaf, or a node as if it were a leaf.
        """
        return self._leaf_renderer.render_leaf(obj, self._pretty_number())
    
    def _wrap_subtext(self, subtext):
        text = "<div%s>%s</div>" % (self._css(), subtext)
        
        return text
    
    def _css(self):
        if self._css_class is None:
            return ''
        return ' class="%s"' % self._css_class
    
    def _current_level(self):
        return len(self._numbering)
    
    def _pretty_number(self):
        return makeNumericString(self._numbering)
    
    def _increment(self):
        if not self._numbering:
            self._new_level()
        self._numbering[-1] += 1
    
    def _is_child(self):
        return len(self._visited_list) > 1
    
    def _new_level(self):
        self._numbering.append(0)
    
    def _back_level(self):
        self._numbering.pop()
    
    def _mark(self, obj):
        self._visited_list.append(obj.UID())
    
    def _visited(self, obj):
        return obj.UID() in self._visited_list
    

class FullTextTreeRenderer(TreeRenderer):
    """ Wrap subtext slightly differently.
    """
    def _wrap_subtext(self, subtext):
        text = "<div%s>%s</div>" % (self._css(), subtext)
        if self._current_level() == 1:
            text += '<div class="pageBreak" >&nbsp;</div>'
        return text
    

class BaseLeafRenderer(object):
    """ Most boring renderer.
    """
    def render_leaf(self, obj, number):
        text = "%s %s" % (number, obj.Title())
            
        return text
    

class LinkingLeafRenderer(object):
    """ A renderer that makes the titles for each node display as links to
        the real objects.
    """
    def render_leaf(self, obj, number):
        text = '%s <a href="%s">%s</a>' % (number, obj.absolute_url(), 
                                                obj.Title())
        
        return text

class FullTextLeafRenderer(object):
    """ A renderer that dumps some overview info plus the full body text of
        each node.
    """
    def render_leaf(self, obj, number):
        workflow = getToolByName(obj, 'portal_workflow')
        state = workflow.getInfoFor(obj, 'review_state')
        contenttype = obj.portal_type
        text = "<h2>%s %s</h2>" % (number, obj.Title())
        text += "<span class='pnpid'>[ %s ] </span>" % obj.getId()
        text += "<span class='pnpdate'>[ revised: %s ] </span>" % obj.ModificationDate()
        text += "<span class='pnptype'>[ %s ] </span>" % contenttype
        if state != 'official':
            text += "<span class='pnpstate'>[ %s ] </span>" % state
        text += "<p>%s</p>" % obj.getText()
            
        return text
    

class BasePandPContent(base.ATCTContent):
    """ Base class for Policy and Procedure types
    """
    meta_type = "BasePandPContent"
    schema = BasePandPSchema
    security = ClassSecurityInfo()
    
    def _renameAfterCreation(self, check_auto_id=False):
        """ The ID (short name) for Policy and Procedure types is 
            a concatenated string comprised of four distinct elements
            separated by dashes:
            {Theatre of Ops}-{Function Area}-{Content Type}-{Camelized Title}
        """
        ops = self.getTheatreOfOpsCode()
        func = self.getFunctionalAreaCode()
        ptype = self.portal_type
        title = self.Title()
        if not isinstance(title, unicode):
            charset = self.getCharset()
            title = unicode(title, charset)
        
        cleaner = IDNormalizer().normalize(title)
        title = camelize(cleaner.replace('-', ' '))
        new_id = "%s-%s-%s-%s" % (ops, func, ptype, title)
        # Can't rename without a subtransaction commit when using
        # portal_factory. Yes it's true! 
        transaction.savepoint(optimistic=True)
        self.setId(new_id)
    
    def approvedBy(self):
        """ If the object is in the "official" workflow state, return
            the ID of the user who moved it there, otherwise, return
            an emtpy string.
        """
        wftool = getToolByName(self, 'portal_workflow')
        state = wftool.getInfoFor(self, 'review_state')
        if state != 'official':
            return ''
        actor = wftool.getInfoFor(self, 'actor')
        return actor
    
    def toc(self, renderer=None):
        """ Render a table of contents, with links
        """
        if renderer is None:
            renderer = TreeRenderer(LinkingLeafRenderer(),
                                    css_class='doc-indented')
        html = renderer.render(self)
        
        return html
    
    def prettyprint(self, renderer=None):
        if renderer is None:
            renderer = FullTextTreeRenderer(FullTextLeafRenderer(),
                                            css_class='doc-indented')
        html = renderer.render(self)
        
        return html
    
    def children(self):
        """ Returns related items that behave logically as sub-items when 
            rendering a set of P&P objects as a hierarchy (toc, print view).
            
            By default, return all related content, but subclasses will likely
            limit the content types returned to those that make sense to show
            "below" the context object. Think of this as a "Factory Method".
        """
        pols = self.getPolicies()
        procs = self.getProcedures()
        howtos = self.getHowtos()

        docs = pols + procs + howtos
        
        return docs
    
    security.declareProtected(ModifyPortalContent, '_limit_rbw_search_params')
    def _limit_rbw_search_params(self, portal_type, sort_on="sortable_title"):
        """ return a query dictionary to limit the search parameters for a 
            reference browser widget query.  Use as basis for more specific 
            versions below
        """
        path = '/'
        return {'portal_type': portal_type,
                'sort_on': sort_on,
                'path': {'query': path}}

    security.declareProtected(ModifyPortalContent, '_search_procedures')
    def _search_procedures(self):
        """ search only procedures
        """
        return self._limit_rbw_search_params(portal_type="Procedure")
    
    security.declareProtected(ModifyPortalContent, '_search_policies')
    def _search_policies(self):
        """ search only policies
        """
        return self._limit_rbw_search_params(portal_type="Policy")
    
    security.declareProtected(ModifyPortalContent, '_search_howtos')
    def _search_howtos(self):
        """ search only howtos
        """
        return self._limit_rbw_search_params(portal_type="Howto")
    
    security.declareProtected(ModifyPortalContent, '_search_forms')
    def _search_forms(self):
        """ search only forms
        """
        return self._limit_rbw_search_params(portal_type="Form")
    
