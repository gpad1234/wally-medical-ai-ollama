import React, { useState, useEffect } from 'react';
import { useGraphStore } from '../../store/graphStore';
import './NodePropertyDialog.css';

export const NodePropertyDialog = ({ node, isOpen, onClose }) => {
  const [formData, setFormData] = useState({
    id: '',
    role: '',
    team: '',
    name: '',
  });
  const [errors, setErrors] = useState({});
  const { updateNode } = useGraphStore();

  // Initialize form when node changes
  useEffect(() => {
    if (node) {
      setFormData({
        id: node.id || '',
        role: node.data?.role || '',
        team: node.data?.team || '',
        name: node.data?.name || node.id || '',
      });
      setErrors({});
    }
  }, [node, isOpen]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
    // Clear error for this field when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: '',
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    if (!formData.id.trim()) newErrors.id = 'Node ID is required';
    if (!formData.name.trim()) newErrors.name = 'Name is required';
    return newErrors;
  };

  const handleSave = async () => {
    const newErrors = validateForm();
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    try {
      await updateNode(formData.id, {
        role: formData.role,
        team: formData.team,
        name: formData.name,
      });
      onClose();
    } catch (error) {
      setErrors({ submit: error.message });
    }
  };

  if (!isOpen || !node) return null;

  return (
    <div className="dialog-overlay" onClick={onClose}>
      <div className="dialog-container" onClick={(e) => e.stopPropagation()}>
        <div className="dialog-header">
          <h2>Node Properties</h2>
          <button className="dialog-close" onClick={onClose}>×</button>
        </div>

        <div className="dialog-content">
          {errors.submit && (
            <div className="error-message">{errors.submit}</div>
          )}

          <div className="form-group">
            <label htmlFor="id">Node ID</label>
            <input
              id="id"
              type="text"
              name="id"
              value={formData.id}
              onChange={handleChange}
              placeholder="e.g., Alice"
              disabled
              className="input-disabled"
            />
            <small className="field-hint">Node ID cannot be changed</small>
          </div>

          <div className="form-group">
            <label htmlFor="name">Name</label>
            <input
              id="name"
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="Node display name"
              className={errors.name ? 'input-error' : ''}
            />
            {errors.name && <span className="error-text">{errors.name}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="role">Role</label>
            <input
              id="role"
              type="text"
              name="role"
              value={formData.role}
              onChange={handleChange}
              placeholder="e.g., manager, developer"
            />
          </div>

          <div className="form-group">
            <label htmlFor="team">Team</label>
            <input
              id="team"
              type="text"
              name="team"
              value={formData.team}
              onChange={handleChange}
              placeholder="e.g., engineering, design"
            />
          </div>
        </div>

        <div className="dialog-footer">
          <button className="btn-cancel" onClick={onClose}>Cancel</button>
          <button className="btn-save" onClick={handleSave}>Save Changes</button>
        </div>
      </div>
    </div>
  );
};
