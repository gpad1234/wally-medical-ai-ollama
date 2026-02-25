
import React, { useState, useRef, useEffect } from 'react';
import { FaSearch, FaMicrophone, FaTimesCircle, FaHistory, FaLightbulb, FaSpinner, FaNode, FaProjectDiagram, FaUserCircle, FaRobot } from 'react-icons/fa';
import api from '../../services/api';
import './NLP.css';

const HINTS = [
  "How many nodes and edges are there?",
  "Show me the full graph.",
  "List all node IDs.",
  "List all edges.",
  "Who are Alice's neighbors?",
  "Find the shortest path from Alice to Frank."
];

const NLP = () => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);
  // Chat log: { sender: 'user'|'bot', text: string, result?: object, error?: string }
  const [chat, setChat] = useState([]);
  const chatEndRef = useRef(null);

  const handleSearch = async (e, q) => {
    e && e.preventDefault();
    const searchQuery = q || query;
    if (!searchQuery) return;
    setLoading(true);
    setError(null);
    setHistory((prev) => [searchQuery, ...prev.filter(h => h !== searchQuery)].slice(0, 8));
    setChat(prev => ([...prev, { sender: 'user', text: searchQuery }]));
    setQuery('');
    try {
      const response = await api.post('/api/nlp_query', { query: searchQuery });
      setChat(prev => ([...prev, { sender: 'bot', text: '', result: response.data }]));
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'Failed to search.';
      const isDisabled = err.response?.data?.feature_disabled;
      setChat(prev => ([...prev, { 
        sender: 'bot', 
        text: '', 
        error: isDisabled 
          ? '⚠️ NLP feature is not configured. Set OPENAI_API_KEY or ANTHROPIC_API_KEY to enable.' 
          : errorMsg 
      }]));
    } finally {
      setLoading(false);
    }
  };

  // Scroll to bottom on new chat
  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [chat, loading]);

  return (
    <div className="nlp-tab">
      <h2><FaProjectDiagram style={{marginRight: '8px'}}/>Search & NLP</h2>
      <div className="nlp-card nlp-input-card">
        <form className="nlp-form" onSubmit={handleSearch}>
          <div className="nlp-input-row">
            <FaMicrophone className="nlp-mic-icon" title="Voice input coming soon" />
            <textarea
              value={query}
              onChange={e => setQuery(e.target.value)}
              placeholder="Ask a question or type a graph search..."
              rows={2}
              className="nlp-input"
              disabled={loading}
              onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { handleSearch(e); } }}
            />
            {query && (
              <FaTimesCircle className="nlp-clear-btn" title="Clear" onClick={() => setQuery('')} />
            )}
            <button type="submit" className="nlp-search-btn" disabled={loading || !query} title="Send">
              {loading ? <FaSpinner className="nlp-spinner spin" /> : <FaSearch />}
            </button>
          </div>
        </form>
        <div className="nlp-hints">
          <FaLightbulb style={{marginRight: '4px'}}/>
          <b>Hints:</b>
          {HINTS.map((hint, i) => (
            <span key={i} className="nlp-hint" onClick={() => { setQuery(hint); handleSearch(null, hint); }}>{hint}</span>
          ))}
        </div>
      </div>
      <div className="nlp-chat-log">
        {chat.length === 0 && (
          <div className="nlp-chat-empty">Start a conversation or try a hint!</div>
        )}
        {chat.map((msg, idx) => (
          <div key={idx} className={`nlp-chat-bubble ${msg.sender === 'user' ? 'user' : 'bot'}`}
            style={{ animationDelay: `${idx * 60}ms` }}>
            <div className="nlp-chat-avatar">
              {msg.sender === 'user' ? <FaUserCircle /> : <FaRobot />}
            </div>
            <div className="nlp-chat-content">
              {msg.text && <span>{msg.text}</span>}
              {msg.result && (
                <div>
                  {msg.result.explanation && <div className="nlp-explanation">{msg.result.explanation}</div>}
                  {msg.result.action && <div className="nlp-action"><b>Action:</b> {msg.result.action}</div>}
                  {msg.result.nodes && (
                    <div className="nlp-nodes"><FaNode style={{marginRight: '4px'}}/><b>Nodes:</b> {Array.isArray(msg.result.nodes) ? msg.result.nodes.map((n, i) => <span key={i} className="nlp-node-badge">{n}</span>) : msg.result.nodes}</div>
                  )}
                  {msg.result.edges && (
                    <div className="nlp-edges">
                      <FaProjectDiagram style={{marginRight: '4px'}}/><b>Edges:</b>
                      <pre>{Array.isArray(msg.result.edges) ? JSON.stringify(msg.result.edges, null, 2) : msg.result.edges}</pre>
                    </div>
                  )}
                  {/* Show shortest path results if present */}
                  {msg.result.path && (
                    <div className="nlp-path">
                      <b>Shortest Path:</b> {Array.isArray(msg.result.path) ? msg.result.path.join(' → ') : msg.result.path}
                    </div>
                  )}
                  {msg.result.cost !== undefined && (
                    <div className="nlp-cost">
                      <b>Path Cost:</b> {msg.result.cost}
                    </div>
                  )}
                  {msg.result.algorithm && (
                    <div className="nlp-algorithm">
                      <b>Algorithm:</b> {msg.result.algorithm}
                    </div>
                  )}
                </div>
              )}
              {msg.error && <div className="nlp-card error">{msg.error}</div>}
            </div>
          </div>
        ))}
        {loading && (
          <div className="nlp-chat-bubble bot">
            <div className="nlp-chat-avatar"><FaRobot /></div>
            <div className="nlp-chat-content"><FaSpinner className="nlp-spinner spin" /> Thinking...</div>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>
      {history.length > 0 && (
        <div className="nlp-card nlp-history">
          <FaHistory style={{marginRight: '4px'}}/>
          <b>Recent queries:</b>
          <button className="nlp-clear-history" onClick={() => setHistory([])} title="Clear history"><FaTimesCircle /></button>
          <div className="nlp-history-list">
            {history.map((h, i) => (
              <span key={i} className="nlp-history-item" onClick={() => { setQuery(h); handleSearch(null, h); }}>{h}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default NLP;
