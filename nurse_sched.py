# Nurse scheduling problem with shift requests

from ortools.sat.python import cp_model
def main():
    """
    This program tries to find an optimal assignment of nurses to shifts
    3shifts/day for 7 days, subject to some constraints:
    Each nurse can request to be assigned to specific shifts
    the optimal assignment maximizes the number of fulfilled shift requests.
    """
    num_nurses = 8 #num_suppliers
    num_shifts = 9 #num_lines
    num_days = 9 #num_lines
    all_nurses = range(num_nurses)
    all_shifts = range(num_shifts)
    all_days = range(num_days)

    shift_requests = [[[1,0,0,0,0,0,0,0,0], [0,1,0,0,0,0,0,0,0],[0,0,1,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0],[0,0,0,0,1,0,0,0,0],[0,0,0,0,0,1,0,0,0],[0,0,0,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]],
                      [[1,0,0,0,0,0,0,0,0], [0,1,0,0,0,0,0,0,0],[0,0,1,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,1,0,0,0],[0,0,0,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,0,1]],
                      [[1,0,0,0,0,0,0,0,0], [0,1,0,0,0,0,0,0,0],[0,0,1,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,1,0,0,0],[0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,0,0]],
                      [[1,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0],[0,0,1,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]],
                      [[1,0,0,0,0,0,0,0,0], [0,1,0,0,0,0,0,0,0],[0,0,1,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0],[0,0,0,0,1,0,0,0,0],[0,0,0,0,0,1,0,0,0],[0,0,0,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,0,1]],
                      [[1,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]],
                      [[1,0,0,0,0,0,0,0,0], [0,1,0,0,0,0,0,0,0],[0,0,1,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0],[0,0,0,0,1,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]],
                      [[1,0,0,0,0,0,0,1,1], [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,0,1]]
                      ]

    #creates the model
    model = cp_model.CpModel()
    #creates shift vars
    #shifts [(n,d,s)]: nurse 'n' works shift 's' on day 'd'
    shifts = {}
    for n in all_nurses:
        for d in all_days:
            for s in all_shifts:
                shifts[(n,d,s)] = model.NewBoolVar('shift_n%id%is%i' %(n,d,s))
    
    #each shift is assigned to exactly one nurse in
    for d in all_days:
        for s in all_shifts:
            model.AddExactlyOne(shifts[(n,d,s)] for n in all_nurses)
    
    #each nurse works at most one shift per day
    for n in all_nurses:
        for d in all_days:
            model.AddAtMostOne(shifts[(n,d,s)] for s in all_shifts)
    
    #distr shifts evenly, so that each nurse works min_shifts_per_nurse shifts
    #when not possible, due to total number of shifts is not div by the number of nurses,
    #some nurses will be assigned one more shift
    min_shifts_per_nurse = (num_shifts * num_days) // num_nurses
    if num_shifts * num_days % num_nurses == 0:
        max_shifts_per_nurse = min_shifts_per_nurse
    else:
        max_shifts_per_nurse = min_shifts_per_nurse + 1
    for n in all_nurses:
        num_shifts_worked = 0
        for d in all_days:
            for s in all_shifts:
                num_shifts_worked += shifts[(n,d,s)]
        model.Add(min_shifts_per_nurse <= num_shifts_worked)
        model.Add(num_shifts_worked <= max_shifts_per_nurse)
    model.Maximize(sum(shift_requests[n][d][s] * shifts[(n,d,s)] for n in all_nurses for d in all_days for s in all_shifts))

    #creates the solver and solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        print('solution:')
        for d in all_days:
            print('line',d)
            for n in all_nurses:
                for s in all_shifts:
                    if solver.Value(shifts[(n,d,s)]) == 1:
                        if shift_requests[n][d][s] == 1:
                            print('supplier',n,'sends shit',s,'(requested).')
                        else:
                            print('Supplier',n,'sends shit',s,'(not requested)')
            print()
        print(f"Number of shift requests met = {solver.ObjectiveValue()}",f"(out of {num_nurses * min_shifts_per_nurse})")
    else:
        print('No optimal solution found :(')
    
    #stats
    print('\nStats')
    print('  - conflicts: %i' % solver.NumConflicts())
    print('  - branches : %i' % solver.NumBranches())
    print('  - wall time: %f s' % solver.WallTime())

if __name__ == "__main__":
    main()

