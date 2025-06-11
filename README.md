# CS-accreditation
This app generates accreditation documentation in various formats from a database
Samples of required input files are in the InputDocs directory:
  Sample-ACS-Knowledgebase.xlsx which contains program information and mappings of units to ACS outcomes
Ouputs are generated in Latex, HTML, Excel, and Word formats using input templates from the subdirectories of InputDocs
The bash script MakeAccrediationOutputs.sh runs everything.
There is a Github Action for this too.

Acknolwedgements: This software for managing program information for accreditation, and generating output documents in multiple formats,
was developed in 2024 by a student team in the University of Western Australia's Masters of Information Technology Capstone Project:
Kent Yip, Shuyu Ding, Phoebus Lee, Subbulakshimi Seenivasan, Aji Wuryanto, and Linfeng Zheng. 
The software was refactored and extended by Rachel Cardell-Oliver. 
This project holds the current version of that codebase.
