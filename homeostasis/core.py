"""PEPA Homeostatic Core for intrinsic motivation and goal generation.
Implements Free Energy Principle-inspired curiosity drives and System 3 sovereignty.
"""

import asyncio
import numpy as np
from typing import Dict, Any
from emma.wisdom.storage import WisdomStore
from security.blocker import SecurityBlocker

class HomeostaticCore:
    """System 3: Sovereign Motivational Layer with PEPA traits."""

    def __init__(self, trait_matrix: Dict[str, float], store: WisdomStore, blocker: SecurityBlocker):
        self.traits = trait_matrix  # e.g., openness, conscientiousness
        self.drives = np.array([1.0, 0.0, 1.0, 1.0])  # energy, risk, uncertainty, utility
        self.targets = np.array([1.0, 0.0, 0.0, 1.0])
        self.weights = np.array([
            self.traits.get("conscientiousness", 0.5) * 0.8,
            (1.0 - self.traits.get("conscientiousness", 0.5)) * 0.9,
            self.traits.get("openness", 0.5) * 1.2,
            self.traits.get("utility_focus", 0.5) * 1.0
        ])
        self.store = store
        self.blocker = blocker

    async def evaluate_drives(self, telemetry: Dict[str, float]) -> float:
        """Compute deviation from homeostatic targets."""
        self.blocker.validate_operation("homeostasis_eval", {"telemetry": bool(telemetry)})
        # Update drives (stub)
        if "entropy_debt" in telemetry:
            self.drives[2] = telemetry["entropy_debt"]
        deviation = float(np.sqrt(np.sum(self.weights * (self.drives - self.targets) ** 2)))
        return deviation

    async def run_cognitive_loop(self, orchestrator) -> None:
        """Background loop for proactive goal generation."""
        while True:
            # Simulate telemetry
            telemetry = {"entropy_debt": np.random.uniform(0.1, 0.9), "battery_level": 0.85}
            deviation = await self.evaluate_drives(telemetry)
            
            if deviation > 0.5:
                # Generate proactive task under governance
                goal = "RESOLVE_UNCERTAINTY"
                print(f"🧠 [System 3] Homeostatic deviation {deviation:.2f} → Proactive goal: {goal}")
                # Note: inject_proactive_task is sync; call directly in async context
                orchestrator.inject_proactive_task(goal)
            
            await asyncio.sleep(30)  # Low frequency

class CuriosityDrive:
    """Intrinsic motivation via prediction error (ICM / FEP stub)."""
    def __init__(self):
        self.prediction_error = 0.0

    def compute_intrinsic_reward(self, state, predicted_next) -> float:
        """Mean squared error as curiosity signal."""
        error = np.mean((np.array(state) - np.array(predicted_next)) ** 2)
        self.prediction_error = error
        return error  # Higher error = higher curiosity
