#!/usr/bin/env python3
"""
Lucy-E.M.M.A. Unified Boot Sequence
Initializes Sovereign Memory, Governance, Orchestrator, and Swarm.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from emma.identity.manager import IdentityManager
from emma.wisdom.storage import WisdomStore
from security.blocker import SecurityBlocker, SecurityViolation
from governance.charter_loader import load_co_evolution_charter
from orchestrator.core import EmmaOrchestrator

def boot_system():
    print("🚀 Booting Lucy Core AI with E.M.M.A. Kernel...")

    # 1. Security First
    blocker = SecurityBlocker()
    try:
        blocker.validate_operation("system_boot", {"caller_module": "lucy_boot"})
    except SecurityViolation as e:
        print(f"❌ SECURITY VIOLATION: {e}")
        sys.exit(1)

    # 2. Identity & Sovereign Memory
    identity = IdentityManager()
    if not identity.verify_identity():
        raise RuntimeError("Identity invariants violated!")

    store = WisdomStore()
    active_laws = store.query_active_laws()
    print(f"✅ Loaded {len(active_laws)} sovereign laws from immutable ledger.")

    # 3. Governance Charter
    charter = load_co_evolution_charter()
    print(f"✅ Co-Evolution Charter loaded with {len(charter.get('mandates', []))} mandates.")

    # 4. Orchestrator + Swarm + OS_Lucy Proactive Layers
    orchestrator = EmmaOrchestrator(store=store, blocker=blocker, charter=charter)
    orchestrator.initialize_swarm()
    # Launch Level 5 autonomy features
    import asyncio
    asyncio.run(orchestrator.start_proactive_systems())

    # Demo: Full Proposal Sandbox Pipeline
    print("\n🧪 Demonstrating Blackboard Proposal Sandbox + Human Approval Pipeline...")
    proposal_id = orchestrator.process_proposal_pipeline(
        title="Implement Enhanced Token Quota Enforcement",
        description="Add runtime simulation for recursive loops to prevent resource drift.",
        proposer="ResearchAgent",
        code_snippet="def enforce_quota(): pass  # Safe stub"
    )
    if proposal_id:
        print(f"✅ Production-ready proposal integrated: {proposal_id}")

    # Demo: Rich Governance + Reflection
    print("\n🏛️ Demonstrating Rich E.M.M.A. Governance (multi-outcome decisions)...")
    orchestrator.run_reflection_cycle()
    
    response = orchestrator.route_to_platform("ollama", "Explain sovereign memory in Lucy Core AI.")
    print(f"Ollama response: {response[:150]}...")
    response2 = orchestrator.route_to_platform("grok", "Summarize Co-Evolution Charter.")
    print(f"Grok response: {response2[:150]}...")

    print("\n🎉 Lucy-E.M.M.A. Unified System Ready!")
    print("Human override available. Local-first execution enforced. Rich governance + reflection active.")
    return orchestrator

if __name__ == "__main__":
    boot_system()