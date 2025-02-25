# Python script to read a multisheet excel knolwedge base file and 
# create a dictionary of dictionary data structure of accreditation information tables
# @ Author Rachel Cardell-Oliver 
# @ Author Original script by MIT team 12 accreditation mapper project
# @Version 29 Oct 2024

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
dfCourses = pd.read_excel(knowledgefile , header=0, sheet_name='CriterionA')

dfJustification = pd.read_excel(knowledgefile , header=0, sheet_name='Program Justification')

dfUnits = pd.read_excel(knowledgefile , header=0, sheet_name='Outcomes Mappings')
dfProgs = pd.read_excel(knowledgefile , header=0, sheet_name='Programs Details')
dfProgOutcomes = pd.read_excel(knowledgefile , header=0, sheet_name='Program Outcome Mappings')
dfProgOutcomeDescriptions = pd.read_excel(knowledgefile , header=0, sheet_name='Program Outcome Descriptions')
unitoutcomesFile = os.path.join(config["caidiInputDocsDir"], config["unitoutcomesFile"]) 
dfUnitOutcomes = pd.read_excel(unitoutcomesFile,  header=2)

staffCVsFile = os.path.join(config["inputDocsDir"], config["staffCVsFile"]) 
staffCVs = pd.read_excel(staffCVsFile,header=1) #ignore long column names row

# get course list to be used for dictionaries
courseSet = set(dfCourses['Course'].dropna())
print(courseSet)

#create a dictionary of dictionaries of ACS tables
acsDict = {}

#=== criterion A
dicA = {}
for course in courseSet:
	cA =  dfCourses.loc[dfCourses['Course']==course,("Program Details","Description or URL")]
	dicA[course] = cA
acsDict["A"] = dicA

#==== criterion A Program justification text
dicJ = {}
for course in courseSet:
	cJ =  dfJustification.loc[dfCourses['Course']==course,("Description or URL")]
	dicJ[course] = cJ
acsDict["J"] = dicJ



#=== criterion B
# use Criterion B make a dictionary: course ID to dataframe table of information needed
cB1 = dfUnits.loc[ dfUnits['Outcome Group']=='ICT Professional Role', ( 'Outcome', 'Course') ]
cB2 = dfUnits.loc[ dfUnits['Outcome Group']=="ICT Skills SFIA",( 'Outcome','Justification','Level (SFIA/Bloom/UnitOutcome)','Unit Code', 'Unit Name', 'Course') ]
cB2.rename(columns = {'Outcome':'SFIA Skill Code'}, inplace = True) #match ACS naming
cB2.rename(columns = {'Level (SFIA/Bloom/UnitOutcome)':'SFIA level'}, inplace = True)
cB2.rename(columns = {'Justification':'SFIA-9 URL'}, inplace = True)

dicB = {}
for course in courseSet:
	sfiaDic = {}
	sfiaDic["Role"] = cB1.loc[cB1['Course'].str.contains(course),'Outcome'].values[0] #get string
	sfiaDic["Units"] =  cB2.loc[cB2['Course'].str.contains(course), ('SFIA Skill Code', 'SFIA-9 URL','SFIA level', 'Unit Code', 'Unit Name') ]
	dicB[course] = sfiaDic
acsDict["B"] = dicB


#=== criterion C
dicC = {}
for course in courseSet:
	cbokDic = {}
	#core (mandatory) units for this program
	core = dfProgs.loc[(dfProgs[course] == 'Core Unit'), 'Unit Code']	
	cg = [ 'CBoK-Professional', 'CBoK-Core', 'CBoK-Depth' ]
	cBoK = dfUnits.loc[ dfUnits['Outcome Group'].isin(cg)]
	ccBoK = cBoK.loc[cBoK['Unit Code'].isin(core), ('Outcome Group', 'Outcome', 'Unit Code', 'Unit Name', 'Level (SFIA/Bloom/UnitOutcome)','Justification')]

	# row names are all core units for a given major/program, 
	rownames = core
	# column names are all CBoK outcomes - actually these should be ordered
	colnames = [ 'ICT Ethics', 'Impacts of ICT', 'Working Individually and Teamwork', 'Professional Communication', 'Professional Practitioner', 'ICT Fundamentals', 'ICT Infrastructure', 'Information and Data Science and Engineering', 'Computational Science and Engineering', 'Application Systems', 'Cyber Security', 'ICT Projects', 'ICT Management and Governance', 'In-depth ICT Knowledge' ]

	# create a mapping table from units to outcomes (blank rather than nan if none)
	cbokmap = pd.DataFrame(index=range(len(rownames)),columns=range(len(colnames))).fillna("")
	cbokmap.columns = colnames
	cbokmap.index = rownames
	# find each unit,outcome pair and record Bloom(group) level in the appropriate cell in cbokmap
	for u1 in rownames:
		oo = ccBoK.loc[ccBoK['Unit Code']==u1,('Outcome','Level (SFIA/Bloom/UnitOutcome)')]
		for ind in oo.index: #every row
			o1 = oo['Outcome'][ind]
			b1 = oo['Level (SFIA/Bloom/UnitOutcome)'][ind]
			cbokmap.loc[u1,o1] = b1
	cbokDic["Map Table"] = cbokmap
	#Next create table of justification reasons
	reasons = ccBoK.loc[:,('Outcome', 'Unit Code', 'Justification')]
	#TODO maybe index ordering
	#df = df.set_index("C1") df = df.sort_values(["C1", "C2"])
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
	dicD[course] = advdf
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

#=== unit outcomes to program outcomes mapping 
#=== TODO create caidi versions as ground truth and not require these
outcomesDic = {}
for course in courseSet:
	outDic = {}
	#get core (mandatory) units for this course
	coreunits = np.sort(dfProgs.loc[(dfProgs[course] == 'Core Unit'), ('Unit Code')])
	courseoutcomes = dfProgOutcomes.loc[dfProgOutcomes['Courses'].str.contains(course), ('Unit Code','Program Outcome Code','Map','Courses')].fillna("")
	uout = dfUnitOutcomes.loc[:,('Code','Title','Assessment items','Outcomes')]
	
	progoutnames = courseoutcomes['Program Outcome Code'].unique()
	outcomekey = dfProgOutcomeDescriptions.loc[dfProgOutcomeDescriptions['Program Outcome Code'].isin(progoutnames)]
	po = outcomekey['Program Outcome Description']
	

	
	# create a mapping table from units to outcomes (blank rather than nan if none)
	outmap = pd.DataFrame(index=range(len(coreunits)),columns=range(len(progoutnames))).fillna("")
	outmap.columns = progoutnames
	outmap.index = coreunits
	outmap.loc[len(outmap)] = list(po) #add prog outcomes as last row
	#TODO change index name of last row. NOT this way outmap.index[-1] = 'Program Outcomes'
	outmap['Unit Outcomes'] = ' '  #add a column to list the unit outcomes
	# now fill the table with outcome mappings
	for ind in outmap.index[:-1]: #every unit code row
		u1 = ind
		# assign to outcome string (removing prefix text)
		oo = uout.loc[uout['Code']==u1,'Outcomes']
		if len(oo)==1: #unit exists, ignores XX choice units
			outstr = oo.values[0] #get string
			#print([course, u1])
			str = outstr.partition('Students are able to ')[2]
			outmap.loc[ind,'Unit Outcomes'] = str
			for pp in progoutnames: #course outcomes # assign list of unit outcomes satisfying course outcome (if any)
				m1 = courseoutcomes['Map'][(courseoutcomes['Unit Code']==u1) & (courseoutcomes['Program Outcome Code']==pp) ]
				if len(m1)==1:
					#print(m1.values[0])
					outmap.loc[ind,pp] = m1.values[0]
	outcomesDic[course] = outmap
acsDict["OutMap"] = outcomesDic


#=== staff CV table for latex part 1
acsDict["StaffCVs"] = staffCVs



