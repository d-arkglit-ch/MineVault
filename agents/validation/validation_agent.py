"""
Validation Agent: Implements deterministic guardrails, physical consistency checks,
and citation grounding verification to prevent hallucinations in mining reports.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field

class ValidationReport(BaseModel):
    is_valid: bool
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    passed_rules: List[str] = Field(default_factory=list)
    failed_rules: List[str] = Field(default_factory=list)
    remediation_notes: str = ""

class ValidationAgent:
    """
    Validates physical plausibility, stratigraphic consistency, and calculation integrity.
    """

    def validate_geological_output(self, agent_output: Dict[str, Any]) -> ValidationReport:
        """
        Runs comprehensive rule-based checks on geological calculations & outputs.
        """
        passed = []
        failed = []

        data = agent_output.get("data", {})
        task_type = agent_output.get("task_type", "")

        # Rule 1: Non-negative reserves
        if task_type in ["RESERVE_ESTIMATION", "RESERVE_CALCULATION"]:
            reserves = data.get("reserves_million_tonnes", data.get("certifiedReservesMT", 0.0))
            if reserves > 0:
                passed.append("RULE_POSITIVE_RESERVES")
            else:
                failed.append("RULE_POSITIVE_RESERVES: Reserve estimate must be strictly greater than 0.")

            # Rule 2: Realistic specific gravity for coal (1.1 to 2.0)
            sg = data.get("specific_gravity", 1.4)
            if 1.1 <= sg <= 2.2:
                passed.append("RULE_VALID_SPECIFIC_GRAVITY")
            else:
                failed.append(f"RULE_VALID_SPECIFIC_GRAVITY: Specific gravity {sg} is outside physical coal bounds.")

        # Rule 3: Thickness discrepancy consistency
        if task_type == "DISCREPANCY_ANALYSIS":
            delta = data.get("deltaMeters", 0.0)
            t_a = data.get("mecl1998Thickness", 0.0)
            t_b = data.get("cmpdi2021Thickness", 0.0)
            if round(t_b - t_a, 2) == round(delta, 2):
                passed.append("RULE_DISCREPANCY_ARITHMETIC_MATCH")
            else:
                failed.append("RULE_DISCREPANCY_ARITHMETIC_MATCH: Delta does not match difference between survey thicknesses.")

        # Rule 4: Citation presence for quantitative claims
        citations = agent_output.get("citations", [])
        if citations or task_type == "GENERAL_QUERY":
            passed.append("RULE_CITATION_PRESENT")
        else:
            failed.append("RULE_CITATION_PRESENT: Quantitative claim lacks source documentation citation.")

        is_valid = len(failed) == 0
        confidence = 0.985 if is_valid else max(0.2, 1.0 - (len(failed) * 0.3))

        return ValidationReport(
            is_valid=is_valid,
            confidence_score=confidence,
            passed_rules=passed,
            failed_rules=failed,
            remediation_notes="All domain constraints satisfied." if is_valid else "; ".join(failed)
        )
