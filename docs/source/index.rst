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

.. req:: PARENT
   :id: REQ_PARENT

   This is a parent requirement that has child requirements. Used for visualisation in ubCode graph

.. req:: Show Engagement Behaviour
   :id: REQ_ENGAGEMENT_BEHAVIOUR
   :parent: REQ_PARENT

   The main goal of DIShboard





User Experience
---------------

.. req:: Shareable URL-driven filters
   :id: REQ_URL_STATE
   :parent: REQ_WEB_FIRST_UX

   Preserve selected filters and list state in URLs so views are shareable and repeatable.



Analysis Capability
-------------------

.. req:: Provide tools to investigate a DIS scenario
   :id: REQ_DIS_INVESTIGATION_TOOLS
   :parent: REQ_ENGAGEMENT_BEHAVIOUR

   Provide tools to investigate a DIS scenario

.. req:: Replay DCS files
   :id: REQ_DCS_FILE_REPLAY
   :parent: REQ_ENGAGEMENT_BEHAVIOUR

   Support replay of DCS recording files into the 3D operational view, translating file contents into platform state and event playback while preserving DIS filters.

.. req:: Replay SIMDIS ASI files
   :id: REQ_SIMDIS_ASI_REPLAY
   :parent: REQ_ENGAGEMENT_BEHAVIOUR

   Support replay of SIMDIS ASI files into the 3D operational view, translating file contents into platform state and event playback while preserving DIS filters.

3D Operational Display
~~~~~~~~~~~~~~~~~~~~~~~

.. req:: 3D operational map
   :id: REQ_3D_OPERATIONAL_MAP
   :parent: REQ_ENGAGEMENT_BEHAVIOUR, REQ_DIS_INVESTIGATION_TOOLS

   Provide a 3D operational display of entities and events, with an interactive scene that supports filtering

.. req:: Live 3D operational map
   :id: REQ_LIVE_3D_OPERATIONAL_MAP
   :parent: REQ_3D_OPERATIONAL_MAP, REQ_DIS_INVESTIGATION_TOOLS

   Provide a 3D operational display of entities and events, with an interactive scene that supports filtering by DIS fields, entity, and PDU type.

.. req:: Allow DIS inspection in the 3D operational map
   :id: REQ_DIS_INSPECTION_3D_MAP
   :parent: REQ_LIVE_3D_OPERATIONAL_MAP, REQ_DIS_INVESTIGATION_TOOLS

   Allow users to click on entities and events in the 3D map to view detailed DIS message information that contributed to that scene element.

.. req:: TacView-inspired display
   :id: REQ_TACVIEW_INSPIRED
   :parent: REQ_LIVE_3D_OPERATIONAL_MAP, REQ_DCS_FILE_REPLAY, REQ_SIMDIS_ASI_REPLAY, REQ_DIS_MESSAGE_REPLAY

   Design the 3D display layer with inspiration from TacView, emphasizing recorded scenario playback, timeline review, and event-focused replay.

.. req:: SIMDIS-inspired display
   :id: REQ_SIMDIS_INSPIRED
   :parent: REQ_LIVE_3D_OPERATIONAL_MAP, REQ_DCS_FILE_REPLAY, REQ_SIMDIS_ASI_REPLAY, REQ_DIS_MESSAGE_REPLAY

   Design the 3D display layer with inspiration from SIMDIS, emphasizing live operational asset state, entity tracking, and tactical event annotation.

   Inspo:
   * https://www.youtube.com/watch?v=MRKUV1nCEh8

.. req:: Entity trajectory trails
   :id: REQ_ENTITY_TRAJECTORY_TRAILS
   :parent: REQ_SIMDIS_INSPIRED

   Display past entity motion as trails or track histories so users can analyze movement, engagements, and maneuver patterns over time.

.. req:: Event markers and engagement visualization
   :id: REQ_EVENT_MARKERS
   :parent: REQ_SIMDIS_INSPIRED

   Render fires, detonations, collisions, and similar engagement events as distinct markers or annotations on the 3D scene.

.. req:: Camera and viewport controls
   :id: REQ_CAMERA_VIEW_CONTROLS
   :parent: REQ_SIMDIS_INSPIRED, REQ_TACVIEW_INSPIRED

   Provide orbit, pan, zoom, and center-on-entity view controls suitable for inspecting tactical scenes from multiple perspectives.

.. req:: Layer and symbol visibility control
   :id: REQ_LAYER_SYMBOL_CONTROL
   :parent: REQ_SIMDIS_INSPIRED

   Allow users to toggle visibility of entity layers, event symbols, trails, and annotations to reduce clutter and focus on selected assets.

.. req:: Use Standard Symbols
   :id: REQ_USE_STANDARD_SYMBOLS
   :parent: REQ_LIVE_3D_OPERATIONAL_MAP

   Use standard military symbology (e.g., MIL-STD-2525) for platform and event representation in the 3D view.

.. req:: Layered architecture for map rendering
   :id: REQ_LAYERED_MAP_ARCHITECTURE
   :parent: REQ_LIVE_3D_OPERATIONAL_MAP, REQ_DCS_FILE_REPLAY, REQ_SIMDIS_ASI_REPLAY, REQ_DIS_MESSAGE_REPLAY, REQ_SEPARATION_OF_CONCERNS

   Separate the system into ingestion/storage, translation, and rendering layers: raw DIS persistence remains distinct from scene generation, and the renderer consumes a translated scene model that supports DIS filters.

.. req:: Playback and scrubber controls
   :id: REQ_PLAYBACK_SCRUBBER_CONTROLS
   :parent: REQ_TACVIEW_INSPIRED, REQ_SIMDIS_INSPIRED, REQ_DCS_FILE_REPLAY, REQ_SIMDIS_ASI_REPLAY, REQ_DIS_MESSAGE_REPLAY

   Support replay controls including pause/resume, play speed, time scrubber, and jump-to-time for recorded scenarios.


Analysis Plots
~~~~~~~~~~~~~~

.. req:: Analysis Plots
   :id: REQ_ANALYSIS_PLOTS
   :parent: REQ_ENGAGEMENT_BEHAVIOUR

   Provide built-in analysis plots such as PDU rate over time, active entities, and spatial distributions to help users understand engagement dynamics.


Range Tool
~~~~~~~~~~

The range tool is the ability to do calculations based on the data from entities. It shows them on the 3D map IN :need:`REQ_3D_OPERATIONAL_MAP`, but also let's them be graphs in the :need:`REQ_ANALYSIS_PLOTS`. The range tool is a core part of the engagement behavior of DIShboard and allows users to quickly understand the spatial (and other, but it's mostly spatial) relationships between entities in a scenario.

.. req:: Range tool for analysis
   :id: REQ_RANGE_TOOL
   :parent: REQ_ANALYSIS_PLOTS, REQ_3D_OPERATIONAL_MAP

   Provide a range tool that allows users to select two or more entities and visualize the range, bearing, and other  relationships between them in both the 3D map and analysis plots.

.. req:: Analysis tool unit configuration
   :id: REQ_ANALYSIS_UNITS
   :parent: REQ_RANGE_TOOL

   Support configurable display units for all analytical outputs, including Metric (m/km, km/h) and Imperial/Aviation (ft/nm, kts).

.. req:: Slant Range Calculation
   :id: REQ_RANGE_SLANT
   :parent: REQ_RANGE_TOOL

   Calculate and display the 3D Euclidean distance (slant range) between two entities or a defined coordinate pair.

.. req:: Relative Bearing Calculation
   :id: REQ_RANGE_BEARING
   :parent: REQ_RANGE_TOOL

   Calculate the horizontal angle from an entity's current orientation (heading) to a target entity or coordinate.

.. req:: Closure Rate Calculation
   :id: REQ_RANGE_CLOSURE
   :parent: REQ_RANGE_TOOL

   Calculate the rate of change of slant range over time between two entities, accounting for their respective velocity vectors.

.. req:: Closest Point of Approach (CPA)
   :id: REQ_RANGE_CPA
   :parent: REQ_RANGE_TOOL

   Predict and display the minimum slant range between two entities based on their current velocity vectors and acceleration.

.. req:: Aspect Angle Calculation
   :id: REQ_RANGE_ASPECT
   :parent: REQ_RANGE_TOOL

   Calculate the angle between a target's nose-to-tail vector and the line-of-sight vector from an observing entity.

.. req:: Line of Sight (LOS) Obstruction
   :id: REQ_RANGE_LOS
   :parent: REQ_RANGE_TOOL

   Determine if a direct line between two entities is obstructed by terrain elevation data.

.. req:: Time to Intercept (TTI)
   :id: REQ_RANGE_TTI
   :parent: REQ_RANGE_TOOL

   Calculate the time remaining until the slant range between an interceptor and a target reaches zero, assuming current velocity vectors.

.. req:: Elevation Angle Calculation
   :id: REQ_RANGE_ELEVATION
   :parent: REQ_RANGE_TOOL

   Calculate the vertical angle between the local horizontal plane of an observer and the target entity.

.. req:: Ground Speed Calculation
   :id: REQ_RANGE_GROUND_SPEED
   :parent: REQ_RANGE_TOOL

   Calculate and display the ground velocity of an entity based on its X, Y velocity vector components.

.. req:: Vertical Velocity (Rate of Climb/Descent)
   :id: REQ_RANGE_VVI
   :parent: REQ_RANGE_TOOL

   Calculate and display the vertical velocity of an entity based on the Z-axis rate of change.

.. req:: Turn Rate Analysis
   :id: REQ_RANGE_TURN_RATE
   :parent: REQ_RANGE_TOOL

   Calculate and display the instantaneous turn rate based on the change in heading over time.

.. req:: G-Force Estimation
   :id: REQ_RANGE_G_LOAD
   :parent: REQ_RANGE_TOOL

   Estimate the instantaneous G-load on an entity

.. req:: Horizon Range Calculation
   :id: REQ_RANGE_HORIZON
   :parent: REQ_RANGE_TOOL

   Calculate the theoretical radio and optical horizon distance for an entity given its altitude above mean sea level (AMSL).

.. req:: Boresight Alignment Analysis
   :id: REQ_RANGE_BORESIGHT
   :parent: REQ_RANGE_TOOL

   Calculate the angular offset between an entity's nose heading and the line-of-sight vector to a target (tracking error).

.. req:: Weapon Fly-Out Range
   :id: REQ_RANGE_WEAPON_FLIGHT
   :parent: REQ_RANGE_TOOL

   Calculate the cumulative distance traveled by a projectile or missile from the point of start (or some other arbitrary time) to current position.

.. req:: Sensor Field-of-Regard (FOR) intersection
   :id: REQ_RANGE_FOR_INTERSECT
   :parent: REQ_RANGE_TOOL

   Determine if a target entity is contained within the current spatial volume defined by a source entity's sensor cone.

.. req:: Time Delta Measurement
   :id: REQ_RANGE_TIME_DELTA
   :parent: REQ_RANGE_TOOL

   Measure the elapsed simulation time between two discrete events (e.g., time from "Launch" to "Impact").

.. req:: Signal Path Loss Estimation
   :id: REQ_RANGE_PATH_LOSS
   :parent: REQ_RANGE_TOOL

   Estimate the free-space path loss (in dB) between a radar emitter and a target based on slant range and frequency to evaluate detection probability thresholds.

.. req:: Relative Altitude Delta (Angled Slant)
   :id: REQ_RANGE_ALT_DELTA
   :parent: REQ_RANGE_TOOL

   Calculate the direct vertical altitude difference between two entities, specifically isolating the height-of-eye/height-of-target differential.

.. req:: Energy State (Specific Energy) Calculation
   :id: REQ_RANGE_ENERGY_STATE
   :parent: REQ_RANGE_TOOL

   Calculate the specific energy (Energy Height) of an entity (potential + kinetic energy) to evaluate maneuverability and "energy-maneuverability" (EM) dogfight capability.



