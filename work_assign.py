# assign workers to tasks

from ortools.linear_solver import pywraplp

def main():
    #data
    costs = [
        [90, 80, 75, 70],
        [35, 85, 55, 65],
        [125, 95, 90, 95],
        [45, 110, 95, 115],
        [50, 100, 90, 100],
    ]
    num_workers = len(costs)
    num_tasks = len(costs[0])

    #solver
    solver = pywraplp.Solver.CreateSolver("SCIP")

    #vars
    # x[i,j] is an array of 0-1 vars, if worker is assign to task j then 1 else 0
    x = {}
    for i in range(num_workers):
        for j in range(num_tasks):
            x[i,j] = solver.IntVar(0,1,'')
    
    #constraints: each worker is assign to at most 1 task
    for i in range(num_workers):
        solver.Add(solver.Sum([x[i,j] for j in range(num_tasks)]) <= 1)
    #each task is assign to exactly one worker
    for j in range(num_tasks):
        solver.Add(solver.Sum([x[i,j] for i in range(num_workers)]) == 1)
    
    #obj
    obj_terms = []
    for i in range(num_workers):
        for j in range(num_tasks):
            obj_terms.append(costs[i][j]*x[i,j])
    solver.Minimize(solver.Sum(obj_terms))

    #solver
    status = solver.Solve()

    #print solution
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print(f'total cost = {solver.Objective().Value()}\n')
        for i in range(num_workers):
            for j in range(num_tasks):
                #test if x[i,j] =1
                if x[i,j].solution_value() > 0.5:
                    print(f'worker{i} assign to task {j}' + f' cost: {costs[i][j]}')
    else:
        print('no solution found :(')

if __name__ == "__main__":
    main()
