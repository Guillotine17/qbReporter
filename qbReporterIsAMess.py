import csv

class Client:
	def __init__(self,name):
		self.name = name
		self.time = float(0)
		self.nonBillableTime = float(0)
	def addTime(self, time, billable):
		if billable:
			self.time = self.time + float(time)
		else:
			self.nonBillableTime = self.nonBillableTime + float(time)

class Caller:
	def __init__(self,name):
		self.name = name
		self.clientDict = {}
	def getName(self):
		return self.name
	def addClient(self, clientName):
		self.clientDict[clientName] = Client(clientName)
	def addTime(self, clientName, time, billable):
		if billable:
			self.clientDict[clientName].addTime(time, billable)
		else:
			self.clientDict[clientName].addTime(time, billable)
			billable = True
			self.clientDict["VSA"].addTime(time,billable)

#checks to make sure that the row isnt just header nonsense etc, but one of the body rows. 
def evaluate(row):
	if isTotal(row):
		return False
	elif firstFilledRestEmpty(row):
		return False
	elif allBlank(row):
		return False
	elif isHeader(row):
		return False
	else:
		return True

def isTotal(row):
	if row[0] == '':
		return False
	if row[0].split()[0] == "Total":
		return True

def firstFilledRestEmpty(row):
	if row[0] != '':
		row.pop(0)
		for each in row:
			if each != '':
				return False
		return True
	else:
		return False

def allBlank(row):
	for x in row:
		if x != '':
			return False
	return True

def isHeader(row):
	if row[1] == 'Activity Date':
		return True
	return False

#reads the configuration text file to get column locations for data. 
def getConfig():
	fh = open("qbReporterConfig", "rbU")
	lines = fh.readlines()
	settings = []
	for line in lines:
		if line[0] == '#':
			continue
		else:
			split = line.split(':')
			settings.append(split[-1][:-1])
	fh.close()
	return settings


def billableEval(row):
	if row[billableColumn] == "Yes":
		return True
	else:
		return False


def getClient(row):
	return row[clientColumn]

def getCaller(row):
	return row[callerColumn]

def updateCallers(client):
	for caller in callerDict.itervalues():
		caller.addClient(client)

def getTime(row):
	return row[timeColumn]

def main():
	global clientColumn
	global callerColumn
	global timeColumn
	global clientList
	global callerDict
	global currentClient
	global billableColumn

	settings = getConfig()
	inputFile = settings[0]
	callerColumn = int(settings[1])
	clientColumn = int(settings[2])
	timeColumn = int(settings[3])
	billableColumn = int(settings[4])

	clientList = []
	callerDict = {}

	with open(inputFile, 'rbU') as f:
		reader = csv.reader(f)

		for row in reader:
			billable = True
			if not evaluate(row):
				continue
			if not billableEval(row):
				billable = False
			client = getClient(row)
			if client not in clientList:
				clientList.append(client)
				updateCallers(client)
			caller = getCaller(row)
			if caller not in callerDict.keys():
				callerDict[caller] = Caller(caller)
				for client in clientList:
					callerDict[caller].addClient(client)
			callerDict[caller].clientDict[client].addTime(getTime(row),billable)

	with open('qbReporterOutput.csv', 'wb') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
		spamwriter.writerow(["caller"] + clientList)
		sortedNames = callerDict.keys()
		sortedNames.sort()
		for name in sortedNames:
			toWrite = []
			toWrite.append(name)
			for client in clientList:
				toWrite.append(str(callerDict[name].clientDict[client].time))
			spamwriter.writerow(toWrite)
		toWrite = []
		toWrite.append("Totals")
		for client in clientList:
			timesum = float(0)
			for caller in callerDict.itervalues():
				timesum += caller.clientDict[client].time
			toWrite.append(str(timesum))
		spamwriter.writerow(toWrite)

	with open('NONBILLABLEqbReporterOutput.csv', 'wb') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
		spamwriter.writerow(["caller"] + clientList)
		sortedNames = callerDict.keys()
		sortedNames.sort()
		for name in sortedNames:
			toWrite = []
			toWrite.append(name)
			for client in clientList:
				toWrite.append(str(callerDict[name].clientDict[client].nonBillableTime))
			spamwriter.writerow(toWrite)
		toWrite = []
		toWrite.append("Totals")
		for client in clientList:
			timesum = float(0)
			for caller in callerDict.itervalues():
				timesum += caller.clientDict[client].nonBillableTime
			toWrite.append(str(timesum))
		spamwriter.writerow(toWrite)
	return callerDict

if __name__ == "__main__":
	main()