Architecture
------------

.. req:: Web-first responsive UI
   :id: REQ_WEB_FIRST_UX
   :parent: REQ_ANALYSIS_PLOTS

   Build a responsive web application with server-rendered pages and progressive enhancement.

   Web-application because plotting libraries are just better

.. req:: No-JavaScript-first navigation
   :id: REQ_NAVIGABLE_WITHOUT_JS
   :parent: REQ_WEB_FIRST_UX

   Make the UI fully navigable without JavaScript whenever possible, while enhancing interactions with HTMX.

.. req:: Separation of concerns
   :id: REQ_SEPARATION_OF_CONCERNS
   :parent: REQ_PARENT

   Keep message ingestion, storage, and UI rendering distinct so the system can evolve independently.

.. req:: Minimal deployment friction
   :id: REQ_MINIMAL_DEPLOYMENT_FRICTION
   :parent: REQ_PARENT

   Package the project as a standard Python package and keep development tooling simple.




Data Ingestion and Persistence
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. req:: Real-time persistence of DIS messages
   :id: REQ_PERSISTENCE
   :parent: REQ_DIS_INVESTIGATION_TOOLS

   Ingest DIS messages in real time and persist them to a local SQL database for efficient filtering and replay.

.. req:: Flexible SQL-first query model
   :id: REQ_SQL_QUERY_MODEL
   :parent: REQ_PARENT

   Support raw SQL filtering and higher-level query helpers for time range, PDU type, entity, and parsed field searches.

.. req:: Schema flexibility for PDU types
   :id: REQ_SCHEMA_FLEXIBILITY
   :parent: REQ_PARENT

   Avoid hard-coding every PDU type schema and support extensible PDU type handling.

.. req:: System health and error logging
   :id: REQ_SYSTEM_HEALTH_LOGGING
   :parent: REQ_PARENT

   Maintain logs for system errors, ingestion dropped packets, and application warnings to aid in troubleshooting and system monitoring.

.. req:: Configurable data retention limits
   :id: REQ_DATA_RETENTION
   :parent: REQ_PERSISTENCE

   Provide a mechanism to prune old DIS messages automatically based on a configurable time horizon or database file size limit to prevent disk exhaustion.

.. req:: Pre-ingestion network filtering
   :id: REQ_NETWORK_FILTERING
   :parent: REQ_PERSISTENCE

   Allow configuration of hardware and network-level filters, such as Exercise ID or Site ID, to drop irrelevant PDUs before processing or database insertion.



Other
-----

.. req:: Replay DIS messages from database
   :id: REQ_DIS_MESSAGE_REPLAY
   :parent: REQ_DIS_INVESTIGATION_TOOLS

   Support replay of persisted DIS messages in the application

.. req:: Re-emit DIS messages over the network
   :id: REQ_DIS_REEMIT
   :parent: REQ_DIS_INVESTIGATION_TOOLS

   Support re-emitting persisted DIS messages over the network to a configurable endpoint for integration with external tools.

.. req:: Export filtered datasets
   :id: REQ_DATA_EXPORT
   :parent: REQ_DIS_INVESTIGATION_TOOLS

   Support exporting the currently filtered view of DIS messages to standard data formats (e.g., CSV, JSON) for external analysis and reporting.












Implementation Choices
----------------------

These implementation choices support the high-level requirements without being the only way to satisfy them.

.. spec:: Paginated message loading
   :id: SPEC_PAGINATION_LIMITS
   :parent: SPEC_MESSAGES_PAGE, SPEC_HTMX_INTERACTIONS

   Implement strict pagination or HTMX-driven infinite scrolling limits on the messages page to prevent browser memory exhaustion when viewing millions of persisted rows.

.. spec:: Real-time ingestion metrics
   :id: SPEC_INGESTION_METRICS
   :parent: REQ_SYSTEM_HEALTH_LOGGING, SPEC_CONNECTION_INFORMATION

   Track and expose internal metrics for the UDP listener, including packets received per second, parse failures, and batch insert latency.


