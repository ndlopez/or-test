"""
    Simple traveling salesperson problem between 10 cities
    The distance matrix is an array whose i, j entry is the distance from location i to location j in miles, where the array indices correspond to the locations in the following order:
    0,1,2,3,4,5,6,7,8,9,10,11,12,13,14
"""
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

"""
    data['distance_matrix'] = [
            [10,11,13,13,10,10,0,0,0,0,0,0,0,13,0],
            [20,0,0,0,20,20,21,23,0,0,0,0,0,20,0],
            [30,31,0,0,30,30,0,0,33,0,0,0,0,30,0],
            [0,0,0,0,40,41,0,0,41,0,0,0,0,41,0],
            [0,0,0,0,60,0,60,60,0,0,60,60,60,60,0],
            [70,0,0,0,70,70,71,0,0,71,0,0,0,0,0],
            [0,0,0,0,80,84,81,88,0,0,87,0,0,0,0],
            [90,0,92,0,0,90,0,0,0,0,0,0,91,0,0],
            [0,0,105,0,0,105,100,104,0,0,105,0,0,0,105]
            ]
    data['distance_matrix'15suppliers]=[
            [112,112,180,0,559,0,757,0],
            [108,0,189,0,0,0,0,0,0],
            [102,0,0,0,0,0,0,777,906],
            [102,0,0,0,0,0,0,0,0],
            [112,112,180,269,461,559,658,0,0],
            [112,112,180,279,0,559,697,757,906],
            [0,117,0,0,461,569,668,0,856],
            [0,128,0,0,461,0,737,0,896],
            [0,0,206,279,0,0,0,0,0],
            [0,0,0,0,0,569,0,0,0],
            [0,0,0,0,461,0,727,0,906],
            [0,0,0,0,461,0,0,0,0],
            [0,0,0,0,461,0,0,767,0],
            [102,112,180,279,461,0,0,0,0],
            [0,0,0,0,0,0,0,0,896]
            ]
"""
def create_data_model():
    #stores the data for the problem
    #distance_matrix values must be integers, either int(float_number) or float_number x100
    data = {}
    #considering all suppliers depart from node 15
    """data['distance_matrix'] = [
            [10,20,30,40,60,70,80,999,999],
            [10,20,30,41,999,70,84,90,105],
            [10,20,30,999,999,70,999,90,999],
            [11,999,31,999,999,999,999,999,999],
            [12,22,32,42,60,70,86,92,100],
            [13,999,999,999,999,999,999,999,999],
            [13,20,30,41,60,999,999,999,999],
            [13,999,999,999,999,999,999,92,105]
            ]"""
    data['distance_matrix']=[
        [0,0,0,0,0,0,0,0,0],
        [134, 214, 306, 402, 598, 697, 796, 0, 0],
        [128, 205, 297, 402, 0, 687, 826, 885, 1034,],
        [122, 197, 287, 0, 0, 677, 0, 875, 0],
        [122, 0, 287, 0, 0, 0, 0, 0, 0],
        [122, 197, 287, 383, 559, 657, 816, 875, 955],
        [122, 0, 0, 0, 0, 0, 0, 0, 0],
        [116, 164, 250, 354, 539, 0, 0, 0, 0],
        [111, 0, 0, 0, 0, 0, 0, 845, 895],
        ]

    data['num_vehicles'] = 1
    data['depot'] = 0 #starting point
    return data

def print_solution(manager, routing, solution):
    #prints available sol
    print('Obj: {}miles'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Route for vehicle 0:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index,index,0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    print(plan_output)
    plan_output += 'Route distance: {}miles\n'.format(route_distance)

def main():
    #instantiate the problem
    data = create_data_model()
    #create routing index mgr
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),data['num_vehicles'],data['depot'])
    #create routing model
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        #returns the distance between two nodes
        #convert routing_variable index -> distance matrix noteIndex
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]
    
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    #define cost of each arc
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    #setting 1st sol heuristic
    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    #solve the problem
    solution = routing.SolveWithParameters(search_params)

    #print sol
    if solution:
        print_solution(manager,routing,solution)

if __name__ == "__main__":
    main()
