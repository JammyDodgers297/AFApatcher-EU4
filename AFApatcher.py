# This program is designed to remove all requirements for building and using monuments in EU4 from the config files. Inspired by Great Monuments Expanded - All For All. 
# It should (hopefully) work for any monument file from any mod (I have only tested it with Flavor Universalis at time of writing. Will likely try it with VU at some point). 
# I made it to make it less tedious to remove the requirements so I could build every monument I conquered.
# Made for Python 3.8 on Windows 10

# UPDATED 
# To use: drag all monument files to be AFA'd into the "Files To Patch" directory (If it doesn't exist run the patcher once and it will create it) 
# Run the patcher (by double clicking or from console)
# The monument requirements should be removed from all of the files

import sys, os, shutil

# Gets the absolute path of the folders where the files are found
patcherDir = os.path.abspath(os.path.dirname(__file__))
fileDir = os.path.join(patcherDir, "Files To Patch")
backupDir = os.path.join(patcherDir, "Old")

# Creates the folders if they do not exist
if not os.path.exists(fileDir):
    os.makedirs(fileDir)
if not os.path.exists(backupDir):
    os.makedirs(backupDir)

# Empties "Old" folder
for file in os.listdir(backupDir):
    fileToRemove = os.path.join(backupDir, file)
    os.remove(fileToRemove)

# Creates backups of the files being patched in the "Old" folder
shutil.copytree(fileDir, backupDir, dirs_exist_ok=True)

# Loop to repeat program for all files in "Files To Patch" folder
for file in os.listdir(fileDir):
    if file.endswith('.txt'):
        filePath = os.path.join(fileDir, file)
        testFile = open(filePath, "r+")
        newFile = []
        delete = False
        inceptionCount = 0
        fixMonument = []
        inMonument = False

        for line in testFile:
            # inceptionCount is keeping track of which level of brackets we are in, so that we only delete the contents of relevant brackets
            if inceptionCount == 0 and "{" in line:
                inMonument = True
                fixMonument = []

            # These are the terms we want to delete the contents from (not tested but should be possible to add more terms here to mass edit/delete from)
            patchTerms = [
                "build_trigger", 
                "can_use_modifiers_trigger", 
                "can_upgrade_trigger", 
                "keep_trigger"
                ]

            for term in patchTerms:
                if term in line:
                    delete = True
            
            if "{" in line: 
                inceptionCount += 1

            # If statement to make the necessary changes to the relevant lines
            newLine = ""
            if delete and inceptionCount == 2:
                if "{" in line:
                    opening = line.index("{")
                    newLine += line[:opening+1]
                    # Special case for build trigger. Will need to manually edit for some buildings such as canals
                    if "build_trigger" in line:
                        newLine += " always = yes"
                    newLine += " }\n"
            # Deleting the contents of the brackets
            elif delete and inceptionCount > 2:
                newLine = ""
            # Change date that monuments are built to game start
            elif "date" in line and "=" in line and inceptionCount == 1:
                opening = line.index("=")
                newLine += line[:opening+1]
                newLine += " 1.01.01\n"
            # If no changes are needed then the new line is the same as the old
            else: 
                newLine = line

            # Creates a list of each line of config for every monument
            # Needed to do this to stop all the indentation and spacing from being deleted between monuments
            fixMonument.append(newLine)

            # Ending delete portion and deincepting
            if "}" in line:
                inceptionCount -= 1
            if inceptionCount <= 1:
                delete = False

            # Once it reaches the closing bracket of a monument object, it will remove empty spaces in the list
            # It then appends the revised object to the master list that will overwrite the file
            if inceptionCount == 0 and "}" in line:
                fixMonument = list(filter(None, fixMonument))
                for l in fixMonument:
                    newFile.append(l)
                inMonument = False
            
            # This is the line that preserves the spacing between monuments
            # inMonument should always be true when inceptionCount is 0 but keeping both here for redundancy
            elif inceptionCount == 0 and not inMonument:
                newFile.append(line)

        # Overwriting the file with edited monuments
        testFile.seek(0)
        for line in newFile:
            testFile.write("%s" % line)
        testFile.truncate()
        testFile.close()
