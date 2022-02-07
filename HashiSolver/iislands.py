"""Code sample that solves a model and displays all solutions."""

from ortools.sat.python import cp_model
from va import VarArraySolutionPrinter

class Island():
  def __init__(self,value,x,y):
    self.remainingcon = value
    self.connections = []
    self.x = x
    self.y = y
    self.directions = []
    self.value = value
    self.allsols = []
    self.tempsols = []
    self.actualsols = []
    self.__dir__ = {"R" : [1,0],
                    "L" : [-1,0],
                    "U" : [0,-1],
                    "D" : [0,1]}

    self.possCon = []

    

  def SearchForAll(self):
    self.remainingcon = self.value - len(self.connections)
    model = cp_model.CpModel()

  # Creates the variables.
    R = model.NewIntVar(0,2, 'R')
    D = model.NewIntVar(0,2, 'U')
    U = model.NewIntVar(0,2, 'D')
    L = model.NewIntVar(0,2,'L')

  # Create the constraints.
    model.Add(R + L + D + U == self.remainingcon)

  # Create a solver and solve.
    solver = cp_model.CpSolver()
    solution_printer = VarArraySolutionPrinter([R,D,U,L])
  # Enumerate all solutions.
    solver.parameters.enumerate_all_solutions = True
  # Solve.
    status = solver.Solve(model, solution_printer)

  #print('Status = %s' % solver.StatusName(status))
  #print('Number of solutions found: %i' % solution_printer.solution_count())
   
    return solution_printer.solutionslist

  def CalcTemp(self):
    notintdirect = [i for i in ["R","L","D","U"] if i not in self.directions]
    l = []
    for i in self.allsols:
      for y in notintdirect:
        pos1 = y + "1"
        pos2 = y + "2"

        if(pos1  in  i or pos2 in i):
          break
      else:
        l.append([x for x in i if "0" not in x])
    self.tempsols = l

  def findDirections(self,board):

    self.allsols = self.SearchForAll()
    dd = []
    p = []
    for d in self.__dir__:
      c = 0

      while True:
        c+= 1
        x = self.__dir__[d][0]*c
        y = self.__dir__[d][1]*c
 
        if(self.x + x >= len(board[0]) or self.x + x < 0 or self.y + y >= len(board) or self.y + y<0):
          break
        else:
          if(board[self.y + y][self.x + x] in ["||","= ","| ","- "]):
            break

          elif(board[self.y + y][self.x + x] == "  "):
            pass
          else:
            dd.append(d)
            p.append((self.x + x,self.y + y))
            break
    self.directions = dd
    self.possCon = p



  def connect(self, move,board):
    b = board
    for i in move:
      dire = i[0]
      c = int(i[1])
      
      obj = board[self.__findObje__(dire)[1]][self.__findObje__(dire)[0]]
      if(c == 2 and dire in ["R","L"]):
        a = 1 if dire == "R" else -1
        for x in range(self.x + a,obj.x,a):
          b[self.y][x] = "= " 
        self.connections.append(obj)
        obj.connections.append(self)
        self.connections.append(obj)
        obj.connections.append(self)
      
      elif(c == 2 and dire in ["D","U"]):
        a = 1 if dire == "D" else -1
        for x in range(self.y + a,obj.y,a):
          b[x][self.x] = "||"
        self.connections.append(obj)
        obj.connections.append(self)
        self.connections.append(obj)
        obj.connections.append(self)

      elif(c==1 and dire in ["R","L"]):
        a = 1 if dire == "R" else -1
        for x in range(self.x+a,obj.x,a):
          b[self.y][x] = "- "
        self.connections.append(obj)
        obj.connections.append(self)

      elif(c==1 and dire in ["D","U"]):
        a = 1 if dire == "D" else -1
        for x in range(self.y+a,obj.y,a):
          b[x][self.x] = "| "
        self.connections.append(obj)
        obj.connections.append(self)

    return b


    

  def calcActualSol(self,board):
    l = []
    for i in self.tempsols:
      if(sum(self.__isValid__(i,board)) == len(self.__isValid__(i,board))):
        l.append(i)
    self.actualsols = l


  def __findObje__(self,dire):
    t = ()
    for i in self.possCon:
      if(dire == "R"):
        if(i[0] > self.x):
          t = i
          break
      elif(dire == "L"):
        if(i[0] < self.x):
          t = i
          break
      elif(dire == "D"):
        if(i[1] > self.y):
          t = i
          break
      elif(dire == "U"):
        if(i[1] < self.y):
          t = i
          break
      else:
        pass
    return t


  def checkisin(self,v,b):
    for i in self.possCon:
      c = b[i[1]][i[0]]
      if(c.value == v):
        return True

    else:
      return False


  def __isValid__(self,move,board):
    oke = []
    for i in move:
      dire = i[0]
      count = int(i[1])
      obj = board[self.__findObje__(dire)[1]][self.__findObje__(dire)[0]]
      if(obj.value < 3):
        if(count > obj.remainingcon):
          oke.append(0)
        elif(count == 2 and obj.value == 2 and len(obj.possCon) > 1 and obj.checkisin(1,board)):
          oke.append(1)
        elif(count == 2 and obj.value == 2 and len(obj.possCon) > 1 and not obj.checkisin(1,board)):
          oke.append(0)
        elif(count == 2 and self.value == 2 and len(self.possCon) > 1):
          oke.append(0)
        elif(count == obj.remainingcon and len(obj.possCon) == 1):
          oke.append(1)
        else:
          oke.append(1)
      else:
        if(count == 2 and self.value == 2):
          if(len(self.possCon)>1 and len(obj.connections) > 1 and obj.remainingcon > 2):
            oke.append(0)
          elif(len(self.possCon)>1 and obj.remainingcon < 2):
            oke.append(0)
          else:
            oke.append(1)
        else:
          if(obj.remainingcon >= count):
            oke.append(1)
        
          else:
            oke.append(0)
    return oke



#print([1,1,2,3,4].count(1))