#!/usr/bin/env python3

from update_function import Updater

# Files which will be updated
filenames = [
    "update_function.py",  # Must always exist
    "sender_update_script.py",  # Must always exist
    "sender.py",
    "sender_support.py",
    "sender_extra_windows.py",
    "figureGen.py",
    "pdflatex.py",
    "template.tex",
    "socket_stuff/BaseSocket.py",
    "socket_stuff/SenderSocket.py",
]

Updater(filenames).run()
