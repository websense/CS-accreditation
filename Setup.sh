#!/bin/bash
#Shell to set up Python environment for accreditation manager on MAC OS

# load common shell vars for project directory structure
source DirectoryNames.sh

#Step 1: Start in project base directory
cd $PROJECT_DIR

# Check python version
## I was running Python 3.9.6 which does not support latest numpty==2.1.0. so updated to 3.13
#python3 --version

# Copy input files from ground truth sources (edited by others): overleaf for latex and ms-teams for knowledgebase and other xlsx
echo ""
echo "Knowledge source documents are updated in ms-teams Accreditation 2025."
read -p "Confirm. Are documents in InputDocs/*.sxlsx the most recent ms-teams versions? y/n: " a
if [ $a != "y" ]
then
	echo "Please update input documents then run Setup again"
	exit 0
fi
ls -l InputDocs/*.xlsx

# Copy input files from ground truth sources (edited by others): overleaf for latex and ms-teams for knowledgebase and other xlsx
echo ""
echo "Latex source documents are updated in Overleaf."
read -p "Confirm: Are documents in InputDocs/LatexInputs the most recent overleaf versions? y/n: " a
if [ $a != "y" ]
then
	echo "Please update input documents then run Setup again"
	exit 0
fi
ls -l InputDocs/LatexInputs/*

# Step 3: Install required dependencies (optional if already installed)
echo "Installing dependencies..."
pip3 -q install -r requirements.txt

# Step 4: Create and Activate a virtual environment (using Python3.13 so it is set as default)
echo "Create and activating virtual environment..."
virtualenv --python="/Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13" "$PROJECT_DIR/venv"

python3 -m venv venv


# Now ready to run scripts
echo ""
echo ""
echo "Set up complete.  You can now run generator scripts (see shell scripts in xxGenerator directories) using:"
echo "source DirectoryNames.sh"
#echo "source $PROJECT_DIR/venv/bin/activate"


