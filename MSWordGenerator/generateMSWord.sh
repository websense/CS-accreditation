#!/bin/bash
#Shell to generate selected tables as ms-word output as required in ACS checklist
#Assumes Setup.sh has been run to initialise the Python environment

echo "MS-WORD generator script"

source DirectoryNames.sh 

# Navigate to the project directory
cd $PROJECT_DIR

# Set up Python to find libraries
export PYTHONPATH="${PYTHONPATH}:$PROJECT_DIR:$KNOWLEDGEBASE_DIR"

# Check and clean output dirs, -f suppresses warnings
echo "Check output directories exist are ready and clean out old files ..."
mkdir $MSWORD_OUTPUT
rm -f $MSWORD_OUTPUT/*.docx




python3  $MSWORD_DIR/mswordGenerator.py

echo "MS-Word accreditation files created."   

exit 0
