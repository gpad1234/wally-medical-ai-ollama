

# --- NLP Query Endpoint (OpenAI integration) ---
#!/usr/bin/env python3
"""
Graph Database Web UI
Provides interactive query interface with visualization and actions
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from graph_db import GraphDB
import json
import os
import logging
import traceback
import openai
import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('graph_web_ui.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)




app = Flask(__name__)

def resolve_node_id(name_or_id):
    """
    Resolve a node name (case-insensitive) or ID to the actual node ID if it exists.
    Returns the node ID if found, else None.
    """
    if not graph:
        return None
    # Try exact match first
    if graph.node_exists(name_or_id):
        return name_or_id
    # Try case-insensitive match
    for node_id in graph.get_all_nodes():
        if node_id.lower() == name_or_id.lower():
            return node_id
    return None

@app.route('/api/nlp_query', methods=['POST'])
def nlp_query():
    """Process a natural language query using OpenAI and map to graph actions"""
    try:
        data = request.json
        query = data.get('query', '')
        if not query:
            return jsonify({'error': 'No query provided'}), 400

        # Check if any API keys are available
        openai_api_key = os.getenv('OPENAI_API_KEY')
        anthropic_api_key = os.getenv('CLAUDE_CODE_KEY') or os.getenv('ANTHROPIC_API_KEY')
        
        if not openai_api_key and not anthropic_api_key:
            return jsonify({
                'error': 'NLP feature requires API keys. Set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable.',
                'feature_disabled': True
            }), 503

        # Compose a prompt for AI to map query to graph actions
        prompt = f"""
You are an assistant for a graph database. Map the user's natural language query to one of these actions:
- "stats": Return the number of nodes and edges.
- "visualization": Return the full graph data (nodes and edges).
- "list_nodes": List all node IDs.
- "list_edges": List all edges as (from, to, name, weight).
- "shortest_path": For shortest path queries, extract the start and target node names or IDs from the query and return action "shortest_path".
- "custom": For anything else, explain what you would do.

