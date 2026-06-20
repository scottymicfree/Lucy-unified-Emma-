from typing import Dict, Any, Optional
import importlib
from security.blocker import SecurityBlocker, SecurityViolation
from emma.wisdom.storage import WisdomStore

class PlatformIntegrator:
    """Manages integration with external AI platforms. E.M.M.A. governs all with -1 veto offset."""

    def __init__(self, store: WisdomStore, blocker: SecurityBlocker):
        self.store = store
        self.blocker = blocker
        self.active_platforms: Dict[str, Any] = {}
        self.safety_offset = -1  # E.M.M.A. veto priority

    def register_platform(self, name: str, config: Dict[str, Any]) -> bool:
        """Register and initialize platform under E.M.M.A. governance."""
        self.blocker.validate_operation("register_platform", {"platform": name, "config": config})

        # Query sovereign laws for approval
        laws = self.store.query_active_laws()
        if any("no_external" in law.law.lower() for law in laws):
            print(f"🚫 E.M.M.A. blocked external platform: {name}")
            return False

        try:
            if name.lower() == "ollama":
                # Local-first preferred
                self.active_platforms[name] = {"type": "local", "client": "ollama"}
            elif name.lower() in ["openai", "anthropic", "grok", "huggingface"]:
                self.active_platforms[name] = {"type": "api", "config": config}
            else:
                print(f"⚠️ Unsupported platform: {name}")
                return False

            print(f"✅ Platform {name} registered under E.M.M.A. governance.")
            return True
        except Exception as e:
            print(f"❌ Registration failed: {e}")
            return False

    def route_to_platform(self, platform_name: str, prompt: str, **kwargs) -> Optional[str]:
        """Route request through rich E.M.M.A. governance engine."""
        self.blocker.validate_operation("route_to_platform", {"platform": platform_name, "prompt": prompt[:100]})

        if platform_name not in self.active_platforms:
            print(f"❌ Platform not registered: {platform_name}")
            return None

        # Use rich governance (passed or integrated via orchestrator)
        # For standalone: simple fallback
        from governance.governance_engine import GovernanceEngine
        gov = GovernanceEngine(self.store, self.blocker)  # Demo instance
        gov_result = gov.evaluate_request("platform_request", {"platform": platform_name, "prompt": prompt[:100]})

        if gov_result["decision"] in ["DENY", "QUARANTINE"]:
            return f"[GOVERNED: {gov_result['decision']}] {gov_result['reason']}"
        elif gov_result["decision"] == "REDIRECT":
            print(f"🔄 REDIRECT to local Ollama per governance.")
            return "Simulated local Ollama response (redirected)."

        # Simulated response for APPROVE / APPROVE_WITH_LIMITS
        print(f"🔀 Routed to {platform_name} under {gov_result['decision']}: {prompt[:50]}... | Constraints: {gov_result.get('constraints')}")
        return f"Simulated response from {platform_name} for: {prompt[:100]}"

    def list_platforms(self) -> Dict:
        """List active integrations."""
        return self.active_platforms