from emma.security.blocker import SecurityBlocker
from agents.base import LucyAgent

class HyperSwarmCoordinator:
    """Distributed multi-agent coordination under E.M.M.A. governance."""

    def __init__(self, blocker: SecurityBlocker):
        self.blocker = blocker
        self.agents = []

    def register_agent(self, agent: LucyAgent):
        self.blocker.validate_operation("register_agent", {"agent": agent.name})
        self.agents.append(agent)
        print(f"Agent {agent.name} registered in HyperSwarm.")