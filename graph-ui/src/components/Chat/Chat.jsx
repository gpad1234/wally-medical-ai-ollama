import React, { useState, useRef, useEffect } from 'react';
import { useGraphStore } from '../../store/graphStore';
import './Chat.css';

export const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);
  const { nodes, addNode, updateNode, deleteNode, addEdge, deleteEdge, shortestPath, bfs } = useGraphStore();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const processNaturalLanguage = async (query) => {
    const response = { type: 'text', content: '' };

    try {
      // Add node
      const addMatch = query.match(/add\s+(?:node\s+)?(\w+)(?:\s+with\s+(?:role|name)\s+([^,\n]+))?/i);
      if (addMatch) {
        const nodeId = addMatch[1];
        const nodeData = { role: 'unknown', team: 'general', name: nodeId };
        if (addMatch[2]) nodeData.role = addMatch[2].trim();
        await addNode(nodeId, nodeData);
        response.content = `✓ Added node '${nodeId}' to graph`;
        return response;
      }

      // Delete node
      const delMatch = query.match(/delete\s+(?:node\s+)?(\w+)|remove\s+(?:node\s+)?(\w+)/i);
      if (delMatch) {
        const nodeId = delMatch[1] || delMatch[2];
        await deleteNode(nodeId);
        response.content = `✓ Deleted node '${nodeId}'`;
        return response;
      }

      // Add edge
      const edgeMatch = query.match(/(?:add\s+)?(?:edge|link|connect)\s+(\w+)\s+(?:to|→|->)\s+(\w+)/i);
      if (edgeMatch) {
        const [, from, to] = edgeMatch;
        await addEdge(from, to);
        response.content = `✓ Added edge: ${from} → ${to}`;
        return response;
      }

      // Shortest path
      const pathMatch = query.match(/(?:shortest\s+)?path\s+(?:from\s+)?(\w+)\s+(?:to|→|->)\s+(\w+)/i);
      if (pathMatch) {
        const [, start, target] = pathMatch;
        const result = await shortestPath(start, target);
        const path = result.path || [];
        response.content = `Path from ${start} to ${target}: ${path.join(' → ')}`;
        return response;
      }

      // BFS
      const bfsMatch = query.match(/(?:BFS|breadth\s+first\s+search|traverse)\s+(?:from\s+)?(\w+)/i);
      if (bfsMatch) {
        const start = bfsMatch[1];
        const result = await bfs(start);
        const visited = result.visited || [];
        response.content = `BFS from ${start}: ${visited.join(', ')}`;
        return response;
      }

      // List nodes
      if (query.match(/(?:list|show|get)\s+(?:all\s+)?nodes|what\s+nodes/i)) {
        const nodeList = nodes.map(n => n.id).join(', ');
        response.content = `Nodes in graph: ${nodeList}`;
        return response;
      }

      // Default response
      response.content = "I didn't understand that. Try: 'add node Alice', 'connect Alice to Bob', 'path from Alice to Bob'";
    } catch (error) {
      response.content = `Error: ${error.message}`;
    }

    return response;
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    // Add user message
    const userMsg = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');

    // Process and respond
    const response = await processNaturalLanguage(input);
    setMessages(prev => [...prev, { role: 'assistant', content: response.content }]);
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h2>Graph Chat</h2>
      </div>
      <div className="chat-messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <span className="role">{msg.role === 'user' ? 'You' : 'Assistant'}</span>
            <span className="content">{msg.content}</span>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div className="chat-input">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Ask me anything... (e.g., 'add node Alice')"
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
};
