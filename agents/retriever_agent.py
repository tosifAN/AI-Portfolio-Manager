import os
import numpy as np
from typing import List, Dict, Any, Optional
from crewai import Agent, Task
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

class RetrieverAgent:
    """Agent for indexing and retrieving information from a vector store."""
    
    def __init__(self, vector_store_path: str = None, openai_api_key: str = None):
        """Initialize the retriever agent.
        
        Args:
            vector_store_path: Path to store the FAISS index
            openai_api_key: OpenAI API key for embeddings
        """
        self.vector_store_path = vector_store_path or os.getenv('VECTOR_STORE_PATH', './vector_store')
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.openai_api_key)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        
        # Create vector store directory if it doesn't exist
        os.makedirs(self.vector_store_path, exist_ok=True)
        
    def create_agent(self) -> Agent:
        """Create a CrewAI agent for retrieval operations."""
        return Agent(
            role="Financial Information Retrieval Specialist",
            goal="Efficiently index and retrieve relevant financial information",
            backstory="""You are an expert in information retrieval systems with a 
            specialization in financial data. Your expertise lies in organizing, indexing, 
            and retrieving the most relevant information from large datasets to answer 
            specific financial queries.""",
            verbose=True,
            allow_delegation=False
        )
    
    def index_documents(self, documents: List[Dict[str, str]], namespace: str = 'default') -> bool:
        """Index documents in the vector store.
        
        Args:
            documents: List of documents to index (each with 'content' and 'metadata' keys)
            namespace: Namespace for the documents
            
        Returns:
            Boolean indicating success
        """
        try:
            # Convert to Document objects
            doc_objects = [Document(page_content=doc['content'], metadata=doc['metadata']) for doc in documents]
            
            # Split documents into chunks
            splits = self.text_splitter.split_documents(doc_objects)
            
            # Create or update the vector store
            vector_store_path = os.path.join(self.vector_store_path, namespace)
            
            # Check if the vector store already exists
            if os.path.exists(vector_store_path):
                # Load existing vector store and add documents
                vector_store = FAISS.load_local(vector_store_path, self.embeddings)
                vector_store.add_documents(splits)
            else:
                # Create new vector store
                vector_store = FAISS.from_documents(splits, self.embeddings)
            
            # Save the vector store
            vector_store.save_local(vector_store_path)
            
            return True
        except Exception as e:
            print(f"Error indexing documents: {e}")
            return False
    
    def retrieve(self, query: str, namespace: str = 'default', k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve documents from the vector store.
        
        Args:
            query: Query string
            namespace: Namespace to search in
            k: Number of documents to retrieve
            
        Returns:
            List of retrieved documents with content, metadata, and similarity score
        """
        try:
            vector_store_path = os.path.join(self.vector_store_path, namespace)
            
            # Check if the vector store exists
            if not os.path.exists(vector_store_path):
                print(f"Vector store not found at {vector_store_path}")
                return []
            
            # Load the vector store
            vector_store = FAISS.load_local(vector_store_path, self.embeddings)
            
            # Retrieve documents
            docs_with_scores = vector_store.similarity_search_with_score(query, k=k)
            
            # Format results
            results = []
            for doc, score in docs_with_scores:
                results.append({
                    'content': doc.page_content,
                    'metadata': doc.metadata,
                    'score': float(score),  # Convert numpy float to Python float
                    'confidence': self._score_to_confidence(score)
                })
            
            return results
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            return []
    
    def _score_to_confidence(self, score: float) -> float:
        """Convert similarity score to confidence percentage.
        
        Args:
            score: Similarity score from FAISS
            
        Returns:
            Confidence percentage (0-100)
        """
        # FAISS returns L2 distance, so smaller is better
        # Convert to a confidence score where higher is better
        # This is a simple conversion and might need tuning
        confidence = max(0, min(100, 100 * (1 - score / 10)))
        return confidence
    
    def index_financial_data(self, data: List[Dict[str, Any]], data_type: str) -> bool:
        """Index financial data in the vector store.
        
        Args:
            data: List of financial data items
            data_type: Type of data (e.g., 'news', 'earnings', 'stock_data')
            
        Returns:
            Boolean indicating success
        """
        documents = []
        
        for item in data:
            if data_type == 'news':
                # Format news articles
                content = f"Title: {item.get('title', '')}\n\nSummary: {item.get('summary', '')}\n\nSource: {item.get('source', '')}"
                metadata = {
                    'type': 'news',
                    'source': item.get('source', ''),
                    'link': item.get('link', ''),
                    'title': item.get('title', '')
                }
            elif data_type == 'earnings':
                # Format earnings data
                content = f"Company: {item.get('name', item.get('symbol', ''))}\n\nSymbol: {item.get('symbol', '')}\n\nEPS Estimate: {item.get('eps_estimate', '')}\n\nReported EPS: {item.get('reported_eps', '')}\n\nSurprise: {item.get('surprise_pct', '')}%"
                metadata = {
                    'type': 'earnings',
                    'symbol': item.get('symbol', ''),
                    'date': item.get('date', ''),
                    'surprise_pct': item.get('surprise_pct', None)
                }
            elif data_type == 'stock_data':
                # Format stock data
                content = f"Company: {item.get('name', item.get('symbol', ''))}\n\nSymbol: {item.get('symbol', '')}\n\nPrice: {item.get('price', '')}\n\nChange: {item.get('change_pct', '')}%\n\nVolume: {item.get('volume', '')}\n\nMarket Cap: {item.get('market_cap', '')}"
                metadata = {
                    'type': 'stock_data',
                    'symbol': item.get('symbol', ''),
                    'country': item.get('country', ''),
                    'change_pct': item.get('change_pct', None)
                }
            elif data_type == 'sentiment':
                # Format sentiment data
                content = f"Overall Sentiment: {item.get('overall_sentiment', '')}\n\nSentiment Score: {item.get('sentiment_score', '')}\n\nKey Indicators: {', '.join([ind.get('headline', '') for ind in item.get('key_indicators', [])])}"
                metadata = {
                    'type': 'sentiment',
                    'sentiment': item.get('overall_sentiment', ''),
                    'score': item.get('sentiment_score', None)
                }
            else:
                # Generic format for other data types
                content = str(item)
                metadata = {'type': data_type}
            
            documents.append({
                'content': content,
                'metadata': metadata
            })
        
        return self.index_documents(documents, namespace=data_type)
    
    def retrieve_asia_tech_info(self, query: str, confidence_threshold: float = 70.0) -> Dict[str, Any]:
        """Retrieve information about Asia tech stocks.
        
        Args:
            query: Query string
            confidence_threshold: Minimum confidence threshold
            
        Returns:
            Dictionary with retrieved information and confidence scores
        """
        # Namespaces to search in
        namespaces = ['news', 'earnings', 'stock_data', 'sentiment']
        
        all_results = []
        confidence_levels = []
        
        for namespace in namespaces:
            results = self.retrieve(query, namespace=namespace, k=3)
            all_results.extend(results)
            
            # Track confidence levels
            for result in results:
                confidence_levels.append(result['confidence'])
        
        # Sort by confidence
        all_results.sort(key=lambda x: x['confidence'], reverse=True)
        
        # Calculate average confidence
        avg_confidence = sum(confidence_levels) / len(confidence_levels) if confidence_levels else 0
        
        # Filter by confidence threshold
        filtered_results = [r for r in all_results if r['confidence'] >= confidence_threshold]
        
        return {
            'results': filtered_results,
            'avg_confidence': avg_confidence,
            'below_threshold': avg_confidence < confidence_threshold,
            'top_result': filtered_results[0] if filtered_results else None
        }

# Example tasks for the retriever agent
def create_retriever_tasks(agent: Agent) -> List[Task]:
    """Create tasks for the retriever agent."""
    return [
        Task(
            description="Index recent financial news, earnings reports, and stock data for Asia tech companies",
            agent=agent,
            expected_output="Confirmation that all data has been successfully indexed in the vector store"
        ),
        Task(
            description="Retrieve relevant information about risk exposure in Asia tech stocks",
            agent=agent,
            expected_output="A collection of the most relevant documents about current risk factors and exposure levels in Asia tech stocks"
        ),
        Task(
            description="Find information about recent earnings surprises in the Asia tech sector",
            agent=agent,
            expected_output="Detailed information about companies that have reported earnings significantly different from analyst expectations"
        )
    ]