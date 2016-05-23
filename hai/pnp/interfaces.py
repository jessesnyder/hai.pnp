from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer

class IHAIPolicyProcedureLayer(IDefaultPloneLayer):
    """Marker interface that will be applied to the request when this product
       is installed.
    """

class IPolicyProcedure(Interface):
    """ Common base marker interface for P & P content
    """

class IForm(IPolicyProcedure):
    """A standard document that supports a procedure"""

class IHowto(IPolicyProcedure):
    """A job aid targeted at a specific staff audience"""

class IPolicy(IPolicyProcedure):
    """A statement of standard, approved behavior or operating principle"""

class IProcedure(IPolicyProcedure):
    """The process by which an organizational policy is implemented"""

class IManual(IPolicyProcedure):
    """The process by which an organizational policy is implemented"""
