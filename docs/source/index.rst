.. DIShboard documentation master file, created by
   sphinx-quickstart on Sat Jun 13 18:54:43 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

DIShboard documentation
=======================

Add your content using ``reStructuredText`` syntax. See the
`reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_
documentation for details.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   asdf
   

.. req:: Example of a requirement
   :id: REQ_EXAMPLE1

   This is an example of a requirement. It can be used to demonstrate the
   functionality of the Sphinx-Needs extension.



Requirements & Specifications
=============================

.. needtable::
   :types: requirement, specification
   :columns: id, title, type, incoming, outgoing
   :style: table

Implementation & Verification Traceability
===========================================
This matrix automatically matches our functional specifications to our actual PyTest test cases and codebase implementations.

.. needtable::
   :types: test_case, code_impl
   :columns: id, title, type, tests, implements
   :style: line


CODELINKS
=========

.. src-trace::
   :project: dishboard


Source Code API Documentation
=============================
Below is the automatically generated documentation pulled directly from our Python source code.

