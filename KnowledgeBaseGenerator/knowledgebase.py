# Python script to read a multisheet excel knolwedge base file and 
# create a dictionary of dictionary data structure of accreditation information tables
# @ Author Rachel Cardell-Oliver 
# @ Author Original script by MIT team 12 accreditation mapper project October 2024
# @Version 2 May 2025

import os
import json
import pandas as pd
import numpy as np

# open config.json and get name of knowledge file
config_path = os.path.join(os.getcwd(), 'config.json')
#print("Config file:" + config_path)
try:
	with open(config_path, 'r') as f:
		config = json.load(f)
		print("Configuration loaded successfully:") #, config)
except FileNotFoundError:
	print(f"Error: config.json file not found at {config_path}")
except json.JSONDecodeError:
	print("Error: Failed to decode the config.json file")


# Open input excel files and read relevant parts into pandas data frames
knowledgefile = os.path.join(config["inputDocsDir"], config["knowledgeInputFile"]) 
dfCourses = pd.read_excel(knowledgefile , header=0, sheet_name='Program Summary Table')

dfJustification = pd.read_excel(knowledgefile , header=0, sheet_name='Program Justifications')

dfRoles = pd.read_excel(knowledgefile , header=0, sheet_name='Professional Role SFIA')

dfUnits = pd.read_excel(knowledgefile , header=0, sheet_name='Outcomes Mappings')
dfProgs = pd.read_excel(knowledgefile , header=0, sheet_name='Programs Details')


#staff CVs
staffCVsFile = os.path.join(config["inputDocsDir"], config["staffCVsFile"]) 
staffCVs = pd.read_excel(staffCVsFile,header=1) #ignore long column names row

#IAP members
IAPFile = os.path.join(config["inputDocsDir"], config["IAPFile"]) 
IAPlist = pd.read_excel(IAPFile) 

# get course list to be used for dictionaries
courseSet = set(dfCourses['Course'].dropna())
#print(courseSet)

#create a dictionary of dictionaries of ACS tables
acsDict = {}

print(courseSet)

#=== criterion A
dicA = {}
for course in courseSet:
	cA =  dfCourses.loc[dfCourses['Course']==course,('Program Details','Table Row','Description or URL')].sort_values(by='Table Row')
	dicA[course] = cA.loc[:,('Program Details','Description or URL')]
acsDict["A"] = dicA

#==== per-Program texts: required for justification in A and footnotes tables B, C, D
dicJ = {}
for course in courseSet:
	cJ =  dfJustification.loc[dfJustification['Courses'].str.contains(course), ( 'Criteria', 'Paragraph', 'Description Text' ) ] 
	dicJ[course] = cJ
acsDict["J"] = dicJ



#=== criterion B
# use Criterion B make a dictionary: course ID to dataframe table of information needed
cB1 = dfUnits.loc[ dfUnits['Outcome Group']=='ICT Professional Role', ( 'Outcome', 'Course') ]
#comments is the sfia link, Justification is the explanatory text
cB2 = dfUnits.loc[ dfUnits['Outcome Group']=="ICT Skills SFIA",( 'Outcome','Comments','Level (SFIA/Bloom/UnitOutcome)','Justification','Unit Code', 'Unit Name', 'Course') ]
cB2.rename(columns = {'Outcome':'SFIA Skill Code'}, inplace = True) #match ACS naming
cB2.rename(columns = {'Comments':'SFIA-9 URL'}, inplace = True)
cB2.rename(columns = {'Level (SFIA/Bloom/UnitOutcome)':'SFIA level'}, inplace = True)


dicB = {}
for course in courseSet:
	sfiaDic = {}

	sfiaDic["Role"] = dfRoles.loc[dfRoles['Course'].str.contains(course),'Role'].values[0] #get string
	
	CB3 = cB2.loc[cB2['Course'].str.contains(course), ('SFIA Skill Code', 'SFIA-9 URL','SFIA level', 'Justification','Unit Code', 'Unit Name') ]
	CB4 = CB3.sort_values(by=['SFIA Skill Code','SFIA level'])
	sfiaDic["Units"] =  CB4
	#TODO order table by SFIA Code then Level
	dicB[course] = sfiaDic
	
acsDict["B"] = dicB


##TODO B include note for any programs with SFIA outcomes from electives eg MDSc - but better to use core units if possible


#=== criterion C
dicC = {}
for course in courseSet:
	cbokDic = {}
	
	#core (mandatory) units and options necessary for CBoK for this program
	
	cBoK = dfUnits.loc[ (dfUnits['ACS Accreditation Criterion'] == 'C') & (dfUnits['Course'].str.contains(course)) , ( 'Outcome Group', 'Outcome', 'Unit Code', 'Unit Name', 'Level (SFIA/Bloom/UnitOutcome)','Justification' ) ]
	#print(cBoK)
	
	coreplus = np.sort(cBoK['Unit Code'].unique().tolist())
	#print(coreplus)

	
	## TODO include the unit code and name in labels frin
	
	#cg = [ 'CBoK-Professional', 'CBoK-Core', 'CBoK-Depth' ]
	#cBoK = dfUnits.loc[ dfUnits['Outcome Group'].isin(cg)]
	#was isin(core)
	ccBoK = cBoK.loc[:, ('Outcome Group', 'Outcome', 'Unit Code', 'Unit Name', 'Level (SFIA/Bloom/UnitOutcome)','Justification')]
	
	
	# row names are all required CBoK units for a given major/program, 
	rownames = coreplus
	# column names are all CBoK outcomes - actually these should be ordered
	colnames = ['ICT Ethics', 'Impacts of ICT', 'Working Individually and Teamwork', 'Professional Communication', 'Professional Practitioner', 'ICT Fundamentals', 'ICT Infrastructure', 'Information and Data Science and Engineering', 'Computational Science and Engineering', 'Application Systems', 'Cyber Security', 'ICT Projects', 'ICT Management and Governance', 'In-depth ICT Knowledge' ]

	# create a mapping table from units to outcomes (blank rather than nan if none)
	cbokmap = pd.DataFrame(index=range(len(rownames)),columns=range(len(colnames))).fillna("")
	cbokmap.columns = colnames
	cbokmap.index = rownames
		
	# find each unit,outcome pair and record Bloom(group) level in the appropriate cell in cbokmap
	for u1 in coreplus:
		oo = ccBoK.loc[ccBoK['Unit Code']==u1,('Outcome','Level (SFIA/Bloom/UnitOutcome)')]
		for ind in oo.index: #every row
			o1 = oo['Outcome'][ind]
			b1 = oo['Level (SFIA/Bloom/UnitOutcome)'][ind]
			cbokmap.loc[u1,o1] = b1
	cbokDic["Map Table"] = cbokmap

	#Next create table of justification reasons
	reasons = ccBoK.loc[:,('Outcome Group','Outcome', 'Unit Code','Unit Name','Justification')].sort_values(by=['Outcome Group', 'Outcome', 'Unit Code'])
	cbokDic["Justification Table"] = reasons
	dicC[course] = cbokDic

acsDict["C"] = dicC	

	
#=== criterion D
dicD = {}
cD = dfUnits.loc[ dfUnits['Outcome Group']=='Advanced', ( 'Unit Code', 'Unit Name','Assessment Item','Justification', 'Course') ]

#find advanced units where course is in the course list
for course in courseSet:
	rows = cD['Course'].str.contains(course)
	advdf = cD.loc[rows,( 'Unit Code', 'Unit Name','Assessment Item','Justification')]
	advdf.rename(columns = {'Justification':'Complex Computing Criteria Met'}, inplace = True) #match ACS naming
	dicD[course] = advdf.sort_values(by='Unit Code')
acsDict["D"] = dicD

#=== criterion E
dicE = {}
cE = dfUnits.loc[ dfUnits['Outcome Group']=='Integrated Skills', ( 'Unit Code', 'Unit Name','Justification', 'Course') ]
for course in courseSet:
	rows = cE['Course'].str.contains(course)
	edf = cE.loc[rows,( 'Unit Code', 'Unit Name','Justification')]
	edf.rename(columns = {'Justification':'Notes in support of Claim'}, inplace = True) #match ACS naming
	dicE[course] = edf
acsDict["E"] = dicE
	
#=== criterion F 
dicF = {}
cF = dfUnits.loc[ dfUnits['Outcome Group']=='Professional Practice', ( 'Justification', 'Course') ]
for course in courseSet:
	profDic = {}
	rows = cF['Course'].str.contains(course)
	profDic["Practice"] = cF.loc[rows,( 'Justification')].values[0] #get string. 
	dicF[course] = profDic
acsDict["F"] = dicF



#=== staff CV and IAP table for latex part 1
acsDict["StaffCVs"] = staffCVs
#===  IAP links table for latex part 1
acsDict["IAPlist"] = IAPlist


