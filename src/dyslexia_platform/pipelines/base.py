"""
Base classes and interfaces for analysis pipelines.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import logging
import time
from datetime import datetime

from ..shared.exceptions import AnalysisError
from ..shared.utils import generate_session_id, calculate_confidence_score

logger = logging.getLogger(__name__)


class BasePipeline(ABC):
    """Base class for all analysis pipelines."""
    
    def __init__(self, name: str):
        self.name = name
        self.initialized = False
        self.model_versions = {}
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup pipeline-specific logging."""
        self.logger = logging.getLogger(f"dyslexia_platform.pipelines.{self.name}")
    
    @abstractmethod
    async def initialize(self):
        """Initialize the pipeline and its models."""
        pass
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data and return analysis results."""
        pass
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get pipeline metadata including model versions."""
        return {
            "pipeline_name": self.name,
            "initialized": self.initialized,
            "model_versions": self.model_versions,
            "timestamp": datetime.now().isoformat()
        }


class AnalysisPipeline(BasePipeline):
    """Base class for analysis pipelines with common functionality."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.confidence_threshold = 0.5
    
    async def analyze_with_timing(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze input with performance timing."""
        start_time = time.time()
        session_id = generate_session_id()
        
        try:
            self.logger.info(f"Starting analysis with session {session_id}")
            
            if not self.initialized:
                await self.initialize()
            
            # Process the input
            result = await self.process(input_data)
            
            # Add metadata
            processing_time = time.time() - start_time
            result.update({
                "session_id": session_id,
                "processing_time": processing_time,
                "pipeline_metadata": self.get_metadata(),
                "timestamp": datetime.now().isoformat()
            })
            
            self.logger.info(f"Analysis completed in {processing_time:.2f}s")
            return result
            
        except Exception as e:
            self.logger.error(f"Analysis failed for session {session_id}: {e}")
            raise AnalysisError(f"Pipeline {self.name} failed: {e}")
    
    def _calculate_overall_confidence(self, individual_scores: List[float]) -> float:
        """Calculate overall confidence from individual component scores."""
        return calculate_confidence_score(individual_scores)
    
    def _generate_recommendations(self, analysis_results: Dict[str, Any], 
                                confidence: float) -> List[str]:
        """Generate recommendations based on analysis results."""
        recommendations = []
        
        # Add confidence-based recommendations
        if confidence > 0.8:
            recommendations.append("Results indicate potential areas for attention")
        elif confidence > 0.5:
            recommendations.append("Consider additional assessment for comprehensive evaluation")
        else:
            recommendations.append("Results are inconclusive, recommend professional evaluation")
        
        return recommendations