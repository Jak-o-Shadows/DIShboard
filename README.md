# DIShboard
A  web application for ingesting, storing, visualizing, sorting, and filtering DIS (Distributed Interactive Simulation) messages.

## Design Goals
DIShboard is intended to be a simple, extensible observer for live DIS traffic with a focus on fast local analysis and data-driven filtering.

Core goals:
 * Web-first UX: build the interface as a responsive web application with server-rendered pages and progressive enhancement.
 * HTMX-driven interactions: use HTML as the primary state carrier and keep dynamic interactions lightweight and declarative.
 * Persistence: ingest DIS messages in real time and persist them to a local SQL database so filtering and replay can be efficient.
 * SQL-first query model: support both raw SQL filtering and higher-level query helpers so analysts can search by fields, time, entity, and PDU type.
 * Schema flexibility: avoid hard-coding every PDU type
 * Separation of concerns: keep message ingestion, storage, and UI rendering distinct enough to evolve independently.
 * Minimal deployment friction: install as a standard Python package, run locally, and use simple tooling for development and documentation.
 * Make the UI fully navigable without JavaScript when possible, while enhancing interactions with HTMX.
 * Cross-platform

Non-goals for the initial version:
 * Replay of DIS
 * A fully offline browser-only app; a lightweight backend is acceptable for UDP ingestion and database persistence.
 * Map view (probably using cesium JS)

### Architecture Principles
 * Keep the backend thin: ingest messages, store them, and render HTML pages.
 * Keep the frontend simple: HTML templates, HTMX requests, and a small (tiny)amount of client-side behavior.
 * Prefer explicit state: use query parameters, form submissions, and URL-driven navigation rather than hidden client-side state.
 * Store each PDU type in a separate table for schema flexibility and efficient querying.
 * Store raw payloads: preserve the original message content and add parsed fields for filtering and display. The raw payload as a blob, and the parsed PDU fields as columns
 * Support extensibility: allow new PDU types and visualizations to be added without rewriting the core database schema by hand.
 * Use open-dis-python for DIS message parsing, serialization, and protocol compliance.
 * Use Django as the web framework for handling requests, rendering templates, and managing the database.
 * Use SQLite with write-ahead logging for local database persistence.
 * Batch insert PDUs at approximately 20 Hz (ish) to balance real-time ingestion with performance.
 * Refresh web pages at approximately 20 Hz (ish) for live updates using HTMX.

#### Task Framework for DIS Ingestion
DIShboard uses [django-tasks-db](https://github.com/RealOrangeOne/django-tasks-db) as the task backend to manage asynchronous operations, particularly for UDP ingestion of DIS PDUs. This ORM-based system stores tasks in the main Django database, removing the need for external queue managers like Celery.

- **UDP Listener as a Task**: The DIS PDU receiver runs as a background task using `asyncio` for non-blocking UDP socket operations. It buffers incoming PDUs in memory and batch-inserts them into the database at approximately 20 Hz to handle high-volume traffic (up to ~10,000 PDUs/s) without overwhelming SQLite.
- **Task Management**: Configure tasks in `settings.py` with queues (e.g., "dis-ingestion"). Run the worker via `./manage.py db_worker --queues dis-ingestion` to process tasks asynchronously.
- **Benefits**: Simplifies async handling, ensures persistence of task state, and allows for easy monitoring and pruning of completed tasks using built-in management commands.

This keeps the architecture aligned with the "Separation of concerns" and "Minimal deployment friction" goals, while enabling real-time, scalable ingestion.

## Pages
The application should include a small set of focused pages that reflect common DIS analysis workflows.

#### Connection Information
 * Display current connection status and transport configuration.
 * Show recent connection events, packet rate, and basic packet-level health indicators.
 * Provide controls to start/stop listening and to configure the source endpoint or file replay.

#### Messages
 * Show an incoming message stream with sortable, filterable rows.
 * Support live refresh, incremental loading, and paging for large message volumes.
 * Provide filters by time range, PDU type, source entity, and parsed PDU values.
 * Allow raw SQL queries for advanced filtering alongside form-based controls.
 * Preserve selected filters and list state in the URL so results are shareable and repeatable.

#### Plots
 * Provide simple summary visualizations for operational insight.
 * Examples:
   * PDU count per second
   * Active entities over time
   * Entity positions on a map-style coordinate plot
   * PDU type distribution and trends
 * Keep plots lightweight and declarative, using Altair/Vega - client side rendering for interactivity.
 * Enable plot generation from the same persisted message data that powers the message browser.

## Install Goals
 * Package the project with a standard `pyproject.toml` configuration.
 * Use modern Python packaging conventions and avoid legacy `setup.py` usage.
 * Document the project with Sphinx for both API documentation and user-facing guidance.

## Future Goals
 * Support replay mode: ingest previously captured DIS traffic from a file or recording.
 * Add richer analytics and saved filter sets for repeated investigations.
 * Investigate a browser-only visualization mode once raw UDP capture is solved by external bridge or native capabilities.


## Developing

To run:

python src/manage.py runserver
python src/manage.py db_worker