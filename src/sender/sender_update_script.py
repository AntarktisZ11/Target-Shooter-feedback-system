#!/usr/bin/env python3

# Standard Library
import importlib
import os
import sys
from typing import List

# First-Party
import update_function


def run() -> List[str]:
    """Runs update loop and reloads update_function module
    to add new files avoiding unecessary reboot

    Raises:
        ConnectionError: IFF internet access was not aquired
        within certain timeframe (Default 20s)

    Returns:
        List[str]: List of all files which had been changed or added
    """
    importlib.reload(update_function)
    # First-Party
    from update_function import SENDER_FILES, Updater

    print("Pre-check")
    if Updater.connected():
        print("Pre-run")
        updater = Updater(SENDER_FILES)
        updater.run()
        return updater.changed_files
    else:
        raise ConnectionError("Network connection bad or non-existent")


changed_files = run()
if "update_function.py" in changed_files:
    changed_files += run()  # Runs again with new module content

if changed_files and sys.platform == "linux":
    os.system("sudo reboot")


print("Exiting")
