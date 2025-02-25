#!/bin/bash
#Shell to generate all outputs for accreditation manager on MAC OS

#set up names for directory structure
source DirectoryNames.sh

# make clean versions of all directories
rm -r $OUTPUT_DIR
mkdir $OUTPUT_DIR
mkdir $EXCEL_OUTPUT
mkdir $EXCEL_PROGRAMS_OUTPUT
mkdir $EXCEL_UNITS_OUTPUT
mkdir $HTML_OUTPUT
mkdir $LATEX_OUTPUT
mkdir $LATEX_TABLES_OUTPUT

# Generate latex, excel and html outputs by running all scripts

python3 $KNOWLEDGEBASE_DIR/knowledgebase.py

bash $LATEX_DIR/generateLatex.sh
bash $HTML_DIR/generateHTML.sh
bash $EXCEL_DIR/generateExcel.sh