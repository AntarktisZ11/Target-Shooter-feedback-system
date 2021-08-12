#!/usr/bin/env python3

from update_function import Updater

# Files which will be updated
filenames = [
    "update_function.py",  # Must always exist
    "sender_update_script.py",  # Must always exist
    "sender.py",
    "sender_support.py",
    "figureGen.py",
    "pdflatex.py",
    "template.tex",
]

Updater(filenames).run()
