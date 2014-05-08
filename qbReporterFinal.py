import csv



class Client:
	def __init__(self, name):
		self.name = name
		self.time = float(0)
	def addTime(self, time):
		if time != "":
			self.time = self.time + float(time)

	def getName(self):
		return self.name
	def getTime(self):
		return self.time

class Caller:
	def __init__(self, name):
		self.name = name
		self.clients = []
	def getName(self):
		return self.name
	def addClient(self, clientName):
		self.clients.append(Client(clientName))
	def addTime(self, clientName, time):
		for client in self.clients:
			if client.getName() == clientName:
				client.addTime(time)
	def getClients(self):
		return self.clients

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

#inputFile:
#CallerColumn:
#clientColumn:
#timeColumn:



def isTotal(row):
	if row[0] == '':
		return False
	if row[0].split()[0] == "Total":
		return True

def getCaller(row):
	return row[callerColumn]

def getClient(row):
	return row[clientColumn]

def getTime(row):
	return row[timeColumn]

def updateClients(clientName):
	global clients
	if clientName not in clients:
		clients.append(clientName)

def updateCallers(clientToAdd):
	global callers
	for caller in callers:
		found = 0
		for client in caller.clients:
			if client.getName() == clientToAdd:
				found = 1
				break
		if found == 0:
			caller.addClient(clientToAdd)

def update():
	global clients
	global callers
	global currentClient
	updateClients(currentClient)
	for client in clients:
		updateCallers(client)



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

	
def main():
	global clientColumn
	global callerColumn
	global timeColumn
	global clients
	global callers
	global currentClient	

	settings = getConfig()
	#load config
	inputFile = settings[0]
	callerColumn = int(settings[1])
	clientColumn = int(settings[2])
	timeColumn = int(settings[3])
	#print settings[3]	
	

	clients = []
	callers = []
	currentClient = ''	

	with open(inputFile, 'rbU') as f:
		reader = csv.reader(f)	

		for row in reader:
			if not evaluate(row):
				continue
			currentClient = getClient(row)
			#print row
			if currentClient not in clients:
				update()
			caller = getCaller(row)
			found = 0
			for employee in callers:
				callerName = employee.getName()
				if callerName == caller:
					found = 1
					employee.addTime(currentClient,getTime(row))
					break
			if found == 0:
				callers.append(Caller(caller))
				update()
				callers[-1].addTime(currentClient, getTime(row))	
	

	########OUTPUT############	
	

	with open('csvWriterOutput.csv', 'wb') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
		spamwriter.writerow(["caller"] + clients)
		for employee in callers:
			times = []
			for client in employee.clients:
				times.append(str(client.time))	

			spamwriter.writerow([employee.name] + times)	

	#print times
	return callers

if __name__ == "__main__":
	main()

