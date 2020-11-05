Development Overview
====================

The following sections aim to bring a new developer up to speed on the Glyph project on a deeper
level than someone looking to use it as an application or even who is deploying it. The goal is to
understand the underlying design aspects and code layouts that make the project possible, and how
the different parts of the system interact together to make a complete application.

Django Background
-----------------

The Glyph backend is written using the `Python Django framework <https://www.djangoproject.com/>`_,
so we *highly* advise that you learn the basics of working with a Django-based project before
contributing major bits of code. For smaller commits and typo fixes, this level of knowledge
may not be required. On top of this, `Django Rest Framework <drf_>`_
is also heavily used to serve most (if not all) of the API traffic and routes.

Layers of Abstraction
+++++++++++++++++++++

If you do not have time to commit to following the Django documentation, the following is designed
to give a crash course overview of the project and what its comprised of. Its in no way meant to be
extensive or comprehensive.


App
***

Django is built around the concept of **apps**. This README does not go terribly in depth of what
they are, but essentially they are specifically-structured modules that provide separation of
functionality in the Django project.

A Django app is a small library representing a discrete part of a larger project. For example,
we have our apps under the ``glyph.apps`` module, each of which comprises some core
functionality of the total project.


Model
*****

At the core of each app is the list of **models** it defines. Models map database tables to Python objects.
Again, Django covers the responsibilities and usages of models pretty extensively, so please
`check out their documentation <https://docs.djangoproject.com/en/3.1/topics/db/models/>`_ on it.


Serializer
**********

`Serializers <https://www.django-rest-framework.org/api-guide/serializers/>`_ are a
`Django Rest Framework <drf_>`_ concept that describe converting
models to and from JSON, and under what circumstances. These automatic and provide a common
interface for describing how (de)serialization works through the project and its routes.


View / Viewsets
***************

`Views <https://www.django-rest-framework.org/api-guide/views/>`_ provide an API endpoint that tie
together a model, its serializer, and a request method (``GET``, ``POST``, ``DELETE``...).
Django Rest Framework has tooling to abstract views out to very similar class declarations.

Views are usually collected into a single
`ViewSet <https://www.django-rest-framework.org/api-guide/viewsets/>`_,
which defines all of the associated views needed for a model, handling different actions, such as
creating, deleting, listing, and retrieving instances.

These viewsets are attached to `Routers <https://www.django-rest-framework.org/api-guide/routers/>`_
that automatically generate the URL patterns for the associated views.

Viewset Filter
**************

`Filters <https://www.django-rest-framework.org/api-guide/filtering/>`_ act on views & viewsets to
return a subset of models based on *query parameters*. This can include pagination, normal filtering
for specific objects through exact or containing searches, and ordering. Each view usually
has an associated `FilterSet` that determines what fields and query parameters can be filtered
against on a model.


Project Breakdown
-----------------

Puzzle App
++++++++++

The ``glyph.apps.puzzle`` app contains the core logic and control around puzzles and their applications.

Hunt App
++++++++

The ``glyph.apps.hunt`` app contains the logic and control around simple and complex puzzle hunts
and competitions.


.. _drf: https://www.django-rest-framework.org/