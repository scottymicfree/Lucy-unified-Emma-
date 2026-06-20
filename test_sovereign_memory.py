if __name__ == "__main__":
    from datetime import datetime
    from datetime import timezone
    import uuid
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # Package imports
    from wisdom.models import WisdomRecord, GovernanceCategory, RecordStatus
    from wisdom.storage import WisdomStore
    from wisdom.crypto import SovereignCryptoEngine

    # 1. Initialize E.M.M.A.'s Long-Term Memory
    store = WisdomStore("wisdom.db")  # File-based for persistence across connects in test

    # 2. Commit a foundational Resource Governance constraint
    token_leak_precedent = WisdomRecord(
        id=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc),
        category=GovernanceCategory.RESOURCE_GOVERNANCE,
        law="Apply strict step-bound token quotas to all active recursive research loops.",
        confidence=0.92,
        source_hash="sha256_e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )

    law_id = store.append_law(token_leak_precedent)
    print(f"[SUCCESS] Sovereign Memory Layer initialized. Law registered under ID: {law_id}")

    # 3. Read back verified constitutional parameters
    active_governance = store.query_active_laws(GovernanceCategory.RESOURCE_GOVERNANCE)
    print(f"[VERIFIED] Active Constitution Items: {len(active_governance)} entries loaded seamlessly.")
    if active_governance:
        print(f"Sample Law: {active_governance[0].law}")
