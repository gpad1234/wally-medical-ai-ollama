import axios from 'axios';

const ONTOLOGY_API_URL = 'http://127.0.0.1:5002';

const ontologyApi = axios.create({
  baseURL: ONTOLOGY_API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
ontologyApi.interceptors.request.use(
  (config) => {
    console.log('🟣 Ontology API Request:', config.method.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('❌ Ontology API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for logging and error handling
ontologyApi.interceptors.response.use(
  (response) => {
    console.log('✅ Ontology API Response:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('❌ Ontology API Error:', error.message, error.config?.url);
    if (error.code === 'ECONNREFUSED') {
      console.error('⚠️  Cannot connect to Ontology API. Is Flask running on port 5002?');
    }
    return Promise.reject(error);
  }
);

// ============================================================================
// Classes
// ============================================================================

export const getAllClasses = () => 
  ontologyApi.get('/api/ontology/classes');

export const getClass = (classId) => 
  ontologyApi.get(`/api/ontology/classes/${classId}`);

export const getClassFull = (classId) => 
  ontologyApi.get(`/api/ontology/classes/${classId}/full`);

export const createClass = (classData) => 
  ontologyApi.post('/api/ontology/classes', classData);

export const deleteClass = (classId, force = false) => 
  ontologyApi.delete(`/api/ontology/classes/${classId}`, { params: { force } });

export const getSubclasses = (classId, directOnly = false) => 
  ontologyApi.get(`/api/ontology/classes/${classId}/subclasses`, { params: { direct: directOnly } });

export const getSuperclasses = (classId, directOnly = false) => 
  ontologyApi.get(`/api/ontology/classes/${classId}/superclasses`, { params: { direct: directOnly } });

// ============================================================================
// Properties
// ============================================================================

export const getAllProperties = () => 
  ontologyApi.get('/api/ontology/properties');

export const getProperty = (propertyId) => 
  ontologyApi.get(`/api/ontology/properties/${propertyId}`);

export const createProperty = (propertyData) => 
  ontologyApi.post('/api/ontology/properties', propertyData);

// ============================================================================
// Instances
// ============================================================================

export const createInstance = (instanceData) => 
  ontologyApi.post('/api/ontology/instances', instanceData);

export const getInstance = (instanceId) => 
  ontologyApi.get(`/api/ontology/instances/${instanceId}`);

export const getClassInstances = (classId, directOnly = true) => 
  ontologyApi.get(`/api/ontology/classes/${classId}/instances`, { params: { direct: directOnly } });

// ============================================================================
// Hierarchy & Reasoning
// ============================================================================

export const getHierarchy = (rootId = 'owl:Thing') => 
  ontologyApi.get('/api/ontology/hierarchy', { params: { root: rootId } });

export const checkConsistency = () => 
  ontologyApi.get('/api/ontology/reasoning/consistency');

export const getStatistics = () => 
  ontologyApi.get('/api/ontology/statistics');

export const validateOntology = () =>
  ontologyApi.get('/api/ontology/validate');

// ============================================================================
// Import/Export
// ============================================================================

export const exportOntology = (format = 'xml') =>
  ontologyApi.get('/api/ontology/export', {
    params: { format },
    responseType: 'text'
  });

export const importOntology = (file) => {
  const formData = new FormData();
  formData.append('file', file);

  return ontologyApi.post('/api/ontology/import', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export const importOntologyFromText = (content, format = 'xml', clearExisting = false) =>
  ontologyApi.post('/api/ontology/import',
    { content, format },
    { params: { clear: clearExisting } }
  );

export default ontologyApi;
