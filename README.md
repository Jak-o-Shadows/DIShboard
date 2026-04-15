# DIShboard
Program to listen to DIS (Distributed Interactive Simulation) messages, and allow them to be visualised, sorted, and filtered.

## Design
 * Should be a web-app
 * HTMX for the GUI
 * Messages stored immediately into a SQL database to enable filtering via SQL
 * GUI should enable raw SQL input for filters, as well as something more human friendly
 * Should be one SQL table per PDU type
 * Should NOT have to be all hard-coded

## Future Goals
 * Wholly contained in the web-page - no backend
   * Not possibly currently as webpages cannot listen or send on raw UDP
 * Replay
