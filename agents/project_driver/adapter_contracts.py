from abc import ABC, abstractmethod
from typing import Protocol

from core_models import ProjectPlan, ProjectTask, ProjectMilestone, ProjectRisk, ProjectDecision


class TaskAdapter(ABC):
    """Provider-neutral contract for writing tasks to an external system."""

    @abstractmethod
    def create_task(self, task: ProjectTask) -> str:
        """Create one task and return provider-specific external ID."""
        raise NotImplementedError


class MilestoneAdapter(ABC):
    """Provider-neutral contract for writing milestones to an external system."""

    @abstractmethod
    def create_milestone(self, milestone: ProjectMilestone) -> str:
        """Create one milestone and return provider-specific external ID."""
        raise NotImplementedError


class RiskAdapter(ABC):
    """Provider-neutral contract for writing risks to an external system."""

    @abstractmethod
    def record_risk(self, risk: ProjectRisk) -> str:
        """Record one project risk and return provider-specific external ID."""
        raise NotImplementedError


class DecisionAdapter(ABC):
    """Provider-neutral contract for writing decisions to an external system."""

    @abstractmethod
    def record_decision(self, decision: ProjectDecision) -> str:
        """Record one decision and return provider-specific external ID."""
        raise NotImplementedError


class PlanPublisher(ABC):
    """Provider-neutral contract for publishing a full project plan."""

    @abstractmethod
    def publish_plan(self, plan: ProjectPlan) -> dict:
        """Publish a complete ProjectPlan and return provider mapping metadata."""
        raise NotImplementedError
