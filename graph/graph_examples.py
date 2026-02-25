"""
Graph Database - Practical Examples

Demonstrates:
- Importing graphs from text files
- Graph traversal use cases
- Node search and queries
- Export to different formats
- Real-world scenarios
"""

from graph_db import GraphDB
import json


def example_1_social_network():
    """Example: Social network graph"""
    print("=" * 70)
    print("EXAMPLE 1: Social Network Graph")
    print("=" * 70)
    print()
    
    # Create undirected graph (friendships are bidirectional)
    graph = GraphDB(directed=False, weighted=False)
    
    # Add people
    people = [
        ("alice", {"name": "Alice", "age": 30, "city": "NYC"}),
        ("bob", {"name": "Bob", "age": 25, "city": "SF"}),
        ("charlie", {"name": "Charlie", "age": 35, "city": "NYC"}),
        ("diana", {"name": "Diana", "age": 28, "city": "LA"}),
        ("eve", {"name": "Eve", "age": 32, "city": "NYC"}),
    ]
    
    for person_id, data in people:
        graph.add_node(person_id, data)
    
    # Add friendships
    friendships = [
        ("alice", "bob"),
        ("alice", "charlie"),
        ("bob", "diana"),
        ("charlie", "eve"),
        ("diana", "eve"),
    ]
    
    for person1, person2 in friendships:
        graph.add_edge(person1, person2)
    
    print("Social Network:")
    print(graph.export_to_adjacency_list())
    print()
    
    # Find people in NYC
    print("Finding people in NYC:")
    nyc_people = graph.find_nodes(lambda id, data: data.get("city") == "NYC")
    for person_id in nyc_people:
        data = graph.get_node(person_id)
        print(f"  {data['name']} (age {data['age']})")
    print()
    
    # Find mutual friends (people connected to Alice)
    print("Alice's network (BFS):")
    bfs = graph.bfs("alice")
    for person_id in bfs['visited'][1:]:  # Skip Alice herself
        data = graph.get_node(person_id)
        distance = bfs['distances'][person_id]
        print(f"  {data['name']} - {distance} degree(s) of separation")
    print()
    
    # Find path between two people
    print("Connection path from Alice to Eve:")
    path_result = graph.shortest_path("alice", "eve")
    path_names = [graph.get_node(p)['name'] for p in path_result['path']]
    print(f"  {' -> '.join(path_names)}")
    print(f"  Degrees of separation: {path_result['distance']}")
    print()


def example_2_file_import_export():
    """Example: Import/export from files"""
    print("=" * 70)
    print("EXAMPLE 2: Import/Export from Files")
    print("=" * 70)
    print()
    
    # Create adjacency list format
    adjacency_text = """
# Web page link structure
index -> about, products, contact
about -> team, history
products -> product1, product2, product3
product1 -> cart
product2 -> cart
product3 -> cart
cart -> checkout
checkout -> confirmation
team -> contact
history -> contact
    """
    
    print("Importing from adjacency list format:")
    print(adjacency_text)
    
    graph = GraphDB(directed=True, weighted=False)
    graph.import_from_adjacency_list(adjacency_text)
    
    print(f"✓ Imported {graph.get_stats()['nodes']} nodes, {graph.get_stats()['edges']} edges")
    print()
    
    # Find paths from index to confirmation
    print("All navigation paths from index to confirmation:")
    paths = graph.find_all_paths("index", "confirmation", max_length=10)
    for i, path in enumerate(paths, 1):
        print(f"  Path {i}: {' → '.join(path)}")
    print()
    
    # Export to JSON
    print("Exporting to JSON format:")
    json_str = graph.export_to_json(pretty=True)
    
    # Save to file
    with open("website_graph.json", "w") as f:
        f.write(json_str)
    print("✓ Saved to website_graph.json")
    print()
    
    # Re-import from JSON
    graph2 = GraphDB()
    with open("website_graph.json", "r") as f:
        graph2.import_from_json(f.read())
    
    print(f"✓ Re-imported: {graph2.get_stats()['nodes']} nodes, {graph2.get_stats()['edges']} edges")
    print()


def example_3_weighted_routes():
    """Example: Road network with distances"""
    print("=" * 70)
    print("EXAMPLE 3: Road Network (Weighted Graph)")
    print("=" * 70)
    print()
    
    # Create weighted graph for cities and distances
    graph = GraphDB(directed=False, weighted=True)
    
    # Add cities
    cities = ["NYC", "Boston", "Philadelphia", "Washington", "Baltimore"]
    for city in cities:
        graph.add_node(city, {"type": "city"})
    
    # Add roads with distances (in miles)
    roads = [
        ("NYC", "Boston", 215),
        ("NYC", "Philadelphia", 95),
        ("Philadelphia", "Washington", 140),
        ("Philadelphia", "Baltimore", 100),
        ("Baltimore", "Washington", 40),
        ("Washington", "NYC", 225),
    ]
    
    for city1, city2, distance in roads:
        graph.add_edge(city1, city2, float(distance))
    
    print("Road Network:")
    print(graph.export_to_adjacency_list())
    print()
    
    # Find shortest route
    print("Shortest route from NYC to Washington:")
    shortest = graph.shortest_path("NYC", "Washington")
    print(f"  Route: {' -> '.join(shortest['path'])}")
    print(f"  Distance: {shortest['distance']:.0f} miles")
    print()
    
    # Find all routes
    print("All routes from NYC to Washington:")
    all_routes = graph.find_all_paths("NYC", "Washington")
    for i, route in enumerate(all_routes, 1):
        # Calculate total distance
        total_dist = 0
        for j in range(len(route) - 1):
            neighbors = graph.get_neighbors(route[j])
            for neighbor in neighbors:
                if neighbor['to'] == route[j+1]:
                    total_dist += neighbor['weight']
                    break
        
        print(f"  Route {i}: {' -> '.join(route)} ({total_dist:.0f} miles)")
    print()


def example_4_dependency_graph():
    """Example: Software package dependencies"""
    print("=" * 70)
    print("EXAMPLE 4: Package Dependency Graph")
    print("=" * 70)
    print()
    
    # Create directed graph for dependencies
    graph = GraphDB(directed=True, weighted=False)
    
    # Define packages with dependencies
    packages = {
        "app": ["web-framework", "database-driver", "logging"],
        "web-framework": ["http-server", "routing", "template-engine"],
        "database-driver": ["connection-pool", "query-builder"],
        "http-server": ["socket-lib"],
        "routing": [],
        "template-engine": ["parser"],
        "connection-pool": ["socket-lib"],
        "query-builder": ["parser"],
        "socket-lib": [],
        "parser": [],
        "logging": ["file-io"],
        "file-io": [],
    }
    
    # Add all packages as nodes
    for package in packages.keys():
        graph.add_node(package, {"type": "package"})
    
    # Add dependencies as edges
    for package, deps in packages.items():
        for dep in deps:
            graph.add_edge(package, dep)
    
    print("Package Dependencies:")
    print(graph.export_to_adjacency_list())
    print()
    
    # Find all dependencies of app (BFS)
    print("All dependencies of 'app' (installation order):")
    bfs_result = graph.bfs("app")
    for i, pkg in enumerate(reversed(bfs_result['visited']), 1):
        level = bfs_result['distances'].get(pkg, 0)
        print(f"  {i}. {pkg} (level {level})")
    print()
    
    # Find which packages depend on 'socket-lib'
    print("Packages that depend on 'socket-lib':")
    all_nodes = graph.get_all_nodes()
    dependents = []
    for node in all_nodes:
        paths = graph.find_all_paths(node, "socket-lib")
        if paths:
            dependents.append(node)
    
    for dep in dependents:
        print(f"  {dep}")
    print()


