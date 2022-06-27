# traveling salesperson -> suppliers, lines problem
import math
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def create_data_model():
    #Stores data in pairs (supplier, line)
    data = {}
    """data['loci'] = [
            (0,10), (0,20), (0,40), (0,80), (0,30), (0,60), (0,70),
            (1,10), (1,20), (1,30), (1,41), (1,84), (1,90), (1,70), (1,92),
            (1,105), (2,10), (2,20), (2,30), (2,70), (2,90), (3,11), (3,31),
            (4,12), (4,32), (4,22), (4,42), (4,86), (4,100), (4,70), (4,92), 
            (4,60), (5,13), (6,13), (6,30), (6,41), (6,20), (6,60), (7,13),
            (7,92), (7,105)]"""
    data['loci'] = [
            [10,20,30,40,60,70,80,0,0],
            [10,20,30,41,70,84,90,92,105],
            [10,20,30,0,0,70,0,90,0],
            [11,0,31,0,0,0,0,0,0],
            [12,22,32,42,0,70,86,92,100],
            [13,0,0,0,0,0,0,0,0],
            [13,20,30,41,60,0,0,0],
            [13,0,0,0,0,0,0,92,105]
            ]
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data

def compute_euclidean_dist_matrix(locations):
    #creates callback to return distance between points
    distances = {}
    for from_counter, from_node in enumerate(locations):
        distances[from_counter] = {}
        for to_counter, to_node in enumerate(locations):
            if from_counter == to_counter:
                distances[from_counter][to_counter] = 0
            else:
                #Euclidean distance
                distances[from_counter][to_counter] = (int(math.hypot((from_node[0] - to_node[0]),(from_node[1]-to_node[1]))))
    
    return distances

def print_solution(manager,routing,solution):
    #prints solution to posole
    print('Obj: {}'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_out = 'Route:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_out += ' {} ->'.format(manager.IndexToNode(index))
        prev_idx = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(prev_idx,index,0)
    plan_out += ' {}\n'.format(manager.IndexToNode(index))
    print(plan_out)
    plan_out += 'Obj: {}m\n'.format(route_distance)

def main():
    #instant the data
    data = create_data_model()
    #create the routing idx mgr
    manager = pywrapcp.RoutingIndexManager(len(data['loci']),data['num_vehicles'], data['depot'])

    #create the route model
    routing = pywrapcp.RoutingModel(manager)
    distance_matrix = compute_euclidean_dist_matrix(data['loci'])
    print(str(distance_matrix))

    def distance_callback(from_idx,to_idx):
        #returns the dist betweeen 2 nodes
        #convert 1st from routing_var idx to dist_matrix nodeIdx
        from_node = manager.IndexToNode(from_idx)
        to_node = manager.IndexToNode(to_idx)
        return distance_matrix[from_node][to_node]

    transit_callback_idx = routing.RegisterTransitCallback(distance_callback)

    #define cost of each arc
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_idx)
    #set 1st heuristic solution
    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    #solve the problem
    solution = routing.SolveWithParameters(search_params)
    #print solution
    if solution:
        print_solution(manager,routing,solution)

if __name__ == "__main__":
    main()
