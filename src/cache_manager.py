"""Advanced caching system for search results"""
import json
import hashlib
import time
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import sqlite3
from threading import Lock

logger = logging.getLogger(__name__)

@dataclass
class CacheEntry:
    """Cache entry data structure"""
    key: str
    value: str
    created_at: float
    ttl: int
    hit_count: int = 0
    
    def is_expired(self) -> bool:
        """Check if cache entry is expired"""
        if self.ttl <= 0:
            return False
        return time.time() - self.created_at > self.ttl
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class CacheManager:
    """SQLite-based cache with TTL support"""
    
    def __init__(self, db_path: str = "cache.db", ttl: int = 3600):
        self.db_path = Path(db_path)
        self.ttl = ttl
        self.lock = Lock()
        self._init_db()
    
    def _init_db(self):
        """Initialize cache database"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS cache (
                        id INTEGER PRIMARY KEY,
                        key TEXT UNIQUE NOT NULL,
                        value TEXT NOT NULL,
                        created_at REAL NOT NULL,
                        ttl INTEGER NOT NULL,
                        hit_count INTEGER DEFAULT 0,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_key ON cache(key)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_ttl ON cache(ttl)')
                conn.commit()
                logger.info("Cache database initialized")
        except Exception as e:
            logger.error(f"Cache initialization error: {str(e)}")
    
    def _get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("PRAGMA journal_mode = WAL")
        return conn
    
    def _hash_key(self, key: str) -> str:
        """Generate hash key for cache"""
        return hashlib.sha256(key.encode()).hexdigest()
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Store value in cache"""
        try:
            ttl = ttl or self.ttl
            json_value = json.dumps(value) if not isinstance(value, str) else value
            hash_key = self._hash_key(key)
            
            with self.lock:
                with self._get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT OR REPLACE INTO cache (key, value, created_at, ttl, hit_count)
                        VALUES (?, ?, ?, ?, 0)
                    ''', (hash_key, json_value, time.time(), ttl))
                    conn.commit()
            
            logger.debug(f"Cache SET: {key[:50]} (TTL: {ttl}s)")
            return True
        except Exception as e:
            logger.error(f"Cache SET error: {str(e)}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """Retrieve value from cache"""
        try:
            hash_key = self._hash_key(key)
            
            with self.lock:
                with self._get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        'SELECT value, created_at, ttl FROM cache WHERE key = ?',
                        (hash_key,)
                    )
                    result = cursor.fetchone()
            
            if not result:
                logger.debug(f"Cache MISS: {key[:50]}")
                return None
            
            value, created_at, ttl = result
            
            # Check expiration
            if ttl > 0 and time.time() - created_at > ttl:
                self.delete(key)
                logger.debug(f"Cache EXPIRED: {key[:50]}")
                return None
            
            # Update hit count
            with self.lock:
                with self._get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        'UPDATE cache SET hit_count = hit_count + 1 WHERE key = ?',
                        (hash_key,)
                    )
                    conn.commit()
            
            logger.debug(f"Cache HIT: {key[:50]}")
            
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        
        except Exception as e:
            logger.error(f"Cache GET error: {str(e)}")
            return None
    
    def delete(self, key: str) -> bool:
        """Delete cache entry"""
        try:
            hash_key = self._hash_key(key)
            
            with self.lock:
                with self._get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute('DELETE FROM cache WHERE key = ?', (hash_key,))
                    conn.commit()
            
            logger.debug(f"Cache DELETE: {key[:50]}")
            return True
        except Exception as e:
            logger.error(f"Cache DELETE error: {str(e)}")
            return False
    
    def clear(self) -> bool:
        """Clear all cache"""
        try:
            with self.lock:
                with self._get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute('DELETE FROM cache')
                    conn.commit()
            logger.info("Cache cleared")
            return True
        except Exception as e:
            logger.error(f"Cache CLEAR error: {str(e)}")
            return False
    
    def cleanup_expired(self) -> int:
        """Remove expired entries"""
        try:
            with self.lock:
                with self._get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        SELECT key, created_at, ttl FROM cache
                        WHERE ttl > 0 AND created_at + ttl < ?
                    ''', (time.time(),))
                    
                    expired_keys = cursor.fetchall()
                    
                    for key, _, _ in expired_keys:
                        cursor.execute('DELETE FROM cache WHERE key = ?', (key,))
                    
                    conn.commit()
            
            logger.info(f"Cleaned {len(expired_keys)} expired cache entries")
            return len(expired_keys)
        except Exception as e:
            logger.error(f"Cache cleanup error: {str(e)}")
            return 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        try:
            with self.lock:
                with self._get_connection() as conn:
                    cursor = conn.cursor()
                    
                    cursor.execute('SELECT COUNT(*) FROM cache')
                    total_entries = cursor.fetchone()[0]
                    
                    cursor.execute('SELECT SUM(hit_count) FROM cache')
                    total_hits = cursor.fetchone()[0] or 0
                    
                    cursor.execute('SELECT LENGTH(value) FROM cache')
                    sizes = cursor.fetchall()
                    total_size = sum(s[0] for s in sizes)
            
            return {
                'total_entries': total_entries,
                'total_hits': total_hits,
                'total_size_bytes': total_size,
                'avg_entry_size': total_size // total_entries if total_entries > 0 else 0
            }
        except Exception as e:
            logger.error(f"Cache stats error: {str(e)}")
            return {}

# Global cache instance
cache = CacheManager()
