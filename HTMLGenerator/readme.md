
├── caidi.py                # CAIDI data processing script
├── dataframe_A.py          # Dataframe generation for Criterion A
├── dataframe_D.py          # Dataframe generation for Criterion D
├── knowledgebase.py        # Knowledgebase script
├── SFIAReader.py           # SFIA reading and processing script
├── sfia.py                 # SFIA data extraction and processing script
├── caidi-data-for-ACS-A.zip# CAIDI zip file that contains data required for processing
├── CSSE-allprograms-outcome-mappings-20241011.xlsx # Knowledgebase Excel file containing mappings of outcomes and accreditation data, used for generating reports.

Ensure they all in current directory and then run this ./run.sh in terminal.

The run.sh script will automate the following tasks:

	•	Activates the Python virtual environment.
	•	Installs all required Python dependencies (listed in requirements.txt).
	•	Executes preprocessing scripts, including sfia.py, caidi.py, and other necessary scripts.
	•	Finally, it launches the Flask web application (app.py).

 To access it, open your web browser and go to:
 http://127.0.0.1:5000
