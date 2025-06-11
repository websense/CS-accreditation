#!/bin/bash
# Directory structure for accreditation mapper project
# This file should be sourced by each project script

PROJECT_DIR="."

## Project Input Documents
INPUT_DIR=$PROJECT_DIR/InputDocs
KNOWLEDGEBASE_FILE="Sample-ACS-Knowledgebase.xlsx"


LATEX_INPUTS=$INPUT_DIR/latexInputs
LATEX_PROG_TEMPLATE=$LATEX_INPUTS/Program-Template.tex
HTML_INPUTS=$INPUT_DIR/htmlInputs
HTML_PROG_TEMPLATE=$HTML_INPUTS/Program-Template.html

## Project Output Documents

OUTPUT_DIR=$PROJECT_DIR/OutputDocs
EXCEL_OUTPUT=$OUTPUT_DIR/excelDocs
EXCEL_PROGRAMS_OUTPUT=$EXCEL_OUTPUT/Programs
EXCEL_UNITS_OUTPUT=$EXCEL_OUTPUT/Units

HTML_OUTPUT=$OUTPUT_DIR/htmlDocs
LATEX_OUTPUT=$OUTPUT_DIR/latexDocs
LATEX_TABLES_OUTPUT=$OUTPUT_DIR/latexDocs/Tables
MSWORD_OUTPUT=$OUTPUT_DIR/msWordDocs


## Project Scripts: shell scripts and Python scripts for processing data

KNOWLEDGEBASE_DIR=$PROJECT_DIR/KnowledgeBaseGenerator
EXCEL_DIR=$PROJECT_DIR/ExcelGenerator
LATEX_DIR=$PROJECT_DIR/LatexGenerator
HTML_DIR=$PROJECT_DIR/HTMLGenerator
MSWORD_DIR=$PROJECT_DIR/MSWordGenerator

cd $PROJECT_DIR

## Copy the directory names into config.json for Python scripts to use
## TODO use the dir variables above in config file
echo '{
    "inputDocsDir": "InputDocs/",
    "knowledgeInputFile" : "Sample-ACS-Knowledgebase.xlsx",
    "staffCVsFile": "Sample-School-Staff-Table.xlsx",
     "IAPFile": "Sample-IAP-Members.xlsx",
    "excelProgramsOutput": "/OutputDocs/excelDocs/Programs/",
    "excelUnitsOutput": "/OutputDocs/excelDocs/Units/",
    "latexProgramTemplate": "/InputDocs/latexInputs/Program-Template.tex",
    "latexOutput": "/OutputDocs/latexDocs/",
    "latexTablesOutput": "/OutputDocs/latexDocs/Tables/",
    "htmlProgramTemplate": "/InputDocs/htmlInputs/Program-Template.html",
    "htmlOutput": "/OutputDocs/htmlDocs/",
    "msWordOutput": "/OutputDocs/msWordDocs/"
}' > config.json


