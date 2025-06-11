#!/bin/bash
#!/usr/bin/python3.13
#Shell to generate latex output
#Assumes setup.sh has been run to initialise the Python environment


echo "LATEX generator script"

source DirectoryNames.sh 

# Navigate to the project directory
cd $PROJECT_DIR

# Set up Python to find libraries
export PYTHONPATH="${PYTHONPATH}:$PROJECT_DIR:$KNOWLEDGEBASE_DIR"

# Remove all previous files from output directory
rm -f $LATEX_OUTPUT/CSSE-ACS-Accreditation*
rm -f $LATEX_OUTPUT/*.tex
rm -f $LATEX_OUTPUT/*.sty
rm -f $LATEX_OUTPUT/*.jpg
rm -f $LATEX_TABLES_OUTPUT/*.tex

# Copy main latex files and image files from input directory to the latex output directory
cp $LATEX_INPUTS/*.tex $LATEX_OUTPUT
cp $LATEX_INPUTS/*.sty $LATEX_OUTPUT
cp $LATEX_INPUTS/*.jpg $LATEX_OUTPUT


# Generate latex tables outputs from the knowledgebase and put them in the tables output directory
python3 $LATEX_DIR/latexGenerator.py

# Make all output dir files read-only (to avoid confusion about editing these)
# chmod 444 $LATEX_OUTPUT/*.*
# chmod 444 $LATEX_TABLES_OUTPUT/*.tex
# chmod 666 $LATEX_TABLES_OUTPUT
# chmod 666 $LATEX_OUTPUT

echo "Latex library files created."   
echo "All required latex source files copied as read-only files to $LATEX_OUTPUT"
echo "Open index.html"


exit 0
