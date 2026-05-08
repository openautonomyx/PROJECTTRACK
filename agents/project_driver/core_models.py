from pydantic import BaseModel, Field
from typing import Literal


class ProjectTask(BaseModel):
    title: str
    description: str
    priority: Literal['low', 'medium', 'high', 'critical'] = 'medium'
    status: Literal['todo', 'in_progress', 'blocked', 'done'] = 'todo'
    acceptance_criteria: list[str] = Field(default_factory=list)
    owner_role: str | None = None


class ProjectMilestone(BaseModel):
    title: str
    goal: str
    tasks: list[ProjectTask] = Field(default_factory=list)
    success_criteria: list[str] = Field(default_factory=list)


class ProjectRisk(BaseModel):
    title: str
    impact: Literal['low', 'medium', 'high', 'critical'] = 'medium'
    mitigation: str


class ProjectDecision(BaseModel):
    title: str
    context: str
    decision: str
    consequences: list[str] = Field(default_factory=list)


class ProjectPlan(BaseModel):
    summary: str
    milestones: list[ProjectMilestone] = Field(default_factory=list)
    risks: list[ProjectRisk] = Field(default_factory=list)
    decisions: list[ProjectDecision] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)
