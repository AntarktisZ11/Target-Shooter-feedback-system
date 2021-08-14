#!/usr/bin/env python3

import importlib
import os
import sys
import update_function


def run():
    importlib.reload(update_function)
    from update_function import Updater, RECEIVER_FILES

    print("Pre-check")
    if Updater.connected():
        print("Pre-run")
        updater = Updater(RECEIVER_FILES)
        updater.run()
        return updater.changed_files
    else:
        raise ConnectionError("Network connection bad or non-existent")


changed_files = run()
if "update_function.py" in changed_files:
    run()  # Runs again with new module content
    if sys.platform == "linux":
        os.system("sudo reboot")


print("Exiting")
