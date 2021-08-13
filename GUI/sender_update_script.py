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

print("Pre-check")
if Updater.connected():
    print("Pre-run")
    Updater(filenames).run()
else:
    raise ConnectionError("Network connection bad or non-existent")
print("Exiting")
