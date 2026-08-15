"""
 ============================================================
  MODULE/PLUGIN NAME: FuzzySearch
  VERSION: 1.0.0
  MODULE CLASS: FuzzySearch
  DESCRIPTION:
       Intelligent search with fuzzy matching for TerminalX

  AUTHOR:  Sebastian Januchowski
  COMPANY: polsoft.ITS™ Dev
  EMAIL:   polsoft.its@mail.com
  GITHUB:  polsoft-IT
  STATUS:  stable

 ============================================================
  COMPATIBILITY
 ============================================================
  PYTHON: 3.10+
  OS: Windows / Linux / macOS / Android (TerminalOS Runtime)
  ARCH: x86_64 / ARM64
  TERMINALOS KERNEL: v1.0+
"""

from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass
from libs.clean_logger import CleanLogger, LogLevel


@dataclass
class SearchResult:
    """Search result"""
    item: Any
    score: float
    matched_indices: List[int]


class FuzzySearch:
    """Fuzzy search with intelligent matching"""
    
    def __init__(self, logger: Optional[CleanLogger] = None):
        """
        Initialize fuzzy search
        
        Args:
            logger: Logger instance
        """
        self.logger = logger or CleanLogger("FuzzySearch", LogLevel.INFO)
        self.indexed_items: Dict[str, Any] = {}
        
    def index_item(self, key: str, item: Any) -> None:
        """
        Index an item for search
        
        Args:
            key: Search key
            item: Item to index
        """
        self.indexed_items[key.lower()] = item
        
    def remove_item(self, key: str) -> bool:
        """
        Remove item from index
        
        Args:
            key: Search key
            
        Returns:
            True if removed
        """
        if key.lower() in self.indexed_items:
            del self.indexed_items[key.lower()]
            return True
        return False
        
    def search(self, query: str, threshold: float = 0.5, 
              max_results: int = 10) -> List[SearchResult]:
        """
        Search indexed items with fuzzy matching
        
        Args:
            query: Search query
            threshold: Minimum score threshold
            max_results: Maximum results to return
            
        Returns:
            List of search results
        """
        results = []
        query_lower = query.lower()
        
        for key, item in self.indexed_items.items():
            score, matched_indices = self._calculate_match(query_lower, key)
            
            if score >= threshold:
                results.append(SearchResult(
                    item=item,
                    score=score,
                    matched_indices=matched_indices
                ))
                
        # Sort by score (descending)
        results.sort(key=lambda x: x.score, reverse=True)
        
        return results[:max_results]
        
    def search_list(self, items: List[str], query: str, threshold: float = 0.5,
                   max_results: int = 10) -> List[SearchResult]:
        """
        Search a list of strings
        
        Args:
            items: List of strings to search
            query: Search query
            threshold: Minimum score threshold
            max_results: Maximum results to return
            
        Returns:
            List of search results
        """
        results = []
        query_lower = query.lower()
        
        for item in items:
            score, matched_indices = self._calculate_match(query_lower, item.lower())
            
            if score >= threshold:
                results.append(SearchResult(
                    item=item,
                    score=score,
                    matched_indices=matched_indices
                ))
                
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:max_results]
        
    def _calculate_match(self, query: str, target: str) -> Tuple[float, List[int]]:
        """
        Calculate match score and indices
        
        Args:
            query: Query string
            target: Target string
            
        Returns:
            Tuple of (score, matched_indices)
        """
        if not query:
            return 0.0, []
            
        if query == target:
            return 1.0, list(range(len(query)))
            
        # Check for exact prefix match
        if target.startswith(query):
            return 0.9, list(range(len(query)))
            
        # Check for exact substring match
        if query in target:
            start = target.index(query)
            return 0.8, list(range(start, start + len(query)))
            
        # Fuzzy matching using character positions
        matched_indices = []
        query_idx = 0
        target_idx = 0
        
        while query_idx < len(query) and target_idx < len(target):
            if query[query_idx] == target[target_idx]:
                matched_indices.append(target_idx)
                query_idx += 1
            target_idx += 1
            
        if query_idx == len(query):
            # All query characters matched
            score = len(query) / len(target)
            return score, matched_indices
            
        # Partial match
        score = len(matched_indices) / len(query)
        return score, matched_indices
        
    def calculate_similarity(self, s1: str, s2: str) -> float:
        """
        Calculate similarity between two strings using Jaccard similarity
        
        Args:
            s1: First string
            s2: Second string
            
        Returns:
            Similarity score (0-1)
        """
        set1 = set(s1.lower())
        set2 = set(s2.lower())
        
        if not set1 or not set2:
            return 0.0
            
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        return intersection / union if union > 0 else 0.0
        
    def calculate_levenshtein(self, s1: str, s2: str) -> int:
        """
        Calculate Levenshtein distance between strings
        
        Args:
            s1: First string
            s2: Second string
            
        Returns:
            Edit distance
        """
        if len(s1) < len(s2):
            return self.calculate_levenshtein(s2, s1)
            
        if len(s2) == 0:
            return len(s1)
            
        previous_row = range(len(s2) + 1)
        
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                
                current_row.append(min(insertions, deletions, substitutions))
                
            previous_row = current_row
            
        return previous_row[-1]
        
    def find_best_match(self, query: str, items: List[str]) -> Optional[Tuple[str, float]]:
        """
        Find best matching item from list
        
        Args:
            query: Search query
            items: List of items to search
            
        Returns:
            Tuple of (best_match, score) or None
        """
        best_match = None
        best_score = 0.0
        
        for item in items:
            score = self.calculate_similarity(query, item)
            if score > best_score:
                best_score = score
                best_match = item
                
        if best_score > 0.3:
            return best_match, best_score
            
        return None
        
    def get_stats(self) -> Dict[str, any]:
        """
        Get search statistics
        
        Returns:
            Statistics dictionary
        """
        return {
            'indexed_items': len(self.indexed_items)
        }


# Global fuzzy search instance
fuzzy_search = FuzzySearch()
