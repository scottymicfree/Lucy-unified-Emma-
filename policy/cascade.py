# Policy cascade translator
from datetime import datetime
from emma.wisdom.models import PolicyRecord, WisdomRecord
from typing import List

class PolicyCascade:
    @staticmethod
    def compile_policies(active_wisdom: List[WisdomRecord]) -> List[PolicyRecord]:
        """Translates WisdomRecords into enforceable PolicyRecords for runtime."""
        policies = []
        for w in active_wisdom:
            policy = PolicyRecord(
                name=f"policy_from_{w.id[:8]}",
                source_wisdom_id=w.id,
                confidence_threshold=w.confidence * 0.9,
                enforcement_rules={"category": w.category.value, "law": w.law[:100]}
            )
            policies.append(policy)
        return policies
