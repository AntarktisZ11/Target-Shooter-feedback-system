#!/usr/bin/env python3

# ! Dont forget
# * chmod +x myscript.py

# Add the dir containing it to your PATH variable.
# (If you want it to stick, you'll have to do this in .bashrc or .bash_profile in your home dir.)

# * export PATH=/path/to/script:$PATH

import sys
import os
from typing import List
import urllib.request  # the lib that handles the url stuff
import urllib.error  # for error handling
from time import sleep


# * Is self-updating
# ! Does not remove any files

SITE = "https://raw.githubusercontent.com"
GITHUB_USER = "AntarktisZ11"
REPO_PARENT = "Target-Shooter-feedback-system/master/GUI"
BASE_URL = f"{SITE}/{GITHUB_USER}/{REPO_PARENT}/"

linux = False
if sys.platform == "linux":
    linux = True

if linux:
    LOCAL_PROJECT_FOLDER = os.path.split(__file__)[0]
else:
    LOCAL_PROJECT_FOLDER = (
        r"C:/Users/Marcus Börne/Desktop/Python Projects/L-O/Target-Shooter-feedback-system/GUI/temp2/"
    )


RECEIVER_FILES = [
    "update_function.py",  # Must always exist
    "receiver_update_script.py",  # Must always exist
    "receiver.py",
    "receiver_support.py",
    "figureGen.py",
    "socket_stuff/BaseSocket.py",
    "socket_stuff/ReceiverSocket.py",
]

SENDER_FILES = [
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


class File:
    """Class for handeling information of file content"""

    cached_text: bytes
    filepath: str
    file_location: str

    def __init__(self, filepath: str) -> None:
        """Class for handeling information of file content

        Args:
            filepath (str): Filepath to file from GUI folder
        """
        self.filepath = filepath
        self.file_location = os.path.join(LOCAL_PROJECT_FOLDER, filepath)

    def cache_online_text(self):
        """Find text of filepath from github repository

        Raises:
            ConnectionError: Raised when request to url fails

        Returns:
            Bool: Returns True successfull
        """
        url = BASE_URL + self.filepath
        try:
            text = b""
            for line in urllib.request.urlopen(url, timeout=5):
                text += line
            self.cached_text = text
        except urllib.error.HTTPError:
            print(f"URL could not be found: {url}")
            return False
        except urllib.error.URLError:
            raise ConnectionError("Network connection bad or non-existent")

        return True

    def content_differs(self) -> bool:
        """Checks if file was different between local file system and git repo

        Returns:
            Bool: Returns True if file was different or new
        """
        if not os.path.isfile(self.file_location):
            print(f"{self.filepath} was new!")
            return True

        with open(self.file_location, "rb") as file:
            if file.read() != self.cached_text:
                print(f"{self.filepath} was modified!")
                return True

        return False

    def update_file(self):
        """Write cached content to file"""
        if len(self.cached_text) == 0:
            raise ValueError("There is no cached content to write to file")

        # Create subdirectory if needed
        dir, _ = os.path.split(self.file_location)
        os.makedirs(dir, exist_ok=True)

        with open(self.file_location, "wb") as file:
            file.write(self.cached_text)


class Updater:

    changed_files: List[str]
    update_files = ["update_function.py", "receiver_update_script.py", "sender_update_script.py"]

    def __init__(self, files_to_update: List[str]) -> None:
        """Interface from which you update the given files from github repository
        https://github.com/AntarktisZ11/Target-Shooter-feedback-system/tree/master/GUI

        Args:
            files_to_update (List[str]): Files to find in repository and update or create locally
        """
        self.files = [File(filepath) for filepath in files_to_update]

    def run(self, reboot: bool = True):
        """Run through all files checking if they need to be updated

        Args:
            reboot (bool, optional): Reboots if any update file has been changed. ONLY LINUX!!! Defaults to True.
        """
        files = [f for f in self.files if f.cache_online_text()]

        self.changed_files = []
        for f in files:
            if f.content_differs():
                f.update_file()
                self.changed_files.append(f.filepath)

        print("Update completed!")

        # if reboot and linux and [f for f in self.changed_files if f in self.update_files]:
        #     os.system("sudo reboot")

    @staticmethod
    def connected(max_retries: int = 20, timeout: float = 1):
        """Check if internet is connected and retry with set interval until it is

        Args:
            max_retries (int, optional): Times to retry establishing connection. Defaults to 20.
            timeout (float, optional): Wait time between retries. Defaults to 1.

        Returns:
            bool: True if internet access was aquired, else False
        """
        retry = 0
        while retry < max_retries:
            try:
                urllib.request.urlopen("https://www.google.com/")
                return True
            except urllib.error.URLError:
                retry += 1
                sleep(timeout)

        return False


if __name__ == "__main__":
    # Files which will be updated
    filenames = ["receiver.py", "receiver_support.py", "figureGen.py", "update_function.py", ""]
    filenames.append("receiver_update_script.py")  # Must always exist

    print("Pre-check")
    if Updater.connected():
        print("Pre-run")
        Updater(filenames).run()
    else:
        raise ConnectionError("Network connection bad or non-existent")
    print("Exiting")
