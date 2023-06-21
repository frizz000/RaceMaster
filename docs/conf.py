# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('../'))


project = 'RaceMaster'
copyright = '2023, Piotr Jałocha & Mateusz Kotula'
author = 'Piotr Jałocha & Mateusz Kotula'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode', 'sphinx.ext.autosummary']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Autodoc configurations --------------------------------------------------
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'imported-members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'exclude-members': '__weakref__',
    'show-inheritance': True,
    'ignore-module-all': True
}

autosummary_generate = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
