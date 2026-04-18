# DIShboard
Program to listen to DIS (Distributed Interactive Simulation) messages, and allow them to be visualised, sorted, and filtered.

## Design
 * Should be a web-app
 * HTMX for the GUI
 * Messages stored immediately into a SQL database to enable filtering via SQL
 * GUI should enable raw SQL input for filters, as well as something more human friendly
 * Should be one SQL table per PDU type
 * Should NOT have to be all hard-coded

### Pages
There are multiple pages available to the user. Note that we want HTML to be the agent of state HATEOS - so avoid doing any

#### Connection Information
 // TODO

#### Messages
 * Where messages are displayed as they come in

#### Plots
 * Where some limited plots are shown
 * This is to be developed after the messages page
 * Plots are written in altair (ie. vega)
 * Example plot types include
   * PDU's per second
   * Entities alive
   * Entities position (on a map)
   * PDU type per second

### Install Goals
 * Should be an installable python project. Uses pyproject.toml, as it is the year 2026 (and hence setup.py should not be used). Is documented using Sphinx - both for the basic API docs, but also some long-form documentation (that should be moved out of here). Said long form documentation will be rendered to HTML and also served.

## Future Goals
 * Wholly contained in the web-page - no backend
   * Not possibly currently as webpages cannot listen or send on raw UDP
 * Replay
