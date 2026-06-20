from datetime import datetime
import uuid
import hashlib
from typing import List, Dict, Any
from emma.wisdom.models import WisdomRecord, GovernanceCategory, RecordStatus
from emma.wisdom.storage import WisdomStore
from security.blocker import SecurityBlocker, SecurityViolation
from governance.governance_engine import GovernanceEngine

class ReflectionEngine:
    """E.M.M.A. Reflection subsystem for closed-loop governance evolution.
    Observation → Reflection → New Wisdom → Policy Update → Enforcement.
    Closes the loop for strategic, forecasting governance."""

    def __init__(self, store: WisdomStore, blocker: SecurityBlocker, governance: GovernanceEngine):
        self.store = store
        self.blocker = blocker
        self.governance = governance
        self.observations: List[Dict] = []
        print("🔄 E.M.M.A. Reflection Engine initialized.")

    def observe(self, event: Dict[str, Any]) -> None:
        """Record operational observations for reflection."""
        self.blocker.validate_operation("reflection_observe", {"event_type": event.get("type")})
        self.observations.append({
            "id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow(),
            **event
        })
        if len(self.observations) > 50:  # Compact periodically
            self._compact_observations()

    def _compact_observations(self):
        """Summarize old observations to manage memory."""
        # Stub for cognitive folding
        self.observations = self.observations[-20:]

    def reflect(self) -> List[WisdomRecord]:
        """Perform reflection: Analyze observations → Generate new wisdom."""
        self.blocker.validate_operation("reflection_cycle", {"obs_count": len(self.observations)})
        
        if not self.observations:
            return []

        # Simulate analysis (in full: LLM-as-Judge or pattern matching)
        new_wisdom = []
        for obs in self.observations[-5:]:  # Recent focus
            if obs.get("type") == "platform_request" and obs.get("outcome") == "blocked":
                law = WisdomRecord(
                    id=str(uuid.uuid4()),
                    timestamp=datetime.utcnow(),
                    category=GovernanceCategory.STRATEGY,
                    law=f"Observed repeated external platform blocks. Recommend REDIRECT to local equivalents.",
                    confidence=0.85,
                    source_hash=hashlib.sha256(str(obs).encode()).hexdigest()[:16]
                )
                new_wisdom.append(law)
        
        # Forecast example
        if any("resource" in o.get("type", "") for o in self.observations):
            forecast_law = WisdomRecord(
                id=str(uuid.uuid4()),
                timestamp=datetime.utcnow(),
                category=GovernanceCategory.RESOURCE_GOVERNANCE,
                law="Forecast: Swarm activity likely to exceed token quota in next cycle. Preemptively apply limits.",
                confidence=0.78,
                source_hash="forecast_hash"
            )
            new_wisdom.append(forecast_law)

        for law in new_wisdom:
            self.store.append_law(law)
            self.governance.update_policies_from_wisdom([law])

        print(f"✅ Reflection complete: Generated {len(new_wisdom)} new WisdomRecords.")
        return new_wisdom

    def run_reflection_cycle(self):
        """Periodic reflection for governance evolution."""
        self.reflect()
