import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { useGraphStore } from '../../store/graphStore';
import { NodePropertyDialog } from '../NodePropertyDialog/NodePropertyDialog';
import './Graph.css';

export const Graph = () => {
  const svgRef = useRef();
  const [nodeDialogOpen, setNodeDialogOpen] = useState(false);
  const [selectedNodeForDialog, setSelectedNodeForDialog] = useState(null);
  const { nodes, edges, selectedNode, setSelectedNode } = useGraphStore();

  useEffect(() => {
    if (!nodes || nodes.length === 0 || !svgRef.current) return;

    const width = svgRef.current.clientWidth;
    const height = svgRef.current.clientHeight;

    // Create simulation - use copies to avoid mutation
    const nodesCopy = nodes.map(d => ({ ...d }));
    const edgesCopy = edges.map(d => ({
      source: typeof d.source === 'string' ? d.source : d.source.id,
      target: typeof d.target === 'string' ? d.target : d.target.id,
      ...d
    }));

    const simulation = d3.forceSimulation(nodesCopy)
      .force('link', d3.forceLink(edgesCopy)
        .id(d => d.id)
        .distance(100))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2));

    // Clear previous content
    d3.select(svgRef.current).selectAll('*').remove();

    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height);

    // Draw links
    const link = svg.selectAll('.link')
      .data(edgesCopy)
      .enter()
      .append('line')
      .attr('class', 'link')
      .attr('stroke', '#999')
      .attr('stroke-width', 2)
      .attr('opacity', 0.6);

    // Draw edge weight labels
    const edgeLabel = svg.selectAll('.edge-label')
      .data(edgesCopy)
      .enter()
      .append('text')
      .attr('class', 'edge-label')
      .attr('text-anchor', 'middle')
      .attr('font-size', '11px')
      .attr('fill', '#666')
      .attr('pointer-events', 'none')
      .text(d => d.value || d.weight || '');

    // Draw nodes
    const node = svg.selectAll('.node')
      .data(nodesCopy)
      .enter()
      .append('circle')
      .attr('class', d => `node ${selectedNode?.id === d.id ? 'selected' : ''}`)
      .attr('r', 25)
      .attr('fill', d => selectedNode?.id === d.id ? '#ff6b6b' : '#4ecdc4')
      .attr('stroke', '#fff')
      .attr('stroke-width', 2)
      .on('click', (event, d) => {
        event.stopPropagation();
        setSelectedNode(d);
        setSelectedNodeForDialog(d);
        setNodeDialogOpen(true);
      })
      .call(drag(simulation));

    // Draw node labels
    const label = svg.selectAll('.label')
      .data(nodesCopy)
      .enter()
      .append('text')
      .attr('class', 'label')
      .attr('text-anchor', 'middle')
      .attr('dy', '.3em')
      .attr('font-size', '12px')
      .attr('pointer-events', 'none')
      .text(d => d.id);

    // Update positions on each tick
    simulation.on('tick', () => {
      link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);

      edgeLabel
        .attr('x', d => (d.source.x + d.target.x) / 2)
        .attr('y', d => (d.source.y + d.target.y) / 2);

      node
        .attr('cx', d => d.x)
        .attr('cy', d => d.y)
        .attr('fill', d => selectedNode?.id === d.id ? '#ff6b6b' : '#4ecdc4');

      label
        .attr('x', d => d.x)
        .attr('y', d => d.y);
    });

    // Drag behavior
    function drag(simulation) {
      function dragstarted(event) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        event.subject.fx = event.subject.x;
        event.subject.fy = event.subject.y;
      }

      function dragged(event) {
        event.subject.fx = event.x;
        event.subject.fy = event.y;
      }

      function dragended(event) {
        if (!event.active) simulation.alphaTarget(0);
        event.subject.fx = null;
        event.subject.fy = null;
      }

      return d3.drag()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended);
    }

    return () => simulation.stop();
  }, [nodes, edges, selectedNode, setSelectedNode]);

  return (
    <>
      <div className="graph-container">
        <svg ref={svgRef} className="graph-canvas"></svg>
      </div>
      <NodePropertyDialog
        node={selectedNodeForDialog}
        isOpen={nodeDialogOpen}
        onClose={() => {
          setNodeDialogOpen(false);
          setSelectedNodeForDialog(null);
        }}
      />
    </>
  );
};
