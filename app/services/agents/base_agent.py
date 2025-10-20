from abc import ABC, abstractmethod


class BaseAgent(ABC):
    name: str

    @abstractmethod
    async def run(self):
        """Perform the main task (e.g., scrape, analyze, etc.)"""

    @abstractmethod
    async def analyze(self, data):
        """Use LangGraph or AI model to interpret results."""

    @abstractmethod
    async def notify(self, message: str):
        """Send alerts or updates (via Resend)."""
