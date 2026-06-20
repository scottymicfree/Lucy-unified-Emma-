from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any

class GovernanceCategory(Enum):
    IDENTITY = "IDENTITY"
    STRATEGY = "STRATEGY"
    ETHICS = "ETHICS"
    RESOURCE_GOVERNANCE = "RESOURCE_GOVERNANCE"

class RecordStatus(Enum):
    ACTIVE = "ACTIVE"
    DEPRECATED = "DEPRECATED"
    SUPERSEDED = "SUPERSEDED"

@dataclass(frozen=True)
class IdentityRecord:
    """The immutable core definition of E.M.M.A.'s existential boundaries."""
    version: int
    timestamp: datetime
    mission: str
    vision: List[str]
    constraints: List[str]
    voice: str
    non_negotiables: List[str]
    sovereignty_rules: List[str]

@dataclass
class WisdomRecord:
    """A persistent meta-cognitive truth derived from operational experience."""
    id: str
    timestamp: datetime
    category: GovernanceCategory
    law: str
    confidence: float
    source_hash: str           # Cryptographic link to the underlying Lucy execution logs
    status: RecordStatus = RecordStatus.ACTIVE
    supersedes: Optional[str] = None
    signature: Optional[str] = None  # Self-signed integrity block

@dataclass(frozen=True)
class PolicyRecord:
    """An operational target manifest compiled for the Lucy Kernel."""
    name: str
    source_wisdom_id: str
    confidence_threshold: float
    enforcement_rules: Dict[str, Any]
    compiled_at: datetime = field(default_factory=datetime.utcnow)
