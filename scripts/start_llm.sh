#!/bin/bash
echo "Starting LLM Service on http://localhost:3001"
cd ubuntu-deploy
node llm-service.js