.. spec:: Optimized database indexing
   :id: SPEC_DB_INDEXING
   :parent: SPEC_SQLITE_WAL, REQ_SQL_QUERY_MODEL

   Maintain explicit database indexing on high-frequency query columns including Timestamp, PDU Type, Entity ID, and Exercise ID to ensure UI responsiveness.

.. spec:: Resilient malformed packet handling
   :id: SPEC_MALFORMED_PACKET_HANDLING
   :parent: SPEC_OPEN_DIS_PY

   Catch and log parser exceptions for malformed UDP packets without interrupting the main asyncio ingestion task or dropping healthy packets in the current batch.

.. spec:: Multicast and broadcast support
   :id: SPEC_MULTICAST_SUPPORT
   :parent: SPEC_CONNECTION_INFORMATION

   Ensure the UDP listener can be configured to join specific multicast groups or listen for general broadcast traffic on designated network interfaces.

.. spec:: Secure default binding
   :id: SPEC_LOCAL_BINDING
   :parent: REQ_MINIMAL_DEPLOYMENT_FRICTION

   Default the Django web server binding to localhost (127.0.0.1) to ensure the application remains a local desktop tool unless explicitly configured otherwise.



.. spec:: HTMX-driven lightweight interactions
   :id: SPEC_HTMX_INTERACTIONS
   :parent: REQ_WEB_FIRST_UX, REQ_NAVIGABLE_WITHOUT_JS

   Prefer HTMX for lightweight, declarative UI enhancements and incremental updates.

.. spec:: Django-based backend
   :id: SPEC_USE_DJANGO
   :parent: REQ_MINIMAL_DEPLOYMENT_FRICTION, SPEC_HTMX_INTERACTIONS

   Use Django for request handling, template rendering, and database management.

.. spec:: SQLite with WAL persistence
   :id: SPEC_SQLITE_WAL
   :parent: REQ_PERSISTENCE, SPEC_USE_DJANGO

   Use SQLite with write-ahead logging for local database persistence.

.. spec:: Batch insert at ~20Hz
   :id: SPEC_BATCH_INSERT_20HZ
   :parent: SPEC_SQLITE_WAL

   Batch insert PDUs at approximately 20 Hz to balance real-time ingestion with SQLite performance.

.. spec:: Live refresh at ~20Hz
   :id: SPEC_LIVE_REFRESH_20HZ
   :parent: SPEC_SQLITE_WAL

   Refresh web pages at approximately 20 Hz for live updates using HTMX.

.. spec:: Open-dis-python parsing
   :id: SPEC_OPEN_DIS_PY

   Use open-dis-python for DIS message parsing, serialization, and protocol compliance.

.. spec:: Disconnect and timeout detection
   :id: SPEC_TIMEOUT_DETECTION
   :parent: SPEC_CONNECTION_INFORMATION

   Mark entities as stale or inactive in the live view if no updated Entity State PDUs are received within a configurable timeout window.

.. spec:: Asynchronous task control API
   :id: SPEC_TASK_CONTROL_API
   :parent: SPEC_CONNECTION_INFORMATION, SPEC_HTMX_INTERACTIONS

   Expose endpoint controls via HTMX to trigger, pause, or terminate the background *db_worker* ingestion tasks from the user interface.

.. spec:: PDU payload binary storage
   :id: SPEC_BLOB_STORAGE
   :parent: SPEC_SQLITE_WAL, REQ_DIS_REEMIT

   Store the unaltered network bytes of every ingested DIS PDU in a dedicated BLOB column alongside the extracted field columns for absolute verification (and later re-emitting)

.. spec:: Static assets compilation
   :id: SPEC_STATIC_ASSETS
   :parent: REQ_MINIMAL_DEPLOYMENT_FRICTION

   Bundle all required frontend libraries (such as HTMX and Altair/Vega) locally within the Python package to avoid third-party CDN dependencies.

