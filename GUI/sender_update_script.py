import sys
import os
import urllib.request  # the lib that handles the url stuff

#* Is self-updating
#! Does not remove any files

# Files which will be updated
filenames = ["sender.py", "sender_support.py", "pdflatex.py", "figureGen.py", "template.tex"]
filenames.append("sender_update_script.py") # Must always exist

site = "https://raw.githubusercontent.com"
github_user = "AntarktisZ11"
repo_parent = "Target-Shooter-feedback-system/master/GUI"
base_url = f'{site}/{github_user}/{repo_parent}/'

if sys.platform == "linux":
    prog_call = sys.argv[0]
    prog_location = os.path.split(prog_call)[0]
    local_project_folder = prog_location
else:
    local_project_folder = r"C:/Users/Marcus Börne/Desktop/Python Projects/L-O/Target-Shooter-feedback-system/GUI/temp/"

for filename in filenames:
    url = base_url + filename

    file_text = b''
    for line in urllib.request.urlopen(url):
        file_text += line

    with open(local_project_folder+filename, 'wb') as file:
        file.write(file_text)
