"""
Router Agent: Analyzes user prompts and classifies query intent to determine
the optimal multi-agent execution path.
"""

from typing import Dict, Any, Literal, List
from pydantic import BaseModel, Field

IntentType = Literal[
    "PQ_FAST_RESPONSE",
    "RESERVE_ESTIMATION",
    "DISCREPANCY_ANALYSIS",
    "STATUTORY_AUDIT",
    "GENERAL_QUERY"
]

class RoutingDecision(BaseModel):
    intent: IntentType
    confidence: float
    target_agents: List[str]
    parameters: Dict[str, Any] = Field(default_factory=dict)
    reasoning: str

class RouterAgent:
    """
    Classifies queries and routes to Core Geological Agent,
    Calculation Tools, or Report Studio.
    """

    def __init__(self, model_name: str = "gemini-1.5-flash"):
        self.model_name = model_name

    def route(self, user_query: str) -> RoutingDecision:
        """
        Analyzes query keywords, entities, and context to determine intent.
        """
        query_lower = user_query.lower()

        if any(term in query_lower for term in ["parliament", "starred question", "pq", "lok sabha", "rajya sabha", "brief"]):
            return RoutingDecision(
                intent="PQ_FAST_RESPONSE",
                confidence=0.96,
                target_agents=["CoreGeologicalAgent", "ValidationAgent", "ReportGenerator"],
                parameters={"query": user_query},
                reasoning="Query targets Parliamentary inquiry response conforming to Ministry format."
            )
        elif any(term in query_lower for term in ["discrepancy", "mecl", "cmpdi 2021", "reconciliation", "variance", "mismatch"]):
            return RoutingDecision(
                intent="DISCREPANCY_ANALYSIS",
                confidence=0.94,
                target_agents=["CoreGeologicalAgent", "ValidationAgent"],
                parameters={"query": user_query},
                reasoning="Query involves historical survey discrepancies across exploration agencies."
            )
        elif any(term in query_lower for term in ["reserve", "tonnage", "gcv", "grade", "stripping ratio", "calculate"]):
            return RoutingDecision(
                intent="RESERVE_ESTIMATION",
                confidence=0.93,
                target_agents=["CoreGeologicalAgent", "ValidationAgent"],
                parameters={"query": user_query},
                reasoning="Query requires quantitative mining formulas or coal grade classifications."
            )
        elif any(term in query_lower for term in ["dgms", "cmr 2017", "safety", "clearance", "form-v", "audit"]):
            return RoutingDecision(
                intent="STATUTORY_AUDIT",
                confidence=0.92,
                target_agents=["CoreGeologicalAgent", "ValidationAgent"],
                parameters={"query": user_query},
                reasoning="Query targets statutory safety clearances or DGMS CMR compliance."
            )
        else:
            return RoutingDecision(
                intent="GENERAL_QUERY",
                confidence=0.88,
                target_agents=["CoreGeologicalAgent"],
                parameters={"query": user_query},
                reasoning="General or scientific exploration inquiry routed to Core Agent for synthesis."
            )