.. spec:: MIL-STD-2525 symbol mapping
   :id: SPEC_SYMBOL_MAPPING
   :parent: REQ_USE_STANDARD_SYMBOLS, REQ_DIS_INVESTIGATION_TOOLS

   Translate DIS Entity Type 7-character record values (Kind, Domain, Country, Category, Subcategory, Specific, Extra) into valid MIL-STD-2525 symbol identification codes.

.. spec:: Code-generation from XML PDU spec
   :id: SPEC_PDU_CODE_GENERATION
   :parent: REQ_SCHEMA_FLEXIBILITY, REQ_DIS_INVESTIGATION_TOOLS

   Use XSLT transformations to generate Django model code and summary field templates from the official DIS PDU XML specification to support maintainability and traceability.

Range Tool
~~~~~~~~~~

The range tool should be accessible from both the 3D map and the analysis plots, allowing users to select entities and visualize calculated relationships between them.

.. spec:: Range Tool UI
   :id: SPEC_RANGE_TOOL_UI
   :parent: REQ_RANGE_TOOL

   The range tool UI should be a separate page (embeddable in the 3D map, and also the PDU viewer) that allows users to select two or more entities and choose from a list of available calculations (slant range, bearing, closure rate, etc.) to visualize the results.

   The tool should be 3 sections - Top is entity selection, bottom-left is calculation type, and right is a list of active calculations with results. When a calculation is selected, the relevant entities and relationships should be highlighted in the 3D map and/or analysis plots.


Page Workflow Specifications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
   :parent: REQ_ANALYSIS_PLOTS

   Provide a plots page with lightweight summary visualizations such as PDU count per second, active entities over time, entity positions, and PDU type distribution.
   Render plots using Altair/Vega and derive visuals from the persisted message data.

.. spec:: 3D map view
   :id: SPEC_3D_MAP_VIEW
   :parent: REQ_3D_OPERATIONAL_MAP, REQ_SIMDIS_INSPIRED, REQ_TACVIEW_INSPIRED

   Provide a SIMDIS/TacView-style live 3D map page that renders translated entity and event state from persisted DIS PDUs. Honor existing filters by time range, PDU type, entity, parsed fields, and raw SQL so users can show only selected assets and platforms.

.. spec:: Playback Selection View
   :id: SPEC_PLAYBACK_SELECTION_VIEW
   :parent: REQ_DCS_FILE_REPLAY, REQ_SIMDIS_ASI_REPLAY, REQ_DIS_MESSAGE_REPLAY

   Provide a view for selecting from available DCS recording files and SIMDIS ASI files for replay, showing metadata such as scenario name, date, duration, and included entities.

.. spec:: DIS translation layer
   :id: SPEC_DIS_TRANSLATION_LAYER
   :parent: REQ_LAYERED_MAP_ARCHITECTURE, REQ_3D_OPERATIONAL_MAP

   Translate persisted DIS PDUs into scene-ready platform and event representations for the 3D map while keeping ingestion and storage separate from display rendering.

.. spec:: SIMDIS ASI file translation layer
   :id: SPEC_SIMDIS_ASI_TRANSLATION_LAYER
   :parent: REQ_LAYERED_MAP_ARCHITECTURE, REQ_3D_OPERATIONAL_MAP, REQ_SIMDIS_ASI_REPLAY

   Translate SIMDIS ASI file contents into scene-ready platform and event representations for the 3D map while keeping replay ingestion and storage separate from display rendering.

.. spec:: DCS file translation layer
   :id: SPEC_DCS_FILE_TRANSLATION_LAYER
   :parent: REQ_LAYERED_MAP_ARCHITECTURE, REQ_3D_OPERATIONAL_MAP, REQ_DCS_FILE_REPLAY

   Translate DCS recording file contents into scene-ready platform and event representations for the 3D map while keeping replay ingestion and storage separate from display rendering.

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


GRAPH VIEW
==========

.. needflow::
   :types: req, spec, test_case, code_impl
   :show_legend:
   :show_link_names:

