"""
ThreatAgent Memory System
=========================

This module provides persistent memory storage and retrieval for threat intelligence data.
It includes vector embeddings for semantic search and learning from historical data.
"""

import json
import sqlite3
import os
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
import numpy as np
from pathlib import Path

logger = logging.getLogger(__name__)

# For vector embeddings (using sentence-transformers)
try:
    from sentence_transformers import SentenceTransformer
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    print("⚠️  Install sentence-transformers for enhanced memory: pip install sentence-transformers")


class ThreatMemoryDB:
    """
    Persistent storage for threat intelligence data with vector search capabilities.
    """
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = os.path.join(os.path.dirname(__file__), "..", "..", "knowledge", "threat_memory.db")
        
        self.db_path = db_path
        self.knowledge_dir = os.path.dirname(db_path)
        
        # Create knowledge directory if it doesn't exist
        Path(self.knowledge_dir).mkdir(parents=True, exist_ok=True)
        
        # Initialize embedding model
        if EMBEDDINGS_AVAILABLE:
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        else:
            self.embedding_model = None
            
        self._init_database()
    
    def _init_database(self):
        """Initialize the SQLite database with required tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # IOC storage table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS iocs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ioc TEXT UNIQUE NOT NULL,
                    ioc_type TEXT NOT NULL,
                    risk_level TEXT NOT NULL,
                    category TEXT NOT NULL,
                    confidence REAL DEFAULT 0.0,
                    source TEXT,
                    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    times_seen INTEGER DEFAULT 1,
                    metadata TEXT,
                    embedding BLOB
                )
            ''')
            
            # TTP mappings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ttp_mappings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ioc_id INTEGER,
                    ttp_id TEXT NOT NULL,
                    ttp_name TEXT,
                    ttp_description TEXT,
                    confidence REAL DEFAULT 0.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (ioc_id) REFERENCES iocs (id)
                )
            ''')
            
            # Analysis history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analysis_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    analysis_type TEXT NOT NULL,
                    input_data TEXT,
                    output_data TEXT,
                    confidence REAL DEFAULT 0.0,
                    processing_time REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    embedding BLOB
                )
            ''')
            
            # Knowledge patterns table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS knowledge_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern_type TEXT NOT NULL,
                    pattern_text TEXT NOT NULL,
                    pattern_rules TEXT,
                    effectiveness_score REAL DEFAULT 0.0,
                    usage_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
    
    def _get_embedding(self, text: str) -> Optional[bytes]:
        """Generate embedding for text."""
        if not self.embedding_model or not text:
            return None
        
        try:
            embedding = self.embedding_model.encode([text])[0]
            return embedding.tobytes()
        except Exception as e:
            print(f"Warning: Could not generate embedding: {e}")
            return None
    
    def _get_connection(self):
        """Get database connection context manager."""
        return sqlite3.connect(self.db_path)
    
    def store_ioc(self, ioc: str, ioc_type: str, risk_level: str, 
                  category: str, confidence: float = 0.0, 
                  source: str = None, metadata: Dict = None) -> int:
        """Store or update an IOC in the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Generate embedding
            embedding = self._get_embedding(f"{ioc} {category} {risk_level}")
            
            # Check if IOC already exists
            cursor.execute('SELECT id, times_seen FROM iocs WHERE ioc = ?', (ioc,))
            existing = cursor.fetchone()
            
            if existing:
                # Update existing IOC
                ioc_id, times_seen = existing
                cursor.execute('''
                    UPDATE iocs SET 
                        risk_level = ?, category = ?, confidence = ?, 
                        last_seen = CURRENT_TIMESTAMP, times_seen = ?,
                        metadata = ?, embedding = ?
                    WHERE id = ?
                ''', (risk_level, category, confidence, times_seen + 1, 
                     json.dumps(metadata or {}), embedding, ioc_id))
                return ioc_id
            else:
                # Insert new IOC
                cursor.execute('''
                    INSERT INTO iocs (ioc, ioc_type, risk_level, category, 
                                    confidence, source, metadata, embedding)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (ioc, ioc_type, risk_level, category, confidence, 
                     source, json.dumps(metadata or {}), embedding))
                return cursor.lastrowid
    
    def store_ttp_mapping(self, ioc_id: int, ttp_id: str, ttp_name: str = None, 
                         ttp_description: str = None, confidence: float = 0.0):
        """Store TTP mapping for an IOC."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO ttp_mappings (ioc_id, ttp_id, ttp_name, ttp_description, confidence)
                VALUES (?, ?, ?, ?, ?)
            ''', (ioc_id, ttp_id, ttp_name, ttp_description, confidence))
            conn.commit()
    
    def store_analysis(self, session_id: str, analysis_type: str, 
                      input_data: Any, output_data: Any, 
                      confidence: float = 0.0, processing_time: float = 0.0):
        """Store analysis history."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            input_text = json.dumps(input_data) if not isinstance(input_data, str) else input_data
            output_text = json.dumps(output_data) if not isinstance(output_data, str) else output_data
            
            embedding = self._get_embedding(f"{analysis_type} {input_text}")
            
            cursor.execute('''
                INSERT INTO analysis_history (session_id, analysis_type, input_data, 
                                            output_data, confidence, processing_time, embedding)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (session_id, analysis_type, input_text, output_text, 
                 confidence, processing_time, embedding))
            conn.commit()
    
    def search_similar_iocs(self, query: str, limit: int = 5) -> List[Dict]:
        """Search for similar IOCs using vector similarity."""
        if not self.embedding_model:
            return self.search_iocs_text(query, limit)
        
        query_embedding = self.embedding_model.encode([query])[0]
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, ioc, ioc_type, risk_level, category, confidence, 
                       times_seen, first_seen, last_seen, metadata, embedding
                FROM iocs WHERE embedding IS NOT NULL
            ''')
            
            results = []
            for row in cursor.fetchall():
                if row[10]:  # embedding exists
                    stored_embedding = np.frombuffer(row[10], dtype=np.float32)
                    similarity = np.dot(query_embedding, stored_embedding) / (
                        np.linalg.norm(query_embedding) * np.linalg.norm(stored_embedding)
                    )
                    
                    results.append({
                        'id': row[0],
                        'ioc': row[1],
                        'ioc_type': row[2],
                        'risk_level': row[3],
                        'category': row[4],
                        'confidence': row[5],
                        'times_seen': row[6],
                        'first_seen': row[7],
                        'last_seen': row[8],
                        'metadata': json.loads(row[9] or '{}'),
                        'similarity': float(similarity)
                    })
            
            # Sort by similarity and return top results
            results.sort(key=lambda x: x['similarity'], reverse=True)
            return results[:limit]
    
    def search_iocs_text(self, query: str, limit: int = 5) -> List[Dict]:
        """Fallback text search for IOCs."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, ioc, ioc_type, risk_level, category, confidence, 
                       times_seen, first_seen, last_seen, metadata
                FROM iocs 
                WHERE ioc LIKE ? OR category LIKE ? OR risk_level LIKE ?
                ORDER BY times_seen DESC, confidence DESC
                LIMIT ?
            ''', (f'%{query}%', f'%{query}%', f'%{query}%', limit))
            
            return [{
                'id': row[0],
                'ioc': row[1],
                'ioc_type': row[2],
                'risk_level': row[3],
                'category': row[4],
                'confidence': row[5],
                'times_seen': row[6],
                'first_seen': row[7],
                'last_seen': row[8],
                'metadata': json.loads(row[9] or '{}'),
                'similarity': 0.5  # Default similarity for text search
            } for row in cursor.fetchall()]
    
    def get_analysis_history(self, analysis_type: str = None, limit: int = 10) -> List[Dict]:
        """Retrieve analysis history."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if analysis_type:
                cursor.execute('''
                    SELECT session_id, analysis_type, input_data, output_data, 
                           confidence, processing_time, created_at
                    FROM analysis_history 
                    WHERE analysis_type = ?
                    ORDER BY created_at DESC LIMIT ?
                ''', (analysis_type, limit))
            else:
                cursor.execute('''
                    SELECT session_id, analysis_type, input_data, output_data, 
                           confidence, processing_time, created_at
                    FROM analysis_history 
                    ORDER BY created_at DESC LIMIT ?
                ''', (limit,))
            
            return [{
                'session_id': row[0],
                'analysis_type': row[1],
                'input_data': row[2],
                'output_data': row[3],
                'confidence': row[4],
                'processing_time': row[5],
                'created_at': row[6]
            } for row in cursor.fetchall()]
    
    def get_statistics(self) -> Dict:
        """Get database statistics."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # IOC statistics
            cursor.execute('SELECT COUNT(*) FROM iocs')
            total_iocs = cursor.fetchone()[0]
            cursor.execute('SELECT risk_level, COUNT(*) FROM iocs GROUP BY risk_level')
            risk_distribution = dict(cursor.fetchall())
            cursor.execute('SELECT category, COUNT(*) FROM iocs GROUP BY category')
            category_distribution = dict(cursor.fetchall())
            # Analysis statistics
            cursor.execute('SELECT COUNT(*) FROM analysis_history')
            total_analyses = cursor.fetchone()[0]
            cursor.execute('SELECT analysis_type, COUNT(*) FROM analysis_history GROUP BY analysis_type')
            analysis_distribution = dict(cursor.fetchall())
            # Always include 'categories' for compatibility
            return {
                'total_iocs': total_iocs,
                'risk_distribution': risk_distribution,
                'categories': list(category_distribution.keys()),
                'category_distribution': category_distribution,
                'total_analyses': total_analyses,
                'analysis_distribution': analysis_distribution
            }
        
    def get_historical_context(self, agent_name: str = None) -> Dict[str, Any]:
        """Get historical context for an agent or general context."""
        context = {
            "iocs": [],
            "ttp_mappings": [],
            "analysis_history": []
        }
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get recent IOCs
                cursor.execute('''
                    SELECT ioc, ioc_type, risk_level, category, confidence, source
                    FROM iocs ORDER BY last_seen DESC LIMIT 10
                ''')
                context["iocs"] = [
                    {
                        "ioc": row[0],
                        "type": row[1], 
                        "risk_level": row[2],
                        "category": row[3],
                        "confidence": row[4],
                        "source": row[5]
                    }
                    for row in cursor.fetchall()
                ]
                
                # Get TTP mappings
                cursor.execute('''
                    SELECT ttp_id, ttp_name, confidence
                    FROM ttp_mappings ORDER BY created_at DESC LIMIT 10
                ''')
                context["ttp_mappings"] = [
                    {
                        "ttp_id": row[0],
                        "ttp_name": row[1],
                        "confidence": row[2]
                    }
                    for row in cursor.fetchall()
                ]
                
                # Get analysis history (filter by agent if specified)
                if agent_name:
                    cursor.execute('''
                        SELECT analysis_type, confidence, created_at
                        FROM analysis_history 
                        WHERE session_id LIKE ? 
                        ORDER BY created_at DESC LIMIT 10
                    ''', (f"%{agent_name}%",))
                else:
                    cursor.execute('''
                        SELECT analysis_type, confidence, created_at
                        FROM analysis_history 
                        ORDER BY created_at DESC LIMIT 10
                    ''')
                
                context["analysis_history"] = [
                    {
                        "analysis_type": row[0],
                        "confidence": row[1],
                        "created_at": row[2]
                    }
                    for row in cursor.fetchall()
                ]
                
        except Exception as e:
            logger.error(f"❌ Error getting historical context: {e}")
        
        return context


# Global memory instance
_memory_instance = None

def get_memory() -> ThreatMemoryDB:
    """Get the global memory instance."""
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = ThreatMemoryDB()
    return _memory_instance
