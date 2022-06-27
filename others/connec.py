from ortools.sat.python import cp_model
import matplotlib.pyplot as plt
import networkx as nx

class SolutionPrint(cp_model.CpSolverSolutionCallback):
    def __init__(self,varias,limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = varias
        self.__solution_count = 0
        self.__solution_limit = limit
        self.colors = ["red","blue","green"]
        self.node_colors = []

    #this is a callback func which is called
    def OnSolutionCallback(self):
        self.__solution_count += 1
        for var in self.__variables:
            print('{} = {}'.format(var,self.colors[self.Value(var)]),end="\n")
            self.node_colors.append(self.colors[self.Value(var)])
        print()
        if self.__solution_count >= self.__solution_limit:
            print("Stop search after {} solutions".format(self.__solution_limit))
            self.StopSearch()

    def SolutionCount(self):
        return self.__solution_count,self.node_colors

#func to solve the graph coloring problem
def graph_coloring(num_nodes,connections,k,num_solutions=2):
    #instant the CpModel
    model = cp_model.CpModel()
    #forEach node create a var range 0 -> k, color
    nodes = [model.NewIntVar(0,k-1,'x%i' %i) for i in range(num_nodes)]
    print(nodes)

    #add a constraint (i.e. value of node A != value of node B)
    for i,conn in enumerate(connections):
        model.Add(nodes[conn[0]] != nodes[conn[1]])

    #instant solver
    solver = cp_model.CpSolver()
    #instant a callback func to print solution
    solution_printer = SolutionPrint(nodes,num_solutions)

    #search for all solutions
    status = solver.SearchForAllSolutions(model,solution_printer)
    count,colors = solution_printer.SolutionCount()
    print("solution found: %i" % count)

    #return color values
    return colors

#define number of nodes in the graph
num_nodes = 12
#set number of colors as domain
domain = 4
#add connection forEach edge
connections = [
               (0,10),(1,10),(2,10),(3,10),(4,10),(5,10),(6,10),(7,10),
               (0,20),(1,20),(2,20),(4,20),(6,20),
               (3,30),(0,30),(1,30),(2,30),(4,30),(6,30),
               (0,40),(1,40),(4,40),(6,40)
]
#define number of solutions required
num_sol = 1

#plot grapg
g1 = nx.Graph()
for xcon in connections:
    g1.add_edge(xcon[0],xcon[1],color="black")
plt.subplot(121)
nx.draw(g1,with_labels=True,font_weight="bold")
plt.savefig("raw.png")

#call the graph coloring func to solve the graph for given colors
colors = graph_coloring(num_nodes,connections,domain,num_sol)

#plot a processed graph
plt.subplot(122)
assign_colors = []
for node in g1.nodes():
    assign_colors.append(colors[node])
nx.draw(g1,node_color=assign_colors,with_labels=True,font_weight='bold')
plt.savefig("processed.png")

