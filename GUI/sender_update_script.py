import os
import urllib.request  # the lib that handles the url stuff

# Files which will be updated
filenames = ["sender.py", "sender_support.py", "pdflatex.py", "figureGen.py", "template.tex"]

site = "https://raw.githubusercontent.com"
github_user = "AntarktisZ11"
repo_parent = "Target-Shooter-feedback-system/master/GUI"
base_url = f'{site}/{github_user}/{repo_parent}/'

local_project_folder = r"C:/Users/Marcus Börne/Desktop/Python Projects/L-O/Target-Shooter-feedback-system/GUI/temp/"

for filename in filenames:
    url = base_url + filename

    file_text = b''
    for line in urllib.request.urlopen(url):
        file_text += line
        
    with open(local_project_folder+filename, 'wb') as file:
        file.write(file_text)
