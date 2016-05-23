"""Common configuration constants
"""
from hai.pnp import pnpMessageFactory as _

PROJECTNAME = 'hai.pnp'

PRODUCT_GLOBALS = globals()

ADD_PERMISSIONS = {
    # -*- extra stuff goes here -*-
    'BasePolicyProcedureContent': 'hai.pnp: Add BasePolicyProcedureContent',
    'Howto': 'hai.pnp: Add Howto',
    'Form': 'hai.pnp: Add Form',
    'Procedure': 'hai.pnp: Add Procedure',
    'Policy': 'hai.pnp: Add Policy',
    'Manual': 'hai.pnp: Add Manual',
}

THEATRE_OPS_CODES = (
    ('', _(u'--choose one--')),
    ('GLO', _(u'Global')),
    ('MOZ', _(u'Mozambique')),
    ('SEA', _(u'Seattle HQ')),
    ('CI', _(u"Cote d'Ivoire")),
    ('SUD', _(u'Sudan')),
    ('TL', _(u'Timor Leste')),
    ('COL', _(u'Columbia')),
)

FUNCTIONAL_AREA_CODES = (
    ('', _(u'--choose one--')),
    ('COM', _(u'Communications')),
    ('FAC', _(u'Facilities')),
    ('FIN', _(u'Finance')),
    ('GRA', _(u'Grants and Budget Management')),
    ( 'HR', _(u'Human Resources')),
    ('IST', _(u'Information Services and Technology')),
    ('NEW', _(u'New Initiatives')),
    ('OPS', _(u'Operating Principles')),
    ('PRO', _(u'Procurement')),
    ('SFT', _(u'Safety and Security')),
    ('TRA', _(u'Employee Travel')),
)
