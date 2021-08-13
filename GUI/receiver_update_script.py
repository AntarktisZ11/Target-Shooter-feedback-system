#!/usr/bin/env python3

from update_function import Updater

# Files which will be updated
filenames = [
    "update_function.py",  # Must always exist
    "receiver_update_script.py",  # Must always exist
    "receiver.py",
    "receiver_support.py",
    "figureGen.py",
    "socket_stuff/BaseSocket.py",
    "socket_stuff/ReceiverSocket.py",
]

if Updater.connected():
    Updater(filenames).run()
else:
    raise ConnectionError("Network connection bad or non-existent")
