from typing import Optional
import asyncio
from emma.wisdom.storage import WisdomStore
from security.blocker import SecurityBlocker
from sandbox.blackboard import Blackboard, Proposal
from homeostasis.core import HomeostaticCore, CuriosityDrive
from acoustic.gateway import AcousticGateway
from lucyai.protocols import llm_interlang_compress  # Stub
from integrations.platforms import PlatformIntegrator
from governance.governance_engine import GovernanceEngine
from emma.reflection.engine import ReflectionEngine

class EmmaOrchestrator:
    """E.M.M.A. Kernel Orchestrator - Task routing, agent lifecycle, SafeGuard integration."""

    def __init__(self, store: WisdomStore, blocker: SecurityBlocker, charter: dict):
        self.store = store
        self.blocker = blocker
        self.charter = charter
        self.agents = {}
        self.blackboard = Blackboard(store=store, blocker=blocker)
        
        # New OS_Lucy components
        traits = {"openness": 0.8, "conscientiousness": 0.7, "utility_focus": 0.9}
        self.homeostasis = HomeostaticCore(traits, store, blocker)
        self.curiosity = CuriosityDrive()
        self.acoustic = AcousticGateway(store, blocker)
        
        # AI Platform Integrations + Rich Governance governed by E.M.M.A.
        self.platforms = PlatformIntegrator(store, blocker)
        self.governance = GovernanceEngine(store, blocker)
        # Register preferred local-first platforms
        self.platforms.register_platform("ollama", {"host": "localhost"})
        self.platforms.register_platform("grok", {"api_key": "stub_xai"})
        
        # Reflection Engine for closed-loop evolution
        self.reflection = ReflectionEngine(store, blocker, self.governance)
        
        print("🧠 OS_Lucy cognitive layers (PEPA + Curiosity) initialized.")
        print("🏛️ Rich Governance + Reflection Engine active under E.M.M.A.")

    def initialize_swarm(self):
        """Initialize HyperSwarm under governance."""
        self.blocker.validate_operation("swarm_init", {"caller_module": "orchestrator"})
        print("🌐 HyperSwarm initialized with governance constraints.")
        # Stub for agent registration

    async def start_proactive_systems(self):
        """Launch acoustic + homeostasis loops for Level 5 autonomy."""
        asyncio.create_task(self.acoustic.start_listening(self))
        asyncio.create_task(self.homeostasis.run_cognitive_loop(self))
        print("🌌 Proactive OS_Lucy systems active: Ambient listening + Epistemic drives.")

    def route_task(self, task: str):
        """Safe task routing with wisdom lookup."""
        self.blocker.validate_operation("route_task", {"task": task})
        active_laws = self.store.query_active_laws()
        print(f"Routing task under {len(active_laws)} active laws: {task}")
        # TODO: Full DAG + lanes implementation

    def process_proposal_pipeline(self, title: str, description: str, proposer: str, code_snippet: Optional[str] = None):
        """Full sandbox: Blackboard proposal → Runtime simulation → Human approval → Production."""
        proposal = Proposal(title=title, description=description, proposer=proposer, code_snippet=code_snippet)
        self.blackboard.post_proposal(proposal)
        
        # Runtime simulation
        sim_results = self.blackboard.simulate_proposal(proposal.id)
        print(f"[SIM] Results: {sim_results}")
        
        # Human approval pipeline (blocks until input)
        approved = self.blackboard.request_human_approval(proposal.id)
        
        if approved:
            print(f"✅ Proposal {proposal.id} APPROVED for production integration.")
            # Here: generate/production code would be committed safely
            return proposal.id
        else:
            print("❌ Proposal rejected.")
            return None

    def inject_proactive_task(self, goal: str):
        """System 3 → Orchestrator for autonomous goals."""
        self.blocker.validate_operation("proactive_task", {"goal": goal})
        print(f"📋 [Orchestrator] Injected proactive task from homeostasis: {goal}")
        # Route to ThinkTank or TaskFlow

    async def process_intent(self, intent: str):
        """Handle acoustic-derived intents."""
        print(f"🎯 Intent from gateway: {intent}")
        self.route_task(f"Handle ambient intent: {intent}")

    def route_to_platform(self, platform: str, prompt: str, **kwargs):
        """Delegate to E.M.M.A.-governed PlatformIntegrator with full control."""
        return self.platforms.route_to_platform(platform, prompt, **kwargs)

    def run_reflection_cycle(self):
        """Trigger governance reflection for evolutionary learning."""
        print("🔄 Running E.M.M.A. Reflection Cycle...")
        self.reflection.observe({"type": "platform_request", "platform": "grok", "outcome": "evaluated"})
        self.reflection.observe({"type": "resource", "memory_pressure": True})
        self.reflection.reflect()