#!/usr/bin/env python3
"""
Zero Trust Engine Template
Copy and customize for your agent deployment.

Usage:
    from zero_trust_engine import ZeroTrustEngine, Tier, ActionType
    
    engine = ZeroTrustEngine(tier=Tier.ENTERPRISE)
    agent = engine.register_agent("my_agent", ["read", "write"])
    result = engine.verify_action(ActionRequest(...))

Based on: Anthropic "Zero Trust for AI Agents" (2026)
"""

import hashlib
import json
import logging
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [ZERO-TRUST] %(message)s")
logger = logging.getLogger("zero-trust")


class Tier(Enum):
    FOUNDATION = "foundation"
    ENTERPRISE = "enterprise"
    ADVANCED = "advanced"


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ActionType(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    COMMUNICATE = "communicate"
    DELEGATE = "delegate"


class ResponseAction(Enum):
    ALERT = "alert"
    THROTTLE = "throttle"
    REVOKE_CREDENTIALS="revoke..."
    TERMINATE_SESSION = "terminate_session"
    QUARANTINE = "quarantine"
    SHUTDOWN = "shutdown"
    SHUTDOWN = "shutdown"


@dataclass
class AgentIdentity:
    agent_id: str
    name: str
    created_at: datetime
    public_key: str
    certificate: Optional[str] = None
    hardware_backed: bool = False
    status: str = "active"
    capabilities: list[str] = field(default_factory=list)
    blast_radius: RiskLevel = RiskLevel.MEDIUM


@dataclass
class PrivilegeScope:
    agent_id: str
    permissions: set[str]
    resources: set[str]
    granted_at: datetime
    expires_at: Optional[datetime] = None
    task_context: Optional[str] = None


@dataclass
class ActionRequest:
    agent_id: str
    action: ActionType
    resource: str
    context: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class VerificationResult:
    approved: bool
    reason: str
    risk_level: RiskLevel
    requires_approval: bool = False
    audit_trail: dict[str, Any] = field(default_factory=dict)


@dataclass
class MemoryEntry:
    entry_id: str
    agent_id: str
    session_id: str
    content_hash: str
    source: str
    created_at: datetime
    expires_at: Optional[datetime] = None
    quarantined: bool = False


class ZeroTrustEngine:
    def __init__(self, tier: Tier = Tier.ENTERPRISE, storage_path: str = None):
        self.tier = tier
        self.storage_path = Path(storage_path or "./zero_trust_data")
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.agents: dict[str, AgentIdentity] = {}
        self.privileges: dict[str, PrivilegeScope] = {}
        self.memory_entries: dict[str, MemoryEntry] = {}
        self._load_state()
        logger.info("Zero Trust Engine initialized (tier: %s)", tier.value)

    def _load_state(self):
        state_file = self.storage_path / "state.json"
        if state_file.exists():
            with open(state_file) as f:
                state = json.load(f)
            for d in state.get("agents", []):
                self.agents[d["agent_id"]] = AgentIdentity(**d)

    def _save_state(self):
        with open(self.storage_path / "state.json", "w") as f:
            json.dump({"agents": [asdict(a) for a in self.agents.values()]}, f, default=str)

    def register_agent(self, name: str, capabilities: list[str],
                       blast_radius: RiskLevel = RiskLevel.MEDIUM) -> AgentIdentity:
        agent_id = f"agent_{uuid.uuid4().hex[:16]}"
        public_key = hashlib.sha256(f"{agent_id}:{name}".encode()).hexdigest()
        cert = None
        if self.tier == Tier.ADVANCED:
            cert = json.dumps({"subject": f"CN={agent_id}", "serial": uuid.uuid4().hex})
        agent = AgentIdentity(agent_id=agent_id, name=name,
                              created_at=datetime.now(timezone.utc),
                              public_key=public_key, certificate=cert,
                              capabilities=capabilities, blast_radius=blast_radius)
        self.agents[agent_id] = agent
        self._save_state()
        logger.info("Registered agent: %s (%s)", name, agent_id)
        return agent

    def grant_privileges(self, agent_id: str, permissions: set[str],
                         resources: set[str], duration_minutes: int = None) -> PrivilegeScope:
        agent = self.agents[agent_id]
        effective = permissions.intersection(set(agent.capabilities))
        now = datetime.now(timezone.utc)
        scope = PrivilegeScope(
            agent_id=agent_id, permissions=effective, resources=resources,
            granted_at=now,
            expires_at=now + timedelta(minutes=duration_minutes) if duration_minutes else None
        )
        self.privileges[agent_id] = scope
        return scope

    def verify_action(self, request: ActionRequest) -> VerificationResult:
        agent = self.agents.get(request.agent_id)
        if not agent or agent.status != "active":
            return VerificationResult(approved=False, reason="Agent not active",
                                      risk_level=RiskLevel.CRITICAL)
        scope = self.privileges.get(request.agent_id)
        if not scope or request.action.value + "_*" not in scope.permissions:
            return VerificationResult(approved=False, reason="Insufficient privileges",
                                      risk_level=RiskLevel.HIGH)
        risk = self._assess_risk(request)
        needs_approval = risk in [RiskLevel.HIGH, RiskLevel.CRITICAL] if self.tier != Tier.FOUNDATION else True
        return VerificationResult(
            approved=not needs_approval,
            reason="Verified" if not needs_approval else "Requires human approval",
            risk_level=risk, requires_approval=needs_approval,
            audit_trail={"agent": request.agent_id, "action": request.action.value,
                         "resource": request.resource, "risk": risk.value}
        )

    def _assess_risk(self, request: ActionRequest) -> RiskLevel:
        score = {ActionType.READ: 1, ActionType.WRITE: 3, ActionType.EXECUTE: 4}.get(request.action, 2)
        if any(s in request.resource.lower() for s in ["password", "secret", "key"]):
            score += 4
        agent = self.agents.get(request.agent_id)
        if agent:
            score += {RiskLevel.LOW: 0, RiskLevel.MEDIUM: 1, RiskLevel.HIGH: 2, RiskLevel.CRITICAL: 3}.get(agent.blast_radius, 1)
        return RiskLevel.CRITICAL if score >= 8 else RiskLevel.HIGH if score >= 6 else RiskLevel.MEDIUM if score >= 4 else RiskLevel.LOW

    def store_memory(self, agent_id: str, session_id: str, content: str,
                     source: str, ttl_minutes: int = None) -> MemoryEntry:
        entry_id = f"mem_{uuid.uuid4().hex[:16]}"
        now = datetime.now(timezone.utc)
        entry = MemoryEntry(entry_id=entry_id, agent_id=agent_id, session_id=session_id,
                            content_hash=hashlib.sha256(content.encode()).hexdigest(),
                            source=source, created_at=now,
                            expires_at=now + timedelta(minutes=ttl_minutes) if ttl_minutes else None)
        self.memory_entries[entry_id] = entry
        return entry

    def verify_memory(self, entry_id: str, content: str) -> bool:
        entry = self.memory_entries.get(entry_id)
        if not entry or entry.quarantined:
            return False
        if entry.expires_at and datetime.now(timezone.utc) > entry.expires_at:
            return False
        return hashlib.sha256(content.encode()).hexdigest() == entry.content_hash

    def generate_report(self) -> dict:
        return {
            "tier": self.tier.value,
            "agents": {"total": len(self.agents),
                       "active": sum(1 for a in self.agents.values() if a.status == "active")},
            "privileges": {"active": len(self.privileges)},
            "memory": {"total": len(self.memory_entries),
                       "quarantined": sum(1 for m in self.memory_entries.values() if m.quarantined)}
        }
