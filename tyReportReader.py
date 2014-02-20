import csv
import datetime
import qbReporterFinal
class entry:
	def __init__(self, name, count):
		self.name = name
		self.count = count
		self.countbyTime = float(-1)

class TyCaller:
	def __init__(self, CflRow):
		self.data = CflRow
		self.tyName = self.data[0]
		self.qbTime = time(self.data[3]).returnDecimal()
		self.qbName = ''
		self.tyTime = -1
		default = 'NOT FOUND'
		self.qbName = userDict.get(self.tyName, default)
		self.workable = -1


#converts the csv reader output into a list of lists to be transposed because tayrex makes no sense
def getClientFileLists(clientFile):
	with open(clientFile, 'rbU') as cf:
		reader = csv.reader(cf)
		clientFileLists = []
		for row in reader:
			clientFileLists.append(row)
	return clientFileLists


#gets the client name and returns it from the cfl. has to be done before client name is popped off
def getClientName(CFL):
	return(CFL[0][0][8:])


# transposes x and y for a list of lists, super useful.
def Transpose(CFL):
	returnList = []
	for item in CFL[0]:
		returnList.append([])
	for row in CFL:
		count = 0
		for item in row:
			returnList[count].append(item)
			count+=1
	return returnList


# removes percent rows from transposed CFL
def removePercents(CFL):
	returnList = []
	for row in CFL:
		row.pop(0)
		if row[0] != '':
			returnList.append(row)
	return returnList


#prints out the CFL used in testing
def printCfl(CFL):
	for row in CFL:
		print row


#borderline useless class, shouldnt be a class
class category:
	def __init__(self, name):
		self.name = name
		self.locations = []
	def addLocation(self, loc):
		self.locations.append(loc)


#returns the category - opportunity etc. not super useful
def getCategory(item):
	return item.split('>')[0].strip()


#gets the groupings of categories, probably needs to be reworked
def getGroupings(header):
	toReturn = []
	count = 0
	categories = []
	for item in header:
		if '>' in item:
			categoryName = getCategory(item)
			if categoryName not in categories:
				categories.append(categoryName)
				toReturn.append(category(categoryName))
			for x in toReturn:
				if x.name == categoryName:
					x.addLocation(count)
		count += 1
	return toReturn


#super janky solution to adding time. pretty rough.
#doesnt even subtract or anything, really just adds. has a return decimal though, useful
class time:
	def __init__(self, strTime):
		split = strTime.split(":")
		self.hrs = int(split[0])
		self.min = int(split[1])
		self.sec = int(split[2])
	def returnString(self):
		return self.hrs + ':' + self.min + ':' + self.sec
	def returnDecimal(self):
		toReturn = float(self.hrs) + (float(self.min)/60) #nobody uses seconds. forget them....
		return toReturn
	def addTime(self,stringTime):
		toAdd = time(stringTime)
		self.sec += toAdd.sec
		self.min += toAdd.min
		self.hrs += toAdd.hrs
		if self.sec >= 60:
			self.sec = self.sec - 60
			self.min += 1
		if self.min >= 60:
			self.min = self.min - 60
			self.hrs += 1


#gets the dict of key(tyusername) data qb username	
def getUserDict():
	#with open('/Volumes/Shared/VSA/Reporting/UserList/userList.csv', 'rbU') as ul:
	with open('userList/userList.csv', 'rbU') as ul:
		reader = csv.reader(ul)
		userDict ={}
		for row in reader:
			userDict[row[0]] = row[3]
	return userDict


#badly named. but it returns the actual values for the user from the indices
def getNumbers(CflRow, spots):
	RL = []
	for x in spots:
		RL.append(int(CflRow[x]))
	return RL


#will reuse in a big way, inserts values.
def insertTotals(CFL):
	global headers
	global headerGroupings
	global tyCallers
	localHeaderGroupings = headerGroupings
	lasts = []
	for header in headerGroupings:
		lasts.append([header.name, header.locations[-1]])
	for item in lasts:
		item[0] = "Total " + item[0] + ":"
	for item in reversed(lasts):
		headers.insert(item[1]+1,item[0])
		lastGrouping = localHeaderGroupings.pop() # removed pop(-1)
		for caller in tyCallers:
			total = sum(getNumbers(caller.data,lastGrouping.locations))
			caller.data.insert((item[1]+1),total)
	headerGroupings = getGroupings(headers)
	return CFL


def getWorkable(data):
	totalOpportunities = -1
	totalNegatives = -1
	count = 0
	for header in headers:
		if header == 'Total Opportunity:':
			totalOpportunities = count
		elif header == "Total Negative:":
			totalNegatives = count
			break
		count += 1
	workable = data[totalOpportunities] + data[totalNegatives]
	return workable	


def getOpportunityIndices():
	trl =[]
	for entry in headers:
		if 'Opportunity' in entry:
			trl.append(headers.index(entry))
	return trl

def formatFloat(num):
	return "{:10.2f}".format(num)
def formatPercentage(num):
	return "{0:.2f}%".format(num * 100)

def insertConversions():
	global headers
	global tyCallers
	opportunityIndices = getOpportunityIndices()
	opportunityIndices.reverse()
	for oppIndex in opportunityIndices:
		oppIndex
		headers.insert(oppIndex + 1,'Conversion: ' + headers[oppIndex])
		for tyCaller in tyCallers:
			if tyCaller.workable == 0:
				conversion = 0
			else:
				conversion =  float(tyCaller.data[oppIndex])/float(tyCaller.workable)
				conversion = formatPercentage(conversion)
			tyCaller.data.insert(oppIndex + 1, conversion)


def getTimeIndices():
	trl = []
	for header in headers:
		if "Opportunity" in header and "Conversion" not in header or header == 'Workable': 
			trl.append(headers.index(header))
	return trl


def insertTimeCalculations():
	global headers
	global tyCallers
	
	timeIndices = getTimeIndices()
	timeIndices.reverse()
	for index in timeIndices:
		headers.insert(index + 1, "TIME :" +headers[index])
		for caller in tyCallers:
			if caller.qbTime > 0:
				oppByTime = float(caller.data[index])/float(caller.qbTime)
				oppByTime = formatFloat(oppByTime)
			else:
				oppByTime = "N/A"
			caller.data.insert(index + 1, oppByTime)

def getConfig():
	with open('tyReporterConfig.txt', 'rbU') as configFile:
		reader = csv.reader(configFile)
		configList = []
		for row in reader:
			configList.append(row)
	return configList


def main():

	#I really need to figure out the proper way to use global variables.
	global userDict 
	global headers
	global headerGroupings	
	global tyCallers
	global client

	userDict = getUserDict()
	tyFilesList = getConfig()
	for tyFile in tyFilesList:
		client = tyFile[0]
		sub(tyFile[1])

def sub(clientFile):
	global headers
	global headerGroupings	
	global tyCallers
	global client
	CFL = getClientFileLists("tyReports/" + clientFile)
	CFL = Transpose(CFL) 
	headers = CFL.pop(0)
	tyClient = headers.pop(0).split(':')[1].strip()
	headerGroupings = getGroupings(headers)
	CFL = removePercents(CFL)
	printCfl(CFL)	

	
	tyCallers = []
	for row in CFL:
		tyCallers.append(TyCaller(row))
	#INSERT TOTALS
	CFL = insertTotals(CFL)
	
	#fill out workable field for each caller for later calculations
	#Broken how to fix.....
	print headers
	for caller in tyCallers:
		caller.workable = getWorkable(caller.data)	


	for header in headerGroupings:
		print header.name
		print header.locations
		print

	

	#grab the guts from qbReader, the fully updated caller list with clients under. blech
	qbCallersList = qbReporterFinal.main()	
	for tyCaller in tyCallers:
		for qbCaller in qbCallersList:
			if tyCaller.qbName == qbCaller.name:
				for client in qbCaller.clients:
					if client.name == tyClient:
						tyCaller.qbTime = client.time
						break

	headers.append("qbName")
	headers.append("qbTime")
	headers.append("Workable")
	headers.append("qbTime-tyTime")	

	for caller in tyCallers:
		caller.data.append(caller.qbName)
		caller.data.append(caller.qbTime)
		caller.data.append(caller.workable)
		caller.data.append(caller.qbTime - caller.tyTime)

	insertConversions()
	insertTimeCalculations()
	print "CLIENT" + str(client.name)
	with open("outputs/" + str(tyClient) + "_tyReport.csv", 'wb') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
		

		spamwriter.writerow(headers)
		for caller in tyCallers:
			
			spamwriter.writerow(caller.data)
	print "DONE" + str(datetime.datetime)

if __name__ == "__main__":
	main()



