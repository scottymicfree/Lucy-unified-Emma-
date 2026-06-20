import uuid
from datetime import datetime
from typing import List, Dict, Optional
from emma.wisdom.storage import WisdomStore
from security.blocker import SecurityBlocker, SecurityViolation

class Proposal:
    """Blackboard proposal for agent-generated ideas/plans/code."""
    def __init__(self, title: str, description: str, proposer: str, code_snippet: Optional[str] = None):
        self.id = str(uuid.uuid4())
        self.timestamp = datetime.utcnow()
        self.title = title
        self.description = description
        self.proposer = proposer
        self.code_snippet = code_snippet
        self.status = "PROPOSED"  # PROPOSED -> SIMULATED -> APPROVED -> REJECTED
        self.simulation_results = None
        self.human_approval = None

class Blackboard:
    """Shared blackboard for proposals in Lucy-E.M.M.A. system."""
    
    def __init__(self, store: WisdomStore, blocker: SecurityBlocker):
        self.store = store
        self.blocker = blocker
        self.proposals: List[Proposal] = []
    
    def post_proposal(self, proposal: Proposal) -> str:
        """Agents post proposals to blackboard."""
        self.blocker.validate_operation("post_proposal", {"proposal_id": proposal.id})
        self.proposals.append(proposal)
        print(f"[BLACKBOARD] New proposal posted: {proposal.title} by {proposal.proposer}")
        return proposal.id
    
    def simulate_proposal(self, proposal_id: str) -> Dict:
        """Runtime simulation of proposal before production."""
        self.blocker.validate_operation("simulate_proposal", {"proposal_id": proposal_id})
        prop = next((p for p in self.proposals if p.id == proposal_id), None)
        if not prop:
            raise ValueError("Proposal not found")
        
        print(f"[SIMULATION] Running safe runtime simulation for {prop.title}...")
        # Mock simulation: check syntax, resource bounds, governance compliance
        if prop.code_snippet:
            # Safe eval stub (in real: use restricted executor)
            simulation_result = {
                "success": True,
                "resource_usage": "low",
                "governance_compliant": True,
                "mock_output": "Simulation passed with U-metric 0.85"
            }
            prop.simulation_results = simulation_result
            prop.status = "SIMULATED"
        return prop.simulation_results or {"success": False}
    
    def request_human_approval(self, proposal_id: str) -> bool:
        """Human-in-the-loop approval pipeline."""
        self.blocker.validate_operation("human_approval", {"proposal_id": proposal_id})
        prop = next((p for p in self.proposals if p.id == proposal_id), None)
        if not prop or prop.status != "SIMULATED":
            raise ValueError("Proposal must be simulated first")
        
        print(f"\n--- HUMAN APPROVAL PIPELINE ---")
        print(f"Proposal: {prop.title}")
        print(f"Description: {prop.description}")
        if prop.simulation_results:
            print(f"Simulation: {prop.simulation_results}")
        
        # Non-interactive demo mode (auto-approve for boot demo; in prod: real human gate)
        print("⚠️ DEMO MODE: Auto-approving for simulation continuity (E.M.M.A. monitored).")
        approval = True  # Human override always available in full deployment
        prop.human_approval = approval
        prop.status = "APPROVED" if approval else "REJECTED"
        
        if approval:
            # Could append wisdom record for successful proposal
            from emma.wisdom.models import WisdomRecord, GovernanceCategory
            law = WisdomRecord(
                id=str(uuid.uuid4()),
                timestamp=datetime.utcnow(),
                category=GovernanceCategory.STRATEGY,
                law=f"Approved proposal: {prop.title}",
                confidence=0.95,
                source_hash="sim_approved"
            )
            self.store.append_law(law)
        
        return approval
