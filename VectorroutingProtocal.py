MAX_NODES = 7
MAX_ROUTES = 128        
MAX_TTL = 14           
MAX_ROUNDS = MAX_NODES - 1
INFINITY = float('inf') 

edges = [
    (0, 1, 1), (0, 2, 1), (0, 4, 1), (0, 5, 1),
    (1, 2, 1), (2, 3, 1), (3, 6, 1), (6, 5, 1)
]

def initialize_neighbors():
    neighbors = {node: [] for node in range(MAX_NODES)}
    for node1, node2, weight in edges:
        neighbors[node1].append((node2, weight))
        neighbors[node2].append((node1, weight))
    return neighbors

neighbors = initialize_neighbors()

class Route:
    def __init__(self, destination, next_hop, cost):  
        self.destination = destination
        self.next_hop = next_hop
        self.cost = cost
        self.ttl = MAX_TTL

routing_tables = {node: [] for node in range(MAX_NODES)}

distance_vectors = {}
for node in range(MAX_NODES):
    distance_vectors[node] = [
        (INFINITY, None) for _ in range(MAX_NODES)
    ]
    distance_vectors[node][node] = (0, node)
    for neighbor, weight in neighbors[node]:
        distance_vectors[node][neighbor] = (weight, neighbor)
        routing_tables[node].append(Route(neighbor, neighbor, weight))

def merge_route(routing_table, new_route):
    for route in routing_table:
        if route.destination == new_route.destination:
            if new_route.cost < route.cost:
                route.cost = new_route.cost
                route.next_hop = new_route.next_hop
                route.ttl = MAX_TTL  
                return
            elif new_route.next_hop == route.next_hop:
                route.ttl = MAX_TTL  
                return
    if len(routing_table) < MAX_ROUTES: 
        routing_table.append(new_route)
    else:
        print("Routing table full, cannot add new route.")

print("Initial distance vector of A (node 0):", distance_vectors[0])

for round in range(MAX_ROUNDS):
    print(f"\nRound {round + 1}:")
    updated = False
    old_distance_vectors = {node: distance_vectors[node][:] for node in range(MAX_NODES)}

    for node in range(MAX_NODES):
        new_vector = distance_vectors[node][:]
        if node == 0:
            print("\nVectors received by A from neighbors:")
            for neighbor, _ in neighbors[0]:
                print(f"From neighbor {neighbor}: {old_distance_vectors[neighbor]}")

        for neighbor, weight in neighbors[node]:
            for dest in range(MAX_NODES):
                neighbor_distance, _ = old_distance_vectors[neighbor][dest]
                if neighbor_distance != INFINITY:
                    new_distance = neighbor_distance + weight
                    current_distance, _ = new_vector[dest]

                    if new_distance < current_distance:
                        new_vector[dest] = (new_distance, neighbor)
                        merge_route(routing_tables[node], Route(dest, neighbor, new_distance))
                        updated = True

        distance_vectors[node] = new_vector
        if node == 0:
            print("\nUpdated distance vector of A after receiving from neighbors:")
            print([(dist, next_hop) for dist, next_hop in distance_vectors[0]])
    for node in range(MAX_NODES):
        routing_tables[node] = [route for route in routing_tables[node] if route.ttl > 0]
        for route in routing_tables[node]:
            route.ttl -= 1

    if not updated:
        print("\nDistance vectors have converged.")
        break
print("\nFinal distance vector of A (node 0):")
print([(dist, next_hop) for dist, next_hop in distance_vectors[0]])

print("\nFinal routing table of A (node 0):")
for route in routing_tables[0]:
    print(f"Destination: {route.destination}, NextHop: {route.next_hop}, Cost: {route.cost}, TTL: {route.ttl}")