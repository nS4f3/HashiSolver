from ortools.sat.python import cp_model

class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
  """Print intermediate solutions."""

  def __init__(self, variables):
    cp_model.CpSolverSolutionCallback.__init__(self)
    self.__variables = variables
    self.__solution_count = 0
    self.solutionslist = []

  def on_solution_callback(self):
    self.__solution_count += 1
    l = []
    for v in self.__variables:
      l.append("{}{}".format(v,self.Value(v)))
      #print('%s=%i' % (v, self.Value(v)), end=' ')
    self.solutionslist.append(l)
    #print()

  def solution_count(self):
    return self.__solution_count
