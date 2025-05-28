# AI Tool Usage Log

## Overview
This document provides a detailed log of AI tool usage during the development of the multi-agent finance assistant. It includes information about prompts, code generation steps, and model parameters used throughout the project.

## Development Process

### Project Structure and Planning
- **AI Tool**: ChatGPT/GPT-4
- **Purpose**: Initial project planning and architecture design
- **Prompt**: "Design a multi-agent finance assistant that delivers spoken market briefs via a Streamlit app, following the requirements in the assignment."
- **Output**: Project structure, component breakdown, and implementation strategy

### Agent Implementation
- **AI Tool**: GPT-4
- **Purpose**: Implementation of specialized agents using CrewAI
- **Prompts**:
  - "Implement an API agent using CrewAI to fetch financial data from Alpha Vantage and Yahoo Finance"
  - "Create a scraping agent using CrewAI to extract financial news and filings"
  - "Develop a retriever agent using CrewAI and FAISS for vector storage and retrieval"
  - "Implement an analysis agent using CrewAI for financial data analysis"
  - "Create a language agent using CrewAI and LangChain for narrative synthesis"
  - "Implement a voice agent using CrewAI, Whisper, and gTTS/pyttsx3"
- **Model Parameters**: Temperature=0.7, Top-p=0.95

### Data Ingestion Pipeline
- **AI Tool**: GPT-4
- **Purpose**: Implementation of data ingestion modules
- **Prompts**:
  - "Create a financial data API module to fetch data from Alpha Vantage and Yahoo Finance"
  - "Implement a web scraping module to extract financial news and sentiment data"
- **Model Parameters**: Temperature=0.5, Top-p=0.9

### Orchestration and API Development
- **AI Tool**: GPT-4
- **Purpose**: Implementation of FastAPI microservices for agent orchestration
- **Prompt**: "Develop a FastAPI orchestrator to coordinate all agents and expose endpoints for the Streamlit frontend"
- **Model Parameters**: Temperature=0.6, Top-p=0.9

### Frontend Development
- **AI Tool**: GPT-4
- **Purpose**: Implementation of Streamlit UI
- **Prompt**: "Create a Streamlit app with tabs for market brief and query functionality, including voice input/output capabilities"
- **Model Parameters**: Temperature=0.6, Top-p=0.9

## Model Selection and Parameters

### LLM Models
- **OpenAI GPT-3.5-Turbo**
  - Used for: Language agent narrative synthesis
  - Parameters: Temperature=0.3, Model="gpt-3.5-turbo"
  - Rationale: Good balance of quality and cost for generating financial narratives

### Embedding Models
- **OpenAI Embeddings**
  - Used for: Vector store indexing in the retriever agent
  - Rationale: High-quality embeddings for financial text, good integration with FAISS

### Voice Models
- **Whisper**
  - Used for: Speech-to-text transcription
  - Model Size: "base" (configurable via environment variable)
  - Rationale: Open-source, high-quality transcription with reasonable resource requirements

- **gTTS/pyttsx3**
  - Used for: Text-to-speech synthesis
  - Configuration: Configurable via environment variable
  - Rationale: gTTS provides high-quality speech but requires internet; pyttsx3 works offline

## Challenges and Solutions

### Challenge 1: International Stock Symbol Handling
- **Problem**: Alpha Vantage had limitations with international stock symbols
- **Solution**: Implemented fallback to Yahoo Finance for international symbols
- **AI Assistance**: GPT-4 suggested the fallback mechanism and provided implementation

### Challenge 2: Web Scraping Reliability
- **Problem**: Web scraping selectors can break when websites change
- **Solution**: Implemented robust error handling and multiple source fallbacks
- **AI Assistance**: GPT-4 provided patterns for resilient scraping with proper error handling

### Challenge 3: Voice Processing Integration
- **Problem**: Integrating Whisper with streaming audio input
- **Solution**: Used temporary file approach with PyAudio for recording
- **AI Assistance**: GPT-4 provided implementation for audio recording and processing

## Conclusion
AI tools were instrumental in rapidly developing this multi-agent finance assistant. GPT-4 was primarily used for code generation, architecture design, and problem-solving. The implementation leverages multiple AI models (OpenAI GPT-3.5-Turbo, Whisper, embeddings) working together to provide a comprehensive financial assistant with voice capabilities.