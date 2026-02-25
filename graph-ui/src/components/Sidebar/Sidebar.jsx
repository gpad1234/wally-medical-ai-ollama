import React, { useState, useEffect } from 'react';
import { useGraphStore } from '../../store/graphStore';
import { NodePropertyDialog } from '../NodePropertyDialog/NodePropertyDialog';
import api from '../../services/api';
import './Sidebar.css';

import { Chat } from '../Chat/Chat';

export const Sidebar = ({ showChat }) => {
  const { nodes, edges, stats, selectedNode, fetchVisualization, fetchStats, deleteNode } = useGraphStore();
  const [nodeDialogOpen, setNodeDialogOpen] = useState(false);
  const [selectedNodeForDialog, setSelectedNodeForDialog] = useState(null);
  const [templates, setTemplates] = useState([]);
  const [loadingTemplate, setLoadingTemplate] = useState(null);

  React.useEffect(() => {
    fetchVisualization();
    fetchStats();
    const interval = setInterval(fetchStats, 5000);
    return () => clearInterval(interval);
  }, []);

  // Load available templates
  useEffect(() => {
    const loadTemplates = async () => {
      try {
        const response = await api.get('/api/templates/list');
        setTemplates(response.data.templates);
      } catch (error) {
        console.error('Failed to load templates:', error);
      }
    };
    loadTemplates();
  }, []);

  const handleLoadTemplate = async (templateName) => {
    setLoadingTemplate(templateName);
    try {
      await api.get(`/api/templates/load/${templateName}`);
      // Refresh visualization after loading
      await fetchVisualization();
      await fetchStats();
      console.log(`Loaded template: ${templateName}`);
    } catch (error) {
      console.error(`Failed to load template ${templateName}:`, error);
      alert(`Failed to load template: ${error.response?.data?.error || error.message}`);
    } finally {
      setLoadingTemplate(null);
    }
  };

  return (
    <div className="sidebar">
      <div className="sidebar-section">
        <h3>Graph Stats</h3>
        {stats && (
          <div className="stats">
            <div><strong>Nodes:</strong> {stats.count_nodes}</div>
            <div><strong>Edges:</strong> {stats.count_edges}</div>
            <div><strong>Connected:</strong> {stats.is_connected ? 'Yes' : 'No'}</div>
            <div><strong>Cyclic:</strong> {stats.is_cyclic ? 'Yes' : 'No'}</div>
          </div>
        )}
      </div>

      <div className="sidebar-section">
        <h3>Sample Templates</h3>
        <div className="templates-list">
          {templates.length > 0 ? (
            templates.map((template) => (
              <button
                key={template.name}
                className="template-btn"
                disabled={loadingTemplate === template.name}
                onClick={() => handleLoadTemplate(template.name)}
                title={template.description}
              >
                {loadingTemplate === template.name ? '⏳ Loading...' : '📊 ' + template.display_name}
                <span className="template-info">
                  {template.nodes} nodes, {template.edges} edges
                </span>
              </button>
            ))
          ) : (
            <p className="no-templates">No templates available</p>
          )}
        </div>
      </div>

      <div className="sidebar-section">
        <h3>Nodes ({nodes.length})</h3>
        <div className="nodes-list">
          {nodes.map(node => (
            <div
              key={node.id}
              className={`node-item ${selectedNode?.id === node.id ? 'selected' : ''}`}
              onClick={() => {
                setSelectedNodeForDialog(node);
                setNodeDialogOpen(true);
              }}
            >
              <div className="node-name">{node.id}</div>
              {node.data?.role && <div className="node-role">{node.data.role}</div>}
              <button 
                className="delete-btn"
                onClick={(e) => {
                  e.stopPropagation();
                  if (confirm(`Delete node ${node.id}?`)) {
                    deleteNode(node.id);
                  }
                }}
              >
                ✕
              </button>
            </div>
          ))}
        </div>
      </div>

      <div className="sidebar-section">
        <h3>Edges ({edges.length})</h3>
        <div className="edges-list">
          {edges.map((edge, idx) => (
            <div key={idx} className="edge-item">
              {(edge.source?.id || edge.source || edge.from) || '?'} → {(edge.target?.id || edge.target || edge.to) || '?'}
            </div>
          ))}
        </div>
      </div>

      <NodePropertyDialog
        node={selectedNodeForDialog}
        isOpen={nodeDialogOpen}
        onClose={() => {
          setNodeDialogOpen(false);
          setSelectedNodeForDialog(null);
        }}
      />

      {showChat && (
        <div className="sidebar-section chat-sidebar-section">
          <Chat />
        </div>
      )}
    </div>
  );
};
