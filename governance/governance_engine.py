from typing import Dict, Any, Optional, List
from enum import Enum
import hashlib
from datetime import datetime
from emma.wisdom.storage import WisdomStore
from security.blocker import SecurityBlocker

class GovernanceDecision(Enum):
    APPROVE = "APPROVE"
    APPROVE_WITH_LIMITS = "APPROVE_WITH_LIMITS"
    REDIRECT = "REDIRECT"
    QUARANTINE = "QUARANTINE"
    DENY = "DENY"
    ESCALATE_TO_HUMAN = "ESCALATE_TO_HUMAN"

class GovernanceEngine:
    """Rich governance decision engine for E.M.M.A. as strategic governor."""

    def __init__(self, store: WisdomStore, blocker: SecurityBlocker):
        self.store = store
        self.blocker = blocker
        print("🏛️ Rich Governance Engine initialized with multi-outcome decisions.")

    def evaluate_request(self, request_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Rich decision model replacing single veto."""
        self.blocker.validate_operation("governance_evaluate", {"request": request_type})
        
        active_laws = self.store.query_active_laws()
        
        # Forecasting stub (predictive)
        forecast = self._generate_forecast(context)
        
        decision = GovernanceDecision.APPROVE
        constraints = {}
        reason = "Compliant with sovereign laws."

        # Example logic
        if "external" in request_type.lower() or "grok" in context.get("platform", ""):
            if any("local" in law.law.lower() for law in active_laws):
                decision = GovernanceDecision.REDIRECT
                reason = "Equivalent local Ollama model available. REDIRECT enforced."
            else:
                decision = GovernanceDecision.APPROVE_WITH_LIMITS
                constraints = {
                    "token_budget": 5000,
                    "file_writes": False,
                    "mode": "read-only"
                }
                reason = "Approved with resource and safety limits."

        # Preemptive actions from forecast
        if forecast.get("risk_high"):
            decision = GovernanceDecision.QUARANTINE if decision == GovernanceDecision.APPROVE else decision
            reason += " | Preemptive quarantine due to forecasted resource pressure."

        result = {
            "decision": decision.value,
            "reason": reason,
            "constraints": constraints,
            "forecast": forecast
        }
        
        # Log to observations for reflection
        from emma.reflection.engine import ReflectionEngine  # Late import to avoid cycles
        # Assume reflection_engine passed or global; for demo
        print(f"🛡️ E.M.M.A. GOVERNANCE: {request_type} → {decision.value} | {reason}")
        return result

    def _generate_forecast(self, context: Dict) -> Dict:
        """Governance Forecasting: Predict consequences."""
        # Stub predictive logic based on homeostasis/observations
        return {
            "risk_high": context.get("memory_pressure", False) or context.get("token_usage", 0) > 80,
            "prediction": "Potential quota exceed in 20min if swarm active.",
            "preemptive_action": "Lower budgets"
        }

    def update_policies_from_wisdom(self, new_wisdom: List):
        """Apply new wisdom to runtime policies."""
        print(f"📜 Updated policies from {len(new_wisdom)} new wisdom records.")
