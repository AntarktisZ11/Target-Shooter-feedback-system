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


# * Is self-updating
# ! Does not remove any files

SITE = "https://raw.githubusercontent.com"
GITHUB_USER = "AntarktisZ11"
REPO_PARENT = "Target-Shooter-feedback-system/master/GUI"
BASE_URL = f"{SITE}/{GITHUB_USER}/{REPO_PARENT}/"

if sys.platform == "linux":
    LOCAL_PROJECT_FOLDER = os.path.split(__file__)[0]
else:
    LOCAL_PROJECT_FOLDER = (
        r"C:/Users/Marcus Börne/Desktop/Python Projects/L-O/Target-Shooter-feedback-system/GUI/temp2/"
    )


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
            for line in urllib.request.urlopen(url):
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
    def __init__(self, files_to_update: List[str]) -> None:
        """Interface from which you update the given files from github repository
        https://github.com/AntarktisZ11/Target-Shooter-feedback-system/tree/master/GUI

        Args:
            files_to_update (List[str]): Files to find in repository and update or create locally
        """
        self.files = [File(filepath) for filepath in files_to_update]

    def run(self):
        """Run through all files checking if they need to be updated"""
        files = [f for f in self.files if f.cache_online_text()]

        for f in files:
            if f.content_differs():
                f.update_file()


if __name__ == "__main__":
    # Files which will be updated
    filenames = ["receiver.py", "receiver_support.py", "figureGen.py", "update_function.py", ""]
    filenames.append("receiver_update_script.py")  # Must always exist

    Updater(filenames).run()
