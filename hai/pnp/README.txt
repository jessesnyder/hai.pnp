===========================
HAI Policies and Procedures
===========================

Developed by NPower Seattle for Health Alliance International.

Overview
--------
This package implements a set of content types and relationships to model HAI's centrally managed Policy and Procedure documents. To facilitate re-use of documents that are applicable in more than one context, the association between different objects is relational rather than containment-based. The Products.Relations package was used to support bi-directional relationships (see 'Dependencies' below).

Dependencies
------------
The main dependency of this package is the Products.Relations package, which provides bi-directional references between the various types of content object. There is some risk here, since relationship construction in Plone seems to clearly be going in a different direction (z3c.relations and plone.app.relations in particular). However, because the project is already making heavy use of Products.Relations via the Products.FacultyStaffDirectory product, this risk seemed justified since it avoids adding several new dependencies on packages geared more toward Plone 4.
