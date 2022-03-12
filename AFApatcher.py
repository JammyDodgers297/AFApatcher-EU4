# This program is designed to remove all requirements for building and using monuments in EU4 from the config files. Inspired by Great Monuments Expanded - All For All. 
# It should (hopefully) work for any monument file from any mod (I have only tested it with Flavor Universalis at time of writing. Will likely try it with VU at some point). 
# I made it to make it less tedious to remove the requirements so I could build every monument I conquered.
# Made for Python 3.8 on Windows 10

# To use, run python script from command line with name/directory of monument file as an argument: $ python3 "AFApatcher.py" "01_monuments.txt"

import sys

testFile = open(sys.argv[1], "r+")
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

    # These are the terms we want to delete the contents from
    if "build_trigger" in line:
        delete = True
    if "can_use_modifiers_trigger" in line:
        delete = True
    if "can_upgrade_trigger" in line:
        delete = True
    if "keep_trigger" in line:
        delete = True
    
    if "{" in line: 
        inceptionCount += 1

    # If statement to make the necessary changes to the relevant lines
    newLine = ""
    if delete and inceptionCount == 2:
        if "{" in line:
            opening = line.index("{")
            newLine += line[:opening+1]
            newLine += "}\n"
    # Deleting the contents of the brackets
    elif delete and inceptionCount > 2:
        newLine = ""
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
