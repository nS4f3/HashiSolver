from iislands import Island
import random

class Main:
	def __init__(self,file):
		self.file =file
		self.b = []
		self.l = []
		self.deleted = []
		self.elem = {}
		self.ab = []


	def check(self,board):
  		res = []
  		for i in board:
  			for j in i:
  				if j not in ["  ","| ","- ","= ","||"]:
  					if(j.value - len(j.connections) == 0):
  						res.append(0)
  					else:
  						res.append(1)

  		return res


	def printB(self):
		for i in self.b:
			for j in i:
				if(j not in ["  ", "= ","- ","| ","||"]):
					print(j.value,end = " ")
				else:
					print(j,end = "")
			print()

	def generateboard(self):
		f = open(self.file)
		board = []
		lines = [i.strip().split(" ") for i in f.readlines()]
		for line in range(len(lines)):
			l = []
			for i in range(len(lines)):

				if lines[line][i] == "0":
					l.append("  ")
				else:
					
					c = Island(int(lines[line][i]),i,line)
					l.append(c)

			board.append(l)
		return board


	def calcAllActuals(self):
		for i in self.b:
			for j in i:
				if(j not in ["  ", "= ","- ","| ","||"]):
					j.findDirections(self.b)
					j.CalcTemp()
					j.calcActualSol(self.b)
					if(len(j.actualsols) > 1):
						if(len(j.actualsols[0]) != 0):
							self.elem[j] = j.actualsols



	def define(self):
		self.l = []
		for i in self.b:
			for j in i:
				if(j not in ["  ", "= ","- ","| ","||"]):
					j.findDirections(self.b)
					j.CalcTemp()
					self.l.append(j)

	def  checkelem(self):
		for i in self.elem:
			if(len(i.actualsols) == 0 ):
				del self.elem[i]

	def procces(self,level):
		


		
		c = 0
		flag = True
		while c < 5:
  			c+=1
  			flag = True
  			print(level)



  			if(sum(self.check(self.b)) == 0):
  				break
  			else:
  				for i in self.l:
  					i.findDirections(self.b)
  					i.CalcTemp()
  					i.calcActualSol(self.b)
  					if(len(i.actualsols) == 1):
  						if(len(i.actualsols[0]) != 0):
  							self.b = i.connect(i.actualsols[0],self.b)
  							flag = False

  							if(sum(self.check(self.b)) == 0):
  								break

  						else:
  							pass
  					else:
  						pass


  			if(flag):
  				self.calcAllActuals()
  				if(len(self.elem) == 0):
  					break
  				
  				liste = list(self.elem.keys())
  				eleman = random.choice(liste)
  				move = random.choice(self.elem[eleman])
  				if(move not in self.deleted):
  					try:
  						self.b = eleman.connect(move,self.b)
  						self.procces(level+1)
  						if(sum(self.check(self.b)) != 0):
  							if(level == 0):
  								pass
  								#self.deleted.append(move)
  								#self.elem[eleman].remove(move)
  							self.b = self.generateboard()
  							
  						else:
  							break
  					except Exception as e:
  						#self.deleted.append(move)
  						#self.elem[eleman].remove(move)
  						self.b = self.generateboard()
  						
  				else:
  					self.b = self.generateboard()
  					





if __name__ == "__main__":
	m = Main("c4.txt")
	m.b = m.generateboard()
	m.define()
	m.procces(0)
	print("\n")
	m.printB()
	input()




