#!/bin/bash
#Shell to generate html output
#Assumes setup.sh has been run to initialise the Python environment
#source setup.sh

echo "HTML generator script"

source DirectoryNames.sh 

# Navigate to the project directory
cd $PROJECT_DIR

# Set up Python to find libraries
export PYTHONPATH="${PYTHONPATH}:$PROJECT_DIR:$KNOWLEDGEBASE_DIR"

# Remove all previous files from output directory
rm -f $HTML_OUTPUT/*


# Copy main html files from input directory to the html output directory (except the ProgramTemplate not needed)
# and create index.html for launch from github pages
cp $HTML_INPUTS/* $HTML_OUTPUT
rm -f $HTML_OUTPUT/Program-Template.html
cp $HTML_OUTPUT/ProgramsHomePage.html $HTML_OUTPUT/index.html 

# Generate html tables outputs from the knowledgebase and insert them into program templates
python3 $HTML_DIR/htmlGenerator.py

# Make all output dir files read-only (to avoid confusion about editing these)
chmod 444 $HTML_OUTPUT/*



echo "Html accreditation files created."   
echo "All required html source files copied as read-only files to output directory." 
echo "Open AccreditationHome.html in a browser to view"


exit 0


