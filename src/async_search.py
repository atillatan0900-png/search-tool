"""Async search engine for improved performance"""
import asyncio
import aiohttp
import logging
import time
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class AsyncSearchResult:
    """Async search result"""
    platform: str
    links: List[str]
    success: bool
    error: Optional[str] = None
    duration: float = 0.0

class AsyncSearchEngine:
    """Async search engine using aiohttp"""
    
    def __init__(self, timeout: int = 10, max_concurrent: int = 10):
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.max_concurrent = max_concurrent
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def search_platform(
        self,
        platform_name: str,
        query: str,
        max_results: int = 10
    ) -> AsyncSearchResult:
        """Search single platform asynchronously"""
        start_time = time.time()
        
        try:
            if not self.session:
                return AsyncSearchResult(
                    platform=platform_name,
                    links=[],
                    success=False,
                    error="No session"
                )
            
            # This is a placeholder - replace with actual DDGS async call
            # For now, we'll simulate the call
            await asyncio.sleep(0.1)
            
            logger.debug(f"Searched platform: {platform_name}")
            
            return AsyncSearchResult(
                platform=platform_name,
                links=[],
                success=True,
                duration=time.time() - start_time
            )
        
        except asyncio.TimeoutError:
            return AsyncSearchResult(
                platform=platform_name,
                links=[],
                success=False,
                error="Timeout",
                duration=time.time() - start_time
            )
        except Exception as e:
            logger.error(f"Async search error ({platform_name}): {str(e)}")
            return AsyncSearchResult(
                platform=platform_name,
                links=[],
                success=False,
                error=str(e),
                duration=time.time() - start_time
            )
    
    async def search_multiple_platforms(
        self,
        platforms: Dict[str, str],
        query: str,
        max_results: int = 10
    ) -> Dict[str, AsyncSearchResult]:
        """Search multiple platforms concurrently"""
        
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        async def search_with_semaphore(name: str, search_query: str):
            async with semaphore:
                return await self.search_platform(name, search_query, max_results)
        
        tasks = [
            search_with_semaphore(platform_name, f"{search_query} {platform_query}")
            for platform_name, platform_query in platforms.items()
        ]
        
        results = await asyncio.gather(*tasks)
        
        return {result.platform: result for result in results}

class AsyncLinkChecker:
    """Async link checker for faster validation"""
    
    def __init__(self, timeout: int = 5, max_concurrent: int = 20):
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.max_concurrent = max_concurrent
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def check_link(self, url: str) -> Tuple[str, str, str]:
        """Check single link asynchronously"""
        try:
            if not self.session:
                return url, "error", "No session"
            
            async with self.session.head(url, allow_redirects=True) as response:
                status = "active" if response.status < 400 else "broken"
                size = response.headers.get('content-length', 'unknown')
                return url, status, size
        
        except asyncio.TimeoutError:
            return url, "timeout", "unknown"
        except aiohttp.ClientError as e:
            return url, "error", str(e)[:50]
        except Exception as e:
            logger.error(f"Link check error ({url[:50]}): {str(e)}")
            return url, "error", str(e)[:50]
    
    async def check_multiple_links(self, urls: List[str]) -> Dict[str, Tuple[str, str]]:
        """Check multiple links concurrently"""
        
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        async def check_with_semaphore(url: str):
            async with semaphore:
                return await self.check_link(url)
        
        tasks = [check_with_semaphore(url) for url in urls]
        results = await asyncio.gather(*tasks)
        
        return {
            url: (status, size)
            for url, status, size in results
        }

# Async helper functions
async def async_search(platforms: Dict[str, str], query: str) -> Dict[str, List[str]]:
    """Helper function for async search"""
    async with AsyncSearchEngine() as engine:
        results = await engine.search_multiple_platforms(platforms, query)
        return {
            platform: result.links
            for platform, result in results.items()
        }

async def async_check_links(urls: List[str]) -> Dict[str, Tuple[str, str]]:
    """Helper function for async link checking"""
    async with AsyncLinkChecker() as checker:
        return await checker.check_multiple_links(urls)

def run_async_search(platforms: Dict[str, str], query: str) -> Dict[str, List[str]]:
    """Run async search in sync context"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(async_search(platforms, query))

def run_async_link_check(urls: List[str]) -> Dict[str, Tuple[str, str]]:
    """Run async link checking in sync context"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(async_check_links(urls))
