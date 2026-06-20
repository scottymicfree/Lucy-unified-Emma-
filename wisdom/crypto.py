import hashlib
import json
from datetime import datetime
from typing import Dict, Any
from .models import WisdomRecord, GovernanceCategory

class SovereignCryptoEngine:
    @staticmethod
    def compute_record_hash(record: WisdomRecord) -> str:
        """Generates a deterministic SHA-256 hash of a WisdomRecord's core data payload."""
        payload: Dict[str, Any] = {
            "id": record.id,
            "timestamp": record.timestamp.isoformat(),
            "category": record.category.value,
            "law": record.law,
            "confidence": round(record.confidence, 4),
            "source_hash": record.source_hash,
            "supersedes": record.supersedes
        }
        serialized = json.dumps(payload, sort_keys=True).encode('utf-8')
        return hashlib.sha256(serialized).hexdigest()

    @classmethod
    def sign_record(cls, record: WisdomRecord, private_key_stub: str = "EMMA_SOVEREIGN_ROOT") -> str:
        """Signs the record payload to establish historical and cryptographic un-linkability."""
        record_hash = cls.compute_record_hash(record)
        # In absolute production, sign this hash using an asymmetric keypair (e.g., Ed25519) via TPM
        signed_manifest = hashlib.sha256(f"{record_hash}:{private_key_stub}".encode('utf-8')).hexdigest()
        return f"emma_v1_{signed_manifest}"

    @classmethod
    def verify_record(cls, record: WisdomRecord) -> bool:
        """Validates that the record has not suffered data degradation or malicious injection."""
        if not record.signature:
            return False
        expected_sig = cls.sign_record(record)
        return record.signature == expected_sig
