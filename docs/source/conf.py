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
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']


# Sphinx-Needs configuration via ubCode
# Need both for it to work with Sphinx, rather than just ubCode
needs_from_toml = "ubproject.toml"
src_trace_config_from_toml = "ubproject.toml"