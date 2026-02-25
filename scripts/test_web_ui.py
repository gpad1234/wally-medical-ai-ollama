#!/usr/bin/env python3
"""
Quick test script for Graph Database Web UI
Tests API endpoints without starting the full server
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_web_ui():
    """Test that all components are available"""
    
    print("=" * 60)
    print("Graph Database Web UI - Component Test")
    print("=" * 60)
    
    # Test 1: Import Flask
    try:
        import flask
        print("✓ Flask installed:", flask.__version__)
    except ImportError as e:
        print("✗ Flask not installed:", str(e))
        print("  Run: pip3 install flask")
        return False
    
    # Test 2: Import GraphDB
    try:
        from graph_db import GraphDB
        print("✓ GraphDB module available")
    except ImportError as e:
        print("✗ GraphDB import failed:", str(e))
        return False
    
    # Test 3: Check template file
    template_path = os.path.join('templates', 'graph_ui.html')
    if os.path.exists(template_path):
        print(f"✓ Template file exists: {template_path}")
    else:
        print(f"✗ Template file missing: {template_path}")
        return False
    
    # Test 4: Create sample graph
    try:
        graph = GraphDB(directed=True, weighted=True)
        graph.add_node('A', {'label': 'Node A'})
        graph.add_node('B', {'label': 'Node B'})
        graph.add_edge('A', 'B', weight=5)
        
        nodes = graph.get_all_nodes()
        edges = graph.get_all_edges()
        
        print(f"✓ Graph operations work: {len(nodes)} nodes, {len(edges)} edges")
    except Exception as e:
        print("✗ Graph operations failed:", str(e))
        return False
    
    # Test 5: Test traversal algorithms
    try:
        graph.add_node('C', {'label': 'Node C'})
        graph.add_edge('B', 'C', weight=3)
        
        result = graph.bfs('A', 'C')
        if result['path'] == ['A', 'B', 'C']:
            print("✓ BFS algorithm works correctly")
        else:
            print(f"✗ BFS returned unexpected path: {result['path']}")
            return False
        
        result = graph.shortest_path('A', 'C')
        if result['path'] == ['A', 'B', 'C'] and result['distance'] == 8:
            print("✓ Dijkstra algorithm works correctly")
        else:
            print(f"✗ Dijkstra returned: path={result['path']}, distance={result['distance']}")
            return False
        
    except Exception as e:
        print("✗ Traversal algorithms failed:", str(e))
        return False
    
    # Test 6: Check web UI file
    web_ui_path = 'graph_web_ui.py'
    if os.path.exists(web_ui_path):
        print(f"✓ Web UI file exists: {web_ui_path}")
    else:
        print(f"✗ Web UI file missing: {web_ui_path}")
        return False
    
    print("\n" + "=" * 60)
    print("✓ All components ready!")
    print("=" * 60)
    print("\nTo start the web UI:")
    print("  make run-web-ui")
    print("\nOr directly:")
    print("  python3 graph_web_ui.py")
    print("\nThen open: http://127.0.0.1:5000")
    print("=" * 60)
    
    return True

if __name__ == '__main__':
    success = test_web_ui()
    sys.exit(0 if success else 1)
