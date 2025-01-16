#!/bin/bash
# Directory structure for accreditation mapper project
# This file should be sourced by each project script

PROJECT_DIR="./"
#"/Users/00047104/Dropbox/CSSE-accreditations/Accreditation-Documenter-Project-2024/accreditation_mapper_master_october2024"


## Project Input Documents
INPUT_DIR=$PROJECT_DIR/InputDocs
KNOWLEDGEBASE_FILE="CSSE-allprograms-outcome-mappings-20241209.xlsx"
UNITOUTCOMES_FILE="CITS-units-outcomes-assessments.xlsx". #and PHIL units but STAT still TODO
MAJORS_OUTCOMES_FILE="Undergrad-majors-outcomes.xlsx"
MIT_OUTCOMES_FILE="MIT-outcomes.xlsx"



CAIDI_INPUTS=$INPUT_DIR/caidiReports
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

## Project Scripts: shell scripts and Python scripts for processing data

KNOWLEDGEBASE_DIR=$PROJECT_DIR/KnowledgeBaseGenerator
EXCEL_DIR=$PROJECT_DIR/ExcelGenerator
LATEX_DIR=$PROJECT_DIR/LatexGenerator
HTML_DIR=$PROJECT_DIR/HTMLGenerator

cd $PROJECT_DIR

## Copy the directory names into config.json for Python scripts to use
## TODO use the dir variables above in config file
## note needed    "latexMappingTemplate": "/InputDocs/latexInputs/Outcomes-Map-Template.tex",
echo '{
    "inputDocsDir": "InputDocs/",
    "knowledgeInputFile" : "CSSE-allprograms-outcome-mappings-20241209.xlsx",
    "staffCVsFile": "ACS-School-Staff-Table.xlsx",
    "caidiInputDocsDir": "InputDocs/caidiReports/",
    "unitoutcomesFile" : "CITS-units-outcomes-assessments.xlsx",
    "majorsoutcomesFile": "Undergrad-majors-outcomes.xlsx",
    "MIToutcomesFile" : "MIT-outcomes.xlsx",
    "excelProgramsOutput": "/OutputDocs/excelDocs/Programs/",
    "excelUnitsOutput": "/OutputDocs/excelDocs/Units/",
    "latexProgramTemplate": "/InputDocs/latexInputs/Program-Template.tex",
    "latexOutput": "/OutputDocs/latexDocs/",
    "latexTablesOutput": "/OutputDocs/latexDocs/Tables/",
    "htmlProgramTemplate": "/InputDocs/htmlInputs/Program-Template.html",
    "htmlOutput": "/OutputDocs/htmlDocs/"
}' > config.json
    

# TODO FIX THIS
#echo "{
#    \"inputDocsDir\": \"${INPUT_DIR}\",
#    \"knowledgeInputFile\" : \"${KNOWLEDGEBASE_FILE}\",
#    \"excelProgramsOutput\": \"${EXCEL_PROGRAMS_OUTPUT}\",
#    \"excelUnitsOutput\": \"${EXCEL_UNITS_OUTPUT}\",
#    \"latexProgramTemplate\": \"${LATEX_PROG_TEMPLATE}\",
#    \"latexOutput\": \"${LATEX_OUTPUT}/\",
#    \"latexTablesOutput\": \"${LATEX_TABLES_OUTPUT}\",
#    \"htmlProgramTemplate\": \"${HTML_PROG_TEMPLATE}\",
#    \"htmlOutput\": \"${HTML_OUTPUT}/\"
#}" > config.json

