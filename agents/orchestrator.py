"""
Multi-Agent Orchestrator: Coordinates the execution pipeline:
User Query -> Router Agent -> Core Geological Agent -> Validation Agent -> Validated Output
"""

import sys
import os
from pathlib import Path

# Add project root and backend to sys.path for direct script execution
project_root = str(Path(__file__).resolve().parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
backend_path = str(Path(__file__).resolve().parent.parent / "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from typing import Dict, Any, List
from agents.router.router_agent import RouterAgent, RoutingDecision
from agents.core.core_agent import CoreGeologicalAgent
from agents.validation.validation_agent import ValidationAgent, ValidationReport

class MultiAgentOrchestrator:
    def __init__(self):
        self.router = RouterAgent()
        self.core_agent = CoreGeologicalAgent()
        self.validation_agent = ValidationAgent()

    def handle_query(self, user_query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        End-to-end multi-agent processing pipeline with fault tolerance across each stage.
        """
        # Step 1: Route query with fallback
        try:
            routing = self.router.route(user_query)
        except Exception as e:
            routing = RoutingDecision(
                intent="GENERAL_QUERY",
                confidence=0.5,
                target_agents=["CoreGeologicalAgent"],
                parameters={"query": user_query},
                reasoning=f"Router fallback triggered due to exception: {e}"
            )

        # Step 2: Core processing with fallback
        try:
            core_output = self.core_agent.process(
                task_type=routing.intent,
                query=user_query,
                context=context
            )
        except Exception as e:
            core_output = {
                "status": "error",
                "task_type": routing.intent,
                "data": {},
                "narrative": "Unable to process this query — please try rephrasing.",
                "error": str(e),
                "citations": []
            }

        # Step 3: Validate output with fallback
        try:
            val_report = self.validation_agent.validate_geological_output(core_output)
        except Exception as e:
            val_report = ValidationReport(
                is_valid=False,
                confidence_score=0.5,
                passed_rules=[],
                failed_rules=[f"Validation runtime exception: {e}"],
                remediation_notes=f"Validation failed with error: {e}"
            )

        # Surface citations visibly at the top level per PRD FR-7
        citations = core_output.get("citations", [])

        return {
            "query": user_query,
            "routing_decision": routing.model_dump() if hasattr(routing, "model_dump") else routing,
            "core_output": core_output,
            "citations": citations,
            "validation": val_report.model_dump() if hasattr(val_report, "model_dump") else val_report,
            "final_answer": core_output.get("narrative", ""),
            "is_verified": getattr(val_report, "is_valid", False)
        }

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    orchestrator = MultiAgentOrchestrator()
    sample_query = "What causes coal seams to split into multiple benches within the same borehole?"
    result = orchestrator.handle_query(sample_query)
    print("Multi-Agent Pipeline Test:")
    print(f"Intent: {result['routing_decision']['intent']}")
    print(f"Answer: {result['final_answer']}")
    print(f"Top-Level Citations Count: {len(result['citations'])}")
    print(f"Validated: {result['is_verified']} (Confidence: {result['validation']['confidence_score']})")