def example_5_graph_operations():
    """Example: Dynamic graph modifications"""
    print("=" * 70)
    print("EXAMPLE 5: Dynamic Graph Operations")
    print("=" * 70)
    print()
    
    graph = GraphDB(directed=True)
    
    # Build initial graph
    print("Building initial graph...")
    for i in range(1, 6):
        graph.add_node(f"N{i}", {"value": i * 10})
    
    graph.add_edge("N1", "N2")
    graph.add_edge("N1", "N3")
    graph.add_edge("N2", "N4")
    graph.add_edge("N3", "N4")
    graph.add_edge("N4", "N5")
    
    print("Initial state:")
    print(graph.export_to_adjacency_list())
    print(f"Stats: {graph.get_stats()}")
    print()
    
    # Update node data
    print("Updating N3 data...")
    graph.update_node("N3", {"value": 100, "updated": True})
    print(f"N3 data: {graph.get_node('N3')}")
    print()
    
    # Add new node and edges
    print("Adding new node N6...")
    graph.add_node("N6", {"value": 60})
    graph.add_edge("N3", "N6")
    graph.add_edge("N6", "N5")
    print("After addition:")
    print(graph.export_to_adjacency_list())
    print()
    
    # Delete an edge
    print("Deleting edge N1 -> N2...")
    graph.delete_edge("N1", "N2")
    print("After edge deletion:")
    print(graph.export_to_adjacency_list())
    print()
    
    # Check connectivity after deletion
    print("Can still reach N5 from N1?")
    path = graph.shortest_path("N1", "N5")
    if path['path']:
        print(f"  Yes: {' -> '.join(path['path'])}")
    else:
        print("  No path found")
    print()
    
    # Delete a node
    print("Deleting node N4...")
    graph.delete_node("N4")
    print("After node deletion:")
    print(graph.export_to_adjacency_list())
    print()
    
    # Check connectivity after node deletion
    print("Can still reach N5 from N1?")
    path = graph.shortest_path("N1", "N5")
    if path['path']:
        print(f"  Yes: {' -> '.join(path['path'])}")
    else:
        print("  No - N5 is unreachable")
    print()


def example_6_json_workflow():
    """Example: Complete JSON workflow"""
    print("=" * 70)
    print("EXAMPLE 6: JSON Import/Export Workflow")
    print("=" * 70)
    print()
    
    # Create sample JSON
    sample_json = {
        "directed": True,
        "weighted": True,
        "nodes": [
            {"id": "START", "data": {"label": "Entry Point", "type": "input"}},
            {"id": "PROC1", "data": {"label": "Process 1", "type": "compute"}},
            {"id": "PROC2", "data": {"label": "Process 2", "type": "compute"}},
            {"id": "DECISION", "data": {"label": "Decision", "type": "branch"}},
            {"id": "END", "data": {"label": "Exit Point", "type": "output"}},
        ],
        "edges": [
            {"from": "START", "to": "PROC1", "weight": 1.0},
            {"from": "PROC1", "to": "DECISION", "weight": 2.0},
            {"from": "DECISION", "to": "PROC2", "weight": 1.0},
            {"from": "DECISION", "to": "END", "weight": 3.0},
            {"from": "PROC2", "to": "END", "weight": 1.0},
        ]
    }
    
    # Save to file
    with open("workflow_graph.json", "w") as f:
        json.dump(sample_json, f, indent=2)
    
    print("✓ Created workflow_graph.json")
    print()
    
    # Import from file
    graph = GraphDB()
    with open("workflow_graph.json", "r") as f:
        graph.import_from_json(f.read())
    
    print(f"✓ Imported graph: {graph}")
    print()
    
    # Analyze workflow
    print("Workflow paths from START to END:")
    paths = graph.find_all_paths("START", "END")
    for i, path in enumerate(paths, 1):
        # Calculate cost
        cost = 0
        for j in range(len(path) - 1):
            neighbors = graph.get_neighbors(path[j])
            for neighbor in neighbors:
                if neighbor['to'] == path[j+1]:
                    cost += neighbor.get('weight', 0)
                    break
        
        print(f"  Path {i}: {' -> '.join(path)} (cost: {cost})")
    print()
    
    # Find optimal path
    print("Optimal path (lowest cost):")
    optimal = graph.shortest_path("START", "END")
    print(f"  {' -> '.join(optimal['path'])}")
    print(f"  Total cost: {optimal['distance']}")
    print()


def main():
    """Run all examples"""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "GRAPH DATABASE - PRACTICAL EXAMPLES" + " " * 18 + "║")
    print("╚" + "═" * 68 + "╝")
    print("\n")
    
    example_1_social_network()
    print("\n")
    
    example_2_file_import_export()
    print("\n")
    
    example_3_weighted_routes()
    print("\n")
    
    example_4_dependency_graph()
    print("\n")
    
    example_5_graph_operations()
    print("\n")
    
    example_6_json_workflow()
    print("\n")
    
    print("=" * 70)
    print("All examples completed successfully!")
    print("=" * 70)
    print()
    print("Generated files:")
    print("  - website_graph.json")
    print("  - workflow_graph.json")
    print()


if __name__ == "__main__":
    main()
