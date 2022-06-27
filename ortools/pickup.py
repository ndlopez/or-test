#simple pick-up and delivery

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def create_data():
    data = {}
    data['distance_matrix'] = [
        [0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354,
        468, 776, 662],
        [548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 1084, 594, 480, 674,
        1016, 868, 1210],
        [776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 1278, 1164,
        1130, 788, 1552, 754],
        [696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 1232, 514, 628, 822,
        1164, 560, 1358],
        [582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 1118, 400, 514, 708,
        1050, 674, 1244],
        [274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628,
        514, 1050, 708],
        [502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856,
        514, 1278, 480],
        [194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320,
        662, 742, 856],
        [308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662,
        320, 1084, 514],
        [194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388,
        274, 810, 468],
        [536, 1084, 400, 1232, 1118, 582, 354, 730, 388, 342, 0, 878, 764,
        730, 388, 1152, 354],
        [502, 594, 1278, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114,
        308, 650, 274, 844],
        [388, 480, 1164, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194,
        536, 388, 730],
        [354, 674, 1130, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0,
        342, 422, 536],
        [468, 1016, 788, 1164, 1050, 514, 514, 662, 320, 274, 388, 650, 536,
        342, 0, 764, 194],
        [776, 868, 1552, 560, 674, 1050, 1278, 742, 1084, 810, 1152, 274,
        388, 422, 764, 0, 798],
        [662, 1210, 754, 1358, 1244, 708, 480, 856, 514, 468, 354, 844, 730,
        536, 194, 798, 0],
    ]
    data['pickups_deliveries'] = [
        [1, 6],
        [2, 10],
        [4, 3],
        [5, 9],
        [7, 8],
        [15, 11],
        [13, 12],
        [16, 14],
    ]
    data['num_vehicles'] = 3
    data['depot'] = 0
    return data

def print_solution(data,manager,routing,solution):
    print(f'Obj: {solution.ObjectiveValue()}')
    total_distance=0
    for vehicle_id in range(data['num_vehicles']):
        idx = routing.Start(vehicle_id)
        plan_out = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        while not routing.IsEnd(idx):
            plan_out += ' {} -> '.format(manager.IndexToNode(idx))
            prev_idx = idx
            idx = solution.Value(routing.NextVar(idx))
            route_distance += routing.GetArcCostForVehicle(prev_idx,idx,vehicle_id)
        plan_out += '{}\n'.format(manager.IndexToNode(idx))
        plan_out += 'distance of the route: {}m\n'.format(route_distance)
        print(plan_out)
        total_distance += route_distance
    print('total distance of all route: {}m'.format(total_distance))

def main():
    #instant the data problem
    data = create_data()
    #create routing idx mgr
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),data['num_vehicles'],data['depot'])
    #create routing model
    routing = pywrapcp.RoutingModel(manager)

    #define cost of eeach arc
    def distance_callback(from_idx,to_idx):
        #returns the Manhattan dist between 2 nodes
        from_node = manager.IndexToNode(from_idx)
        to_node = manager.IndexToNode(to_idx)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_idx = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_idx)

    #add distance constraint
    dim_name = 'Distance'
    routing.AddDimension(
            transit_callback_idx,
            0, #no slack?
            3000, #vehicle max travel dist
            True, #start cumul to zero?
            dim_name)
    distance_dim = routing.GetDimensionOrDie(dim_name)
    distance_dim.SetGlobalSpanCostCoefficient(100)

    #define transport requests
    for request in data['pickups_deliveries']:
        pickup_idx = manager.NodeToIndex(request[0])
        deliv_idx = manager.NodeToIndex(request[1])
        routing.AddPickupAndDelivery(pickup_idx,deliv_idx)
        routing.solver().Add(routing.VehicleVar(pickup_idx)== routing.VehicleVar(deliv_idx))
        routing.solver().Add(distance_dim.CumulVar(pickup_idx) <= distance_dim.CumulVar(deliv_idx))

    #setting first solution: heuristic
    search_param = pywrapcp.DefaultRoutingSearchParameters()
    search_param.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION)

    #solve the problem
    solution = routing.SolveWithParameters(search_param)

    if solution:
        print_solution(data,manager,routing,solution)

if __name__ == "__main__":
    main()

