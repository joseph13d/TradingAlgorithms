#
#
#
#
import csv

def stripCSV(name,year):
	with open(name) as appleData:
		lines = csv.DictReader(appleData)
		closePrices = []
		lastclose= 1
		closeV = 1
		for row in lines:

			lastclose = closeV
			closeV = float(row['close'])

			if row['date'][:4] == year:
				#print (row)
				
				#print(type(closeV))
				pctdiff = (closeV - lastclose) / lastclose
				closePrices.append(pctdiff)

		return closePrices




class Perceptron:
	def __init__(self):
		#9 
		self.weights = [0,0,0,0,0,0,0,0,0] 
		self.selfIndex = 0
		#self.history = FullData
	def activation(self, featureVector):
		return self.dotProduct(featureVector,self.weights)
	def dotProduct(self, a, b):
		total = 0
		for i in range(len(a)):
			total += a[i] * b[i]
		return total
	def update(self, featureVector, y, ystar):
		if y * ystar > 0:
			return
		else:
			for i in range(len(self.weights)):
				self.weights[i] = self.weights[i] + (ystar * featureVector[i])
	def trainOnce(self, featureVector, ystar):
		y = self.activation(featureVector)
		self.update(featureVector, y, ystar)




class StockData:
	def __init__(self, year):
		self.files = [
			'AAPL_data.csv',
			'AMD_data.csv',
			'HPQ_data.csv',
			'IBM_data.csv',
			'INTC_data.csv',
			'MSFT_data.csv',
			'MU_data.csv',
			'NVDA_data.csv']
		self.featureList = []
		self.buildFeatures(year)
	def buildFeatures(self,year):
		bigDict = {}
		for x in self.files:
			print('parsing ', x)
			bigDict[x] = stripCSV(x,year)
		#print (bigDict)
		for i in range(len(bigDict['AAPL_data.csv'])):
			nextfeature = [
				1,
				bigDict['AAPL_data.csv'][i],
				bigDict['AMD_data.csv'][i],
				bigDict['HPQ_data.csv'][i],
				bigDict['IBM_data.csv'][i],
				bigDict['INTC_data.csv'][i],
				bigDict['MSFT_data.csv'][i],
				bigDict['MU_data.csv'][i],
				bigDict['NVDA_data.csv'][i]]
			self.featureList.append(nextfeature)
		#print(self.featureList)



#FullData = StockData('2016')
class PerceptronAlgoTrader:
	def __init__(self):
		self.apple = Perceptron()
		self.apple.selfIndex = 1

		self.amd = Perceptron()
		self.amd.selfIndex = 2
		
		self.hp = Perceptron()
		self.hp.selfIndex = 3
		
		self.ibm = Perceptron()
		self.ibm.selfIndex = 4

		self.intel = Perceptron()
		self.intel.selfIndex = 5

		self.msft = Perceptron()
		self.msft.selfIndex = 6

		self.micron = Perceptron()
		self.micron.selfIndex = 7

		self.nvidia = Perceptron()
		self.nvidia.selfIndex = 8

		self.history = StockData('2016')
		self.alltrons = [self.apple, self.amd, self.hp, self.ibm, self.intel, self.msft, self.micron, self.nvidia]
		self.account = 25000.0
		self.baseAllowance = 2000.0
	def trainOne(self, tron):
		for i in range(len(self.history.featureList)-1): #stop one from the end
			tron.trainOnce(self.history.featureList[i], 
				self.history.featureList[i+1][tron.selfIndex])
	def trainAll(self):
		for tron in self.alltrons:
			self.trainOne(tron)
	def dotProduct(self, a, b):
		total = 0
		for i in range(len(a)):
			total += a[i] * b[i]
		return total
	#return a vector containing all the expected activations for each stock
	def getPredictionVector(self,featureVector):
		pred = [1.0]
		for tron in self.alltrons:
			pred.append(tron.activation(featureVector))
		return pred
	#perform one period's worth of trading, in this case one day
	def dailyTrade(self,dayFeatures,nextDayFeatures):
		pred = self.getPredictionVector(dayFeatures)
		available = [1,2,3,4,5,6,7,8]
		purchases = [0,0,0,0,0,0,0,0,0]
		allowed = self.baseAllowance
		wallet = self.account
		#still havent ran out of money or stocks to consider
		while len(available) > 0 and wallet > 1:
			index = self.getMaxOfIndeces(pred,available)
			available.remove(index)
			allowed = min(allowed,wallet)
			#expected index to rise, purchase at index and 
			if pred[index] > 0:
				purchases[index] = allowed
				wallet -= allowed
				allowed *= 0.8
			else:
				available = []
		delta = self.dotProduct(purchases,nextDayFeatures)
		self.account += delta
	#trade for the whole year
	def tradeTheYear(self,year):
		yearHistory = StockData(year)
		features = yearHistory.featureList
		for i in range(len(features)-1):
			self.dailyTrade(features[i], features[i+1])
			print(self.account)
	def tradeTheYearWithLearning(self,year):
		yearHistory = StockData(year)
		features = yearHistory.featureList
		prevAcct = self.account
		fail = 0
		success = 0
		print('c(')
		for i in range(len(features)-1):
			self.dailyTrade(features[i], features[i+1])
			for tron in self.alltrons:
				tron.trainOnce(features[i],features[i+1][tron.selfIndex])

			print(self.account, ',')
			if self.account < prevAcct:
				fail += 1
			else:
				success += 1
			prevAcct = self.account
		print(fail,", ", success)
	#given a list and a list of valid indeces from that list, return a valid index with the highest value from the list
	def getMaxOfIndeces(self, mylist, indeces):
		maxval = mylist[indeces[0]]
		maxdex = indeces[0]
		for i in indeces:
			#print(i)
			#print(mylist)
			if mylist[i] > maxval:
				maxval = mylist[i]
				maxdex = i
		return maxdex


Trader = PerceptronAlgoTrader()
Trader.trainAll()
#Trader.tradeTheYear('2017')
Trader.tradeTheYearWithLearning('2017')
#minimum = 1
#for tron in Trader.alltrons:
#	print(tron.weights)

#print FullData
#for i in range(len()-1) #stop trading at end of year




'''
apple = 'AAPL_data.csv'
amd = ''
hp = ''
ibm = ''
intel = ''
micron = ''

y16 = '2016'
y17 = '2017'
q = stripCSV(apple, y16)
print(q)
'''