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

   autodoc

Project Requirements
====================

These requirements are derived from the README and describe the core goals, architecture principles, and install objectives for DIShboard.

.. req:: Example of a requirement
   :id: REQ_EXAMPLE1

   This is an example requirement that demonstrates the codelinks functionality


High-Level Requirements
-----------------------

.. req:: Web-first responsive UI
   :id: REQ_WEB_FIRST_UX

   Build a responsive web application with server-rendered pages and progressive enhancement.

.. req:: Real-time persistence of DIS messages
   :id: REQ_PERSISTENCE

   Ingest DIS messages in real time and persist them to a local SQL database for efficient filtering and replay.

.. req:: Flexible SQL-first query model
   :id: REQ_SQL_QUERY_MODEL

   Support raw SQL filtering and higher-level query helpers for time range, PDU type, entity, and parsed field searches.

.. req:: Shareable URL-driven filters
   :id: REQ_URL_STATE

   Preserve selected filters and list state in URLs so views are shareable and repeatable.

.. req:: Schema flexibility for PDU types
   :id: REQ_SCHEMA_FLEXIBILITY

   Avoid hard-coding every PDU type schema and support extensible PDU type handling.

.. req:: Separation of concerns
   :id: REQ_SEPARATION_OF_CONCERNS

   Keep message ingestion, storage, and UI rendering distinct so the system can evolve independently.

.. req:: Minimal deployment friction
   :id: REQ_MINIMAL_DEPLOYMENT_FRICTION

   Package the project as a standard Python package and keep development tooling simple.

.. req:: No-JavaScript-first navigation
   :id: REQ_NAVIGABLE_WITHOUT_JS

   Make the UI fully navigable without JavaScript whenever possible, while enhancing interactions with HTMX.

Implementation Choices
----------------------

These implementation choices support the high-level requirements without being the only way to satisfy them.

.. spec:: HTMX-driven lightweight interactions
   :id: SPEC_HTMX_INTERACTIONS

   Prefer HTMX for lightweight, declarative UI enhancements and incremental updates.

.. spec:: Django-based backend
   :id: SPEC_USE_DJANGO

   Use Django for request handling, template rendering, and database management.

.. spec:: SQLite with WAL persistence
   :id: SPEC_SQLITE_WAL

   Use SQLite with write-ahead logging for local database persistence.

.. spec:: Batch insert at ~20Hz
   :id: SPEC_BATCH_INSERT_20HZ

   Batch insert PDUs at approximately 20 Hz to balance real-time ingestion with SQLite performance.

.. spec:: Live refresh at ~20Hz
   :id: SPEC_LIVE_REFRESH_20HZ

   Refresh web pages at approximately 20 Hz for live updates using HTMX.

.. spec:: Open-dis-python parsing
   :id: SPEC_OPEN_DIS_PY

   Use open-dis-python for DIS message parsing, serialization, and protocol compliance.

Page Workflow Specifications
----------------------------

.. spec:: Connection information page
   :id: SPEC_CONNECTION_INFORMATION

   Provide a page that displays current connection status, transport configuration, recent connection events, packet rate, and session health.
   Include controls to start/stop listening and configure the source endpoint or replay mode.

.. spec:: Messages page
   :id: SPEC_MESSAGES_PAGE

   Provide a messages page that shows incoming DIS PDUs as sortable, filterable rows with live refresh, incremental loading, and paging.
   Support filters by time range, PDU type, source entity, parsed fields, and raw SQL queries.

.. spec:: Plots page
   :id: SPEC_PLOTS_PAGE

   Provide a plots page with lightweight summary visualizations such as PDU count per second, active entities over time, entity positions, and PDU type distribution.
   Render plots using Altair/Vega and derive visuals from the persisted message data.

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

Source
------

.. src-trace::
   :project: dishboard_source

Tests
-----

.. src-trace::
   :project: dishboard_tests



Source Code API Documentation
=============================
Below is the automatically generated documentation pulled directly from our Python source code.