User query: {query}
Respond ONLY with a single line JSON object using double quotes for all keys and string values, e.g. {{"action": "stats", "explanation": "..."}}
"""
        # Try OpenAI first (only if key exists and looks valid)
        result = None
        openai_error = None
        if openai_api_key and openai_api_key.startswith('sk-') and len(openai_api_key) > 20:
            try:
                openai.api_key = openai_api_key
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "system", "content": "You are a helpful assistant."},
                              {"role": "user", "content": prompt}],
                    max_tokens=150,
                    temperature=0
                )
                content = response['choices'][0]['message']['content']
                try:
                    result = json.loads(content)
                except Exception as parse_exc:
                    openai_error = f'OpenAI response could not be parsed as JSON: {content[:100]}'
            except Exception as openai_exc:
                openai_error = f'OpenAI API error: {str(openai_exc)[:200]}'
        
        # If OpenAI didn't work, try Claude as backup
        if not result and anthropic_api_key:
            try:
                headers = {
                    "x-api-key": anthropic_api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                }
                data_payload = {
                    "model": "claude-3-5-sonnet-20241022",
                    "max_tokens": 256,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                }
                r = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=data_payload)
                if r.ok:
                    content = r.json()["content"][0]["text"]
                    result = json.loads(content.replace("'", '"'))
                else:
                    claude_error = f'Claude API error {r.status_code}: {r.text[:200]}'
            except Exception as claude_exc:
                claude_error = f'Claude API error: {str(claude_exc)[:200]}'
        
        # If neither worked, return error
        if not result:
            errors = []
            if openai_error:
                errors.append(f"OpenAI: {openai_error}")
            if 'claude_error' in locals():
                errors.append(f"Claude: {claude_error}")
            return jsonify({
                'error': 'NLP query failed. ' + '; '.join(errors) if errors else 'No valid API keys configured.',
                'feature_disabled': len(errors) == 0
            }), 500
        
        action = result.get('action')
        explanation = result.get('explanation', '')
        
        # Map action to backend
        if action == 'stats':
            node_ids = graph.get_all_nodes()
            edge_tuples = graph.get_all_edges()
            return jsonify({'action': action, 'explanation': explanation, 'nodes': len(node_ids), 'edges': len(edge_tuples)})
        elif action == 'visualization':
            # Reuse visualization logic
            return get_visualization_data()
        elif action == 'list_nodes':
            node_ids = graph.get_all_nodes()
            return jsonify({'action': action, 'explanation': explanation, 'nodes': node_ids})
        elif action == 'list_edges':
            edge_tuples = graph.get_all_edges()
            edges = []
            for edge in edge_tuples:
                edge_dict = {
                    'from': edge[0],
                    'to': edge[1],
                    'weight': edge[2] if len(edge) > 2 else None,
                    'name': edge[3] if len(edge) > 3 else None
                }
                edges.append(edge_dict)
            return jsonify({'action': action, 'explanation': explanation, 'edges': edges})
        elif action == 'shortest_path':
            # Try to extract start and target node names/IDs from the query or explanation
            import re
            match = re.search(r'from (?:node )?(\w+) to (?:node )?(\w+)', query, re.IGNORECASE)
            if match:
                start_raw, target_raw = match.group(1), match.group(2)
            else:
                # Try to find two words or numbers in the query
                tokens = re.findall(r'\b\w+\b', query)
                if len(tokens) >= 2:
                    start_raw, target_raw = tokens[0], tokens[1]
                else:
                    return jsonify({'action': action, 'explanation': explanation, 'error': 'Could not extract start and target nodes from your query. Please specify, e.g., "Find the shortest path from Alice to Frank."'}), 400
            # Resolve names/IDs to actual node IDs
            start = resolve_node_id(start_raw)
            target = resolve_node_id(target_raw)
            if not start or not target:
                return jsonify({'action': action, 'explanation': explanation, 'error': f'Could not find node(s): {start_raw if not start else ""} {target_raw if not target else ""}'}), 400
            # Call the backend shortest_path endpoint
            try:
                sp_resp = app.test_client().post('/api/graph/shortest_path', json={'start': start, 'target': target})
                if sp_resp.status_code == 200:
                    sp_data = sp_resp.get_json()
                    return jsonify({'action': action, 'explanation': explanation, 'start': start, 'target': target, 'path': sp_data.get('path'), 'cost': sp_data.get('cost'), 'algorithm': sp_data.get('algorithm')})
                else:
                    return jsonify({'action': action, 'explanation': explanation, 'error': sp_resp.get_json().get('error', 'Failed to compute shortest path')}), 400
            except Exception as e:
                return jsonify({'action': action, 'explanation': explanation, 'error': str(e)}), 500
        else:
            return jsonify({'action': action, 'explanation': explanation})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

app.config['DEBUG'] = False

# Enable CORS for React frontend and test pages
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173", "http://127.0.0.1:5173", 
                    "http://localhost:3000", "http://127.0.0.1:3000",
                    "http://localhost:8080", "http://127.0.0.1:8080"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

# Global graph database instance
graph = None

def initialize_sample_graph():
    """Initialize a sample graph for demonstration"""
    global graph
    graph = GraphDB(directed=True, weighted=True)
    
    # Sample social network
    graph.add_node('Alice', {'role': 'Developer', 'team': 'Backend'})
    graph.add_node('Bob', {'role': 'Designer', 'team': 'Frontend'})
    graph.add_node('Charlie', {'role': 'Manager', 'team': 'Product'})
    graph.add_node('Diana', {'role': 'Developer', 'team': 'Frontend'})
    graph.add_node('Eve', {'role': 'DevOps', 'team': 'Infrastructure'})
    graph.add_node('Frank', {'role': 'Developer', 'team': 'Backend'})
    
    # Relationships with weights (collaboration strength)
    graph.add_edge('Alice', 'Bob', weight=5)
    graph.add_edge('Alice', 'Frank', weight=9)
    graph.add_edge('Bob', 'Diana', weight=8)
    graph.add_edge('Charlie', 'Alice', weight=3)
    graph.add_edge('Charlie', 'Bob', weight=4)
    graph.add_edge('Diana', 'Eve', weight=6)
    graph.add_edge('Eve', 'Frank', weight=7)
    graph.add_edge('Frank', 'Diana', weight=5)

@app.route('/')
def index():
    """Main page"""
    return render_template('graph_ui.html')

@app.route('/chat')
def chat():
    """Chat interface"""
    return render_template('chat_ui.html')

@app.route('/favicon.ico')
def favicon():
    """Prevent 404 errors for favicon"""
    return '', 204

@app.route('/api/graph/stats', methods=['GET'])
def get_stats():
    """Get graph statistics"""
    try:
        logger.info("GET /api/graph/stats")
        if not graph:
            logger.error("Graph not initialized")
            return jsonify({'error': 'Graph not initialized'}), 400
        
        node_ids = graph.get_all_nodes()
        nodes = []
        for node_id in node_ids:
            node_data = graph.get_node(node_id)
            if node_data:
                nodes.append(node_data)
        
        # Get all edges as tuples and convert to dicts
        edge_tuples = graph.get_all_edges()
        edges = []
        for edge in edge_tuples:
            edge_dict = {
                'from': edge[0],
                'to': edge[1]
            }
            if len(edge) > 2 and edge[2] is not None:
                edge_dict['weight'] = edge[2]
            edges.append(edge_dict)
        
        logger.info(f"Stats: {len(nodes)} nodes, {len(edges)} edges")
        return jsonify({
            'node_count': len(nodes),
            'edge_count': len(edges),
            'directed': graph.directed,
            'weighted': graph.weighted
        })
    except Exception as e:
        logger.error(f"Error in get_stats: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/graph/nodes', methods=['GET'])
def get_all_nodes():
    """Get all nodes"""
    try:
        logger.info("GET /api/graph/nodes")
        if not graph:
            logger.error("Graph not initialized")
            return jsonify({'error': 'Graph not initialized'}), 400
        
        node_ids = graph.get_all_nodes()
        nodes = []
        for node_id in node_ids:
            node_data = graph.get_node(node_id)
            if node_data:
                nodes.append(node_data)
        
        logger.info(f"Returning {len(nodes)} nodes")
        return jsonify({'nodes': nodes})
    except Exception as e:
        logger.error(f"Error in get_all_nodes: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/graph/edges', methods=['GET'])
def get_all_edges():
    """Get all edges"""
    if not graph:
        return jsonify({'error': 'Graph not initialized'}), 400
    
    edge_tuples = graph.get_all_edges()
    edges = []
    for edge in edge_tuples:
        edge_dict = {
            'from': edge[0],
            'to': edge[1]
        }
        if len(edge) > 2 and edge[2] is not None:
            edge_dict['weight'] = edge[2]
        edges.append(edge_dict)
    
    return jsonify({'edges': edges})

@app.route('/api/graph/node/<node_id>', methods=['GET'])
def get_node(node_id):
    """Get specific node details"""
    if not graph:
        return jsonify({'error': 'Graph not initialized'}), 400
    
    node = graph.get_node(node_id)
    if not node:
        return jsonify({'error': f'Node {node_id} not found'}), 404
    
    neighbors = graph.get_neighbors(node_id)
    degree = graph.get_degree(node_id)
    
    return jsonify({
        'node': node,
        'neighbors': neighbors,
        'degree': degree
    })

@app.route('/api/graph/neighbors/<node_id>', methods=['GET'])
def get_neighbors(node_id):
    """Get neighbors of a node"""
    if not graph:
        return jsonify({'error': 'Graph not initialized'}), 400
    
    if not graph.node_exists(node_id):
        return jsonify({'error': f'Node {node_id} not found'}), 404
    
    neighbors = graph.get_neighbors(node_id)
    neighbor_details = []
    
    for neighbor_id in neighbors:
        neighbor = graph.get_node(neighbor_id)
        edge = graph.get_edge(node_id, neighbor_id)
        neighbor_details.append({
            'id': neighbor_id,
            'data': neighbor.get('data', {}),
            'edge': edge
        })
    
    return jsonify({'neighbors': neighbor_details})

@app.route('/api/graph/bfs', methods=['POST'])
def bfs_traversal():
    """Perform BFS traversal"""
    try:
        logger.info("POST /api/graph/bfs")
        if not graph:
            logger.error("Graph not initialized")
            return jsonify({'error': 'Graph not initialized'}), 400
        
        data = request.json
        logger.debug(f"BFS request data: {data}")
        start = data.get('start')
        target = data.get('target')
        
        if not start:
            return jsonify({'error': 'Start node required'}), 400
        
        if not graph.node_exists(start):
            return jsonify({'error': f'Start node {start} not found'}), 404
        
        if target and not graph.node_exists(target):
            return jsonify({'error': f'Target node {target} not found'}), 404
        
        result = graph.bfs(start, target)
        logger.info(f"BFS result: visited={len(result['visited'])}, path={result['path']}")
        
        return jsonify({
            'algorithm': 'BFS',
            'start': start,
            'target': target,
            'visited': result['visited'],
            'path': result['path'],
            'distances': result['distances']
        })
    except Exception as e:
        logger.error(f"Error in bfs_traversal: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/graph/dfs', methods=['POST'])
def dfs_traversal():
    """Perform DFS traversal"""
    try:
        logger.info("POST /api/graph/dfs")
        if not graph:
            logger.error("Graph not initialized")
            return jsonify({'error': 'Graph not initialized'}), 400
        
        data = request.json
        logger.debug(f"DFS request data: {data}")
        start = data.get('start')
        target = data.get('target')
        
        if not start:
            return jsonify({'error': 'Start node required'}), 400
        
        if not graph.node_exists(start):
            return jsonify({'error': f'Start node {start} not found'}), 404
        
        if target and not graph.node_exists(target):
            return jsonify({'error': f'Target node {target} not found'}), 404
        
        result = graph.dfs(start, target)
        logger.info(f"DFS result: visited={len(result['visited'])}, path={result['path']}")
        
        return jsonify({
            'algorithm': 'DFS',
            'start': start,
            'target': target,
            'visited': result['visited'],
            'path': result['path']
        })
    except Exception as e:
        logger.error(f"Error in dfs_traversal: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/graph/shortest_path', methods=['POST'])
def shortest_path():
    """Find shortest path using Dijkstra or BFS"""
    try:
        logger.info("POST /api/graph/shortest_path")
        if not graph:
            logger.error("Graph not initialized")
            return jsonify({'error': 'Graph not initialized'}), 400
        
        data = request.json
        logger.debug(f"Shortest path request data: {data}")
        start = data.get('start')
        target = data.get('target')
        
        if not start or not target:
            return jsonify({'error': 'Start and target nodes required'}), 400
        
        if not graph.node_exists(start):
            return jsonify({'error': f'Start node {start} not found'}), 404
        
        if not graph.node_exists(target):
            return jsonify({'error': f'Target node {target} not found'}), 404
        
        result = graph.shortest_path(start, target)
        
        algorithm = 'Dijkstra' if graph.weighted else 'BFS'
        logger.info(f"{algorithm} shortest path: {result['path']} (cost: {result['distance']})")
        
        return jsonify({
            'algorithm': algorithm,
            'start': start,
            'target': target,
            'path': result['path'],
            'cost': result['distance']
        })
    except Exception as e:
        logger.error(f"Error in shortest_path: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/graph/all_paths', methods=['POST'])
def all_paths():
    """Find all paths between two nodes"""
    try:
        logger.info("POST /api/graph/all_paths")
        if not graph:
            logger.error("Graph not initialized")
            return jsonify({'error': 'Graph not initialized'}), 400
        
        data = request.json
        logger.debug(f"All paths request data: {data}")
        start = data.get('start')
        target = data.get('target')
        max_depth = data.get('max_depth', 10)
        
        if not start or not target:
            return jsonify({'error': 'Start and target nodes required'}), 400
        
        if not graph.node_exists(start):
            return jsonify({'error': f'Start node {start} not found'}), 404
        
        if not graph.node_exists(target):
            return jsonify({'error': f'Target node {target} not found'}), 404
        
        paths = graph.find_all_paths(start, target, max_depth)
        
        # Calculate costs for weighted graphs
        path_details = []
        for path in paths:
            cost = 0
            if graph.weighted and len(path) > 1:
                for i in range(len(path) - 1):
                    edge = graph.get_edge(path[i], path[i+1])
                    if edge:
                        cost += edge.get('weight', 0)
            
            path_details.append({
                'path': path,
                'length': len(path) - 1,
                'cost': cost if graph.weighted else len(path) - 1
            })
        
        # Sort by cost
        path_details.sort(key=lambda x: x['cost'])
        
        logger.info(f"Found {len(paths)} paths between {start} and {target}")
        
        return jsonify({
            'start': start,
            'target': target,
            'count': len(paths),
            'paths': path_details
        })
    except Exception as e:
        logger.error(f"Error in all_paths: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/graph/search', methods=['POST'])
def search_nodes():
    """Search nodes by criteria"""
    try:
        logger.info("POST /api/graph/search")
        if not graph:
            logger.error("Graph not initialized")
            return jsonify({'error': 'Graph not initialized'}), 400
        
        data = request.json
        logger.debug(f"Search request data: {data}")
        key = data.get('key')
        value = data.get('value')
        
        if not key:
            return jsonify({'error': 'Search key required'}), 400
        
        # Search using predicate
        def predicate(node_id, node_data):
            data = node_data.get('data', {})
            if key not in data:
                return False
            if value is None:
                return True
            return str(data[key]).lower() == str(value).lower()
        
        result_ids = graph.find_nodes(predicate)
        logger.info(f"Search found {len(result_ids)} nodes matching key='{key}', value='{value}'")
        
        # Convert node IDs to full node objects
        results = []
        for node_id in result_ids:
            node_data = graph.get_node(node_id)
            if node_data:
                results.append(node_data)
        
        return jsonify({
            'key': key,
            'value': value,
            'count': len(results),
            'results': results
        })
    except Exception as e:
        logger.error(f"Error in search_nodes: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/graph/export/json', methods=['GET'])
def export_json():
    """Export graph as JSON"""
    try:
        logger.info("GET /api/graph/export/json")
        if not graph:
            logger.error("Graph not initialized")
            return jsonify({'error': 'Graph not initialized'}), 400
        
        json_data = graph.export_to_json()
        logger.info(f"Exported graph as JSON ({len(json_data)} chars)")
        return jsonify({'data': json_data})
    except Exception as e:
        logger.error(f"Error in export_json: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/graph/export/adjacency', methods=['GET'])
def export_adjacency():
    """Export graph as adjacency list"""
    try:
        logger.info("GET /api/graph/export/adjacency")
        if not graph:
            logger.error("Graph not initialized")
            return jsonify({'error': 'Graph not initialized'}), 400
        
        adjacency_data = graph.export_to_adjacency_list()
        logger.info(f"Exported graph as adjacency list ({len(adjacency_data)} chars)")
        return jsonify({'data': adjacency_data})
    except Exception as e:
        logger.error(f"Error in export_adjacency: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/graph/import/json', methods=['POST'])
def import_json():
    """Import graph from JSON"""
    global graph
    
    data = request.json
    json_data = data.get('json_data')
    
    if not json_data:
        return jsonify({'error': 'JSON data required'}), 400
    
    try:
        # Create new graph
        graph = GraphDB()
        graph.import_from_json(json_data)
        
        nodes = graph.get_all_nodes()
        edges = graph.get_all_edges()
        
        return jsonify({
            'success': True,
            'node_count': len(nodes),
            'edge_count': len(edges)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/graph/visualization', methods=['GET'])
def get_visualization_data():
    """Get graph data formatted for visualization"""
    try:
        logger.info("GET /api/graph/visualization")
        if not graph:
            logger.error("Graph not initialized")
            return jsonify({'error': 'Graph not initialized'}), 400
        
        # Get all node IDs and build full node objects
        node_ids = graph.get_all_nodes()
        logger.debug(f"Found {len(node_ids)} node IDs: {node_ids}")
        nodes = []
        for node_id in node_ids:
            node_data = graph.get_node(node_id)
            logger.debug(f"Node {node_id}: {node_data}")
            if node_data:
                nodes.append(node_data)
        
        # Get all edges as tuples and convert to dicts
        edge_tuples = graph.get_all_edges()
        edges = []
        for edge in edge_tuples:
            edge_dict = {
                'from': edge[0],
                'to': edge[1]
            }
            if len(edge) > 2 and edge[2] is not None:
                edge_dict['weight'] = edge[2]
            edges.append(edge_dict)
        
        # Format for visualization libraries (e.g., D3.js, vis.js)
        vis_nodes = []
        for node in nodes:
            vis_nodes.append({
                'id': node['id'],
                'label': node['id'],
                'title': json.dumps(node.get('data', {}), indent=2),
                'data': node.get('data', {})
            })
        
        vis_edges = []
        for edge in edges:
            edge_data = {
                'from': edge['from'],
                'to': edge['to'],
                'arrows': 'to' if graph.directed else ''
            }
            if graph.weighted and 'weight' in edge:
                edge_data['label'] = str(edge['weight'])
                edge_data['value'] = edge['weight']
            
            vis_edges.append(edge_data)
        
        logger.info(f"Visualization data: {len(vis_nodes)} nodes, {len(vis_edges)} edges")
        return jsonify({
            'nodes': vis_nodes,
            'edges': vis_edges,
            'options': {
                'directed': graph.directed,
                'weighted': graph.weighted
            }
        })
    except Exception as e:
        logger.error(f"Error in get_visualization_data: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/graph/reset', methods=['POST'])
def reset_graph():
    """Reset graph to sample data"""
    initialize_sample_graph()
    return jsonify({'success': True, 'message': 'Graph reset to sample data'})

@app.route('/api/graph/node', methods=['POST'])
def add_node():
    """Add a new node"""
    try:
        logger.info("POST /api/graph/node")
        if not graph:
            logger.error("Graph not initialized")
            return jsonify({'error': 'Graph not initialized'}), 400
        
        data = request.json
        logger.debug(f"Add node request: {data}")
        node_id = data.get('id')
        node_data = data.get('data', {})
        
        if not node_id:
            return jsonify({'error': 'Node ID required'}), 400
        
        if graph.node_exists(node_id):
            return jsonify({'error': f'Node {node_id} already exists'}), 409
        
        success = graph.add_node(node_id, node_data)
        
        if success:
            logger.info(f"Added node: {node_id}")
            return jsonify({
                'success': True,
                'message': f'Node {node_id} added',
                'node': {'id': node_id, 'data': node_data}
            })
        else:
            return jsonify({'error': 'Failed to add node'}), 500
    except Exception as e:
        logger.error(f"Error in add_node: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/graph/node/<node_id>', methods=['DELETE'])
def delete_node(node_id):
    """Delete a node"""
    try:
        logger.info(f"DELETE /api/graph/node/{node_id}")
        if not graph:
            logger.error("Graph not initialized")
            return jsonify({'error': 'Graph not initialized'}), 400
        
        if not graph.node_exists(node_id):
            return jsonify({'error': f'Node {node_id} not found'}), 404
        
        success = graph.delete_node(node_id)
        
        if success:
            logger.info(f"Deleted node: {node_id}")
            return jsonify({
                'success': True,
                'message': f'Node {node_id} deleted'
            })
        else:
            return jsonify({'error': 'Failed to delete node'}), 500
    except Exception as e:
        logger.error(f"Error in delete_node: {str(e)}")
        logger.error(traceback.format_exc())

@app.route('/api/graph/node/<node_id>', methods=['PUT'])
def update_node(node_id):
    """Update a node's data"""
    try:
        logger.info(f"PUT /api/graph/node/{node_id}")
        if not graph:
            logger.error("Graph not initialized")
            return jsonify({'error': 'Graph not initialized'}), 400
        
        if not graph.node_exists(node_id):
            return jsonify({'error': f'Node {node_id} not found'}), 404
        
        data = request.json
        logger.debug(f"Update node request data: {data}")
        
        if not data or 'data' not in data:
            return jsonify({'error': 'Node data required'}), 400
        
        node_data = data['data']
        success = graph.update_node(node_id, node_data)
        
        if success:
            logger.info(f"Updated node: {node_id} with data: {node_data}")
            return jsonify({
                'success': True,
                'message': f'Node {node_id} updated',
                'node': graph.get_node(node_id)
            })
        else:
            return jsonify({'error': 'Failed to update node'}), 500
    except Exception as e:
        logger.error(f"Error in update_node: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/graph/edge', methods=['POST'])
def add_edge():
    """Add a new edge"""
    try:
        logger.info("POST /api/graph/edge")
        if not graph:
            logger.error("Graph not initialized")
            return jsonify({'error': 'Graph not initialized'}), 400
        
        data = request.json
        logger.debug(f"Add edge request: {data}")
        from_node = data.get('from')
        to_node = data.get('to')
        weight = data.get('weight', 1.0)
        
        if not from_node or not to_node:
            return jsonify({'error': 'Both from and to nodes required'}), 400
        
        if not graph.node_exists(from_node):
            return jsonify({'error': f'Node {from_node} not found'}), 404
        
        if not graph.node_exists(to_node):
            return jsonify({'error': f'Node {to_node} not found'}), 404
        
        success = graph.add_edge(from_node, to_node, weight)
        
        if success:
            logger.info(f"Added edge: {from_node} -> {to_node} (weight: {weight})")
            return jsonify({
                'success': True,
                'message': f'Edge added: {from_node} -> {to_node}',
                'edge': {'from': from_node, 'to': to_node, 'weight': weight}
            })
        else:
            return jsonify({'error': 'Edge already exists or failed to add'}), 409
    except Exception as e:
        logger.error(f"Error in add_edge: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/graph/edge/<from_node>/<to_node>', methods=['DELETE'])
def delete_edge(from_node, to_node):
    """Delete an edge"""
    try:
        logger.info(f"DELETE /api/graph/edge/{from_node}/{to_node}")
        if not graph:
            logger.error("Graph not initialized")
            return jsonify({'error': 'Graph not initialized'}), 400
        
        success = graph.delete_edge(from_node, to_node)
        
        if success:
            logger.info(f"Deleted edge: {from_node} -> {to_node}")
            return jsonify({
                'success': True,
                'message': f'Edge deleted: {from_node} -> {to_node}'
            })
        else:
            return jsonify({'error': 'Edge not found or failed to delete'}), 404
    except Exception as e:
        logger.error(f"Error in delete_edge: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/templates/load/<template_name>', methods=['GET'])
def load_template(template_name):
    """Load a template dataset into the graph"""
    try:
        global graph
        logger.info(f"GET /api/templates/load/{template_name}")
        
        template_path = os.path.join(os.path.dirname(__file__), 'templates', f'{template_name}.json')
        
        if not os.path.exists(template_path):
            logger.error(f"Template not found: {template_path}")
            return jsonify({'error': f'Template {template_name} not found'}), 404
        
        with open(template_path, 'r') as f:
            template_data = json.load(f)
        
        # Clear existing graph
        graph = GraphDB(directed=True, weighted=True)
        
        # Load nodes
        for node in template_data.get('nodes', []):
            graph.add_node(node['id'], node.get('data', {}))
        
        # Load edges
        for edge in template_data.get('edges', []):
            graph.add_edge(edge['from'], edge['to'], edge.get('value', 1))
        
        logger.info(f"Loaded template {template_name}: {len(template_data['nodes'])} nodes, {len(template_data['edges'])} edges")
        
        return jsonify({
            'success': True,
            'message': f'Loaded template {template_name}',
            'nodes_loaded': len(template_data['nodes']),
            'edges_loaded': len(template_data['edges'])
        })
    except Exception as e:
        logger.error(f"Error loading template: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to load template: {str(e)}'}), 500

@app.route('/api/templates/list', methods=['GET'])
def list_templates():
    """List available templates"""
    try:
        logger.info("GET /api/templates/list")
        templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
        
        if not os.path.exists(templates_dir):
            return jsonify({'templates': []})
        
        templates = []
        for filename in os.listdir(templates_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(templates_dir, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                templates.append({
                    'name': filename[:-5],  # Remove .json
                    'display_name': data.get('name', filename[:-5]),
                    'description': data.get('description', ''),
                    'nodes': len(data.get('nodes', [])),
                    'edges': len(data.get('edges', []))
                })
        
        logger.info(f"Found {len(templates)} templates")
        return jsonify({'templates': templates})
    except Exception as e:
        logger.error(f"Error listing templates: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to list templates: {str(e)}'}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(e)}")
    logger.error(traceback.format_exc())
    return jsonify({'error': f'Internal server error: {str(e)}'}), 500

if __name__ == '__main__':
    try:
        # Load environment variables from .env if present
        load_dotenv()

        # Initialize with sample data
        logger.info("Initializing sample graph...")
        initialize_sample_graph()

        # Create templates directory if it doesn't exist
        os.makedirs('templates', exist_ok=True)

        print("=" * 60)
        print("Graph Database Web UI")
        print("=" * 60)
        print("Server starting at:")
        print("  - Local:   http://127.0.0.1:5001")
        print("  - Network: http://0.0.0.0:5001")
        print("")
        print("Logs written to: graph_web_ui.log")
        print("Press Ctrl+C to stop")
        print("=" * 60)

        logger.info("Starting Flask server on http://0.0.0.0:5001")
        # Set debug=False to prevent auto-restart on file changes
        # Set debug=True for development with auto-reload
        app.run(debug=False, host='0.0.0.0', port=5001)
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        logger.error(traceback.format_exc())
        raise
