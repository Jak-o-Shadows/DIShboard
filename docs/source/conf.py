# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys


project = 'DIShboard'
copyright = '2026, Jak-o-Shadows'
author = 'Jak-o-Shadows'

# Tell Sphinx to look inside your "src" directory for your Python modules
sys.path.insert(0, os.path.abspath("../src"))

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_needs",
    "sphinx_codelinks",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "autoapi.extension",
    "sphinx.ext.graphviz"
]

templates_path = ['_templates']
exclude_patterns = []

########## Sphinx-AutoAPI configuration ##########
autosummary_generate = True
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "inherited-members": True,
}
autoapi_type = "python"
autoapi_dirs = [os.path.abspath("../../src")]
autoapi_root = "api"
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "imported-members",
]
autoapi_keep_files = True
autoapi_add_toctree_entry = False



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']


# Sphinx-Needs configuration via ubCode
# Need both for it to work with Sphinx, rather than just ubCode
needs_from_toml = "ubproject.toml"
src_trace_config_from_toml = "ubproject.toml"

# Must switch between graphviz & plantUML, depending on whether we are doing latex export or not
build_type = sys.argv[2]  # This is not a great way, but is easy - see https://stackoverflow.com/a/65849575
match build_type:
    case "latex":
        needs_flow_engine = "graphviz" # Can't get a workign install of plantUML with other deps
        #needs_flow_engine = "plantuml"  # Doing latex export, so plantUML is required
        #extensions.append("sphinxcontrib.plantuml")
    case "html":
        needs_flow_engine = "graphviz"  # Not doing latex export, so graphviz is better
    case _:
        needs_flow_engine = "graphviz"  # More likely to be installed?



