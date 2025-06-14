#!/bin/bash
#Shell to generate excel output
#Assumes Setup.sh has been run to initialise the Python environment

echo "EXCEL generator script"

source DirectoryNames.sh 

#Problems - python path not found problem in venv environment?
#echo "This shell should be run in the venv created by Setup.sh"
#echo "To start run:"
#echo "source venv/bin/activate"
#echo " "
#echo " "

# Navigate to the project directory
cd $PROJECT_DIR

# Set up Python to find libraries
export PYTHONPATH="${PYTHONPATH}:$PROJECT_DIR:$KNOWLEDGEBASE_DIR"

# Check and clean output dirs, -f suppresses warnings
echo "Check output directories are ready and clean out old files ..."
rm -f $EXCEL_OUTPUT/Programs/*.xlsx
rm -f $EXCEL_OUTPUT/Units/*.xlsx
rm -f  $EXCEL_OUTPUT/UnitProgramMappings/*.xlsx

mkdir $EXCEL_PROGRAMS_OUTPUT
mkdir $EXCEL_UNITS_OUTPUT
mkdir $EXCEL_UNITPROG_OUTPUT

python3  $EXCEL_DIR/excelGenerator.py

echo "Excel accreditation files created."   

exit 0
