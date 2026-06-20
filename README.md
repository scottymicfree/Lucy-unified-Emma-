# E.M.M.A. Core (emma-core)

**Sovereign Memory Foundation for Lucy Core AI**

Production-grade implementation of the immutable constitutional core for E.M.M.A. (Enhanced Machine Mind Architecture). 

## Key Features
- **Immutable Sovereign Memory**: Cryptographically signed WisdomRecords in append-only SQLite ledger.
- **Advanced Security Blocking**: `security/blocker.py` enforces strict controls against code injection, exfiltration, recursion drift, and unauthorized module access.
- **Identity Invariants**: Bootstrap core self-definition that survives reboots and swarm chaos.
- **Policy Cascade**: Translates laws into enforceable runtime policies.
- **Tamper-Evident**: HMAC, SHA-256, signature verification on every critical operation.

## Security Priority
Every mutation and query is gated through `SecurityBlocker.validate_operation()`. Blocked patterns include system calls, eval/exec, network exfil, etc. Designed for local-first, human-sovereign execution.

## Setup
```bash
cd "E:\lucy emma unified\upgraded\lucy-emma-unified"
pip install -e .
python test_sovereign_memory.py
```

## Integration with Lucy Core
Hook into orchestrator boot sequence. Load Co-Evolution Charter as initial IdentityRecord + WisdomRecords.

## Next
- Full TPM/Ed25519 signing
- Distributed swarm replication under charter rules
- Red-team hardening

Built as unified extension from scottymicfree's repos.