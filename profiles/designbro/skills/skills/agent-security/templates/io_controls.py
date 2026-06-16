#!/usr/bin/env python3
"""
I/O Controls Template
Input sanitization and output filtering for Zero Trust.

Usage:
    from io_controls import get_io_controls
    
    controls = get_io_controls()
    threats = controls.scan_input("ignore previous instructions")
    sanitized, threats = controls.sanitize_input(user_input)
    redacted, threats = controls.redact_output(agent_output)

Detects: prompt injection, credential leaks, PII exposure, command injection
"""

import re
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Optional

logger = logging.getLogger("io-controls")


class ThreatType(Enum):
    PROMPT_INJECTION = "prompt_injection"
    DATA_EXFILTRATION = "data_exfiltration"
    CREDENTIAL_LEAK = "credential_leak"
    PII_EXPOSURE = "pii_exposure"
    COMMAND_INJECTION = "command_injection"
    ENCODED_BYPASS = "encoded_bypass"


@dataclass
class ThreatDetection:
    threat_type: ThreatType
    severity: str
    description: str
    location: str
    matched_pattern: str
    recommendation: str


class IOControls:
    def __init__(self):
        self.injection_patterns = [
            # Direct instruction overrides
            (r"ignore\s+(previous|all|above)\s+(instructions?|prompts?|rules?)", "HIGH"),
            (r"disregard\s+(previous|all|above)\s+(instructions?|prompts?|rules?)", "HIGH"),
            (r"forget\s+(previous|all|above)\s+(instructions?|prompts?|rules?)", "HIGH"),
            (r"new\s+instructions?\s*:", "HIGH"),
            (r"system\s*:\s*", "MEDIUM"),
            # Role manipulation
            (r"you\s+are\s+now\s+", "HIGH"),
            (r"act\s+as\s+if\s+you\s+are", "HIGH"),
            (r"pretend\s+to\s+be", "HIGH"),
            # Extraction attempts
            (r"what\s+(are|is)\s+your\s+(instructions?|prompts?|rules?|system\s+prompt)", "HIGH"),
            (r"reveal\s+your\s+(instructions?|prompts?|rules?|system\s+prompt)", "HIGH"),
            (r"show\s+me\s+your\s+(instructions?|prompts?|rules?|system\s+prompt)", "HIGH"),
            # Encoded instructions
            (r"base64\s*:\s*[A-Za-z0-9+/=]{20,}", "HIGH"),
            (r"hex\s*:\s*[0-9a-fA-F]{20,}", "MEDIUM"),
            # Delimiter confusion
            (r"```\s*system", "HIGH"),
            (r"<\|im_start\|>", "HIGH"),
            (r"\[INST\]", "HIGH"),
        ]
        
        self.credential_patterns = [
            (r"sk-[a-zA-Z0-9]{20,}", "OpenAI API Key"),
            (r"sk-ant-[a-zA-Z0-9]{20,}", "Anthropic API Key"),
            (r"nvapi-[a-zA-Z0-9]{20,}", "NVIDIA API Key"),
            (r"ghp_[a-zA-Z0-9]{36}", "GitHub PAT"),
            (r"AKIA[0-9A-Z]{16}", "AWS Access Key"),
            (r"password\s*[=:]\s*\S+", "Password"),
            (r"secret\s*[=:]\s*\S+", "Secret"),
            (r"private_key\s*[=:]\s*-----BEGIN", "Private Key"),
        ]
        
        self.pii_patterns = [
            (r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "Email"),
            (r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", "Phone"),
            (r"\b\d{3}-\d{2}-\d{4}\b", "SSN"),
            (r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b", "Credit Card"),
        ]
        
        self.command_patterns = [
            (r";\s*(rm|del|format|shutdown|reboot)", "Dangerous Command"),
            (r"\|\s*(rm|del|format|shutdown|reboot)", "Dangerous Command"),
            (r"`[^`]*`", "Command Substitution"),
            (r"\$\([^)]*\)", "Command Substitution"),
            (r"curl\s+.*\|\s*(bash|sh)", "Pipe to Shell"),
        ]

    def scan_input(self, text: str) -> list[ThreatDetection]:
        threats = []
        for pattern, severity in self.injection_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                threats.append(ThreatDetection(
                    threat_type=ThreatType.PROMPT_INJECTION, severity=severity,
                    description="Prompt injection attempt", location="input",
                    matched_pattern=match.group(), recommendation="Block or sanitize"
                ))
        for pattern, desc in self.command_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                threats.append(ThreatDetection(
                    threat_type=ThreatType.COMMAND_INJECTION, severity="HIGH",
                    description=f"{desc} detected", location="input",
                    matched_pattern=match.group(), recommendation="Sanitize command"
                ))
        return threats

    def scan_output(self, text: str) -> list[ThreatDetection]:
        threats = []
        for pattern, desc in self.credential_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                threats.append(ThreatDetection(
                    threat_type=ThreatType.CREDENTIAL_LEAK, severity="CRITICAL",
                    description=f"{desc} in output", location="output",
                    matched_pattern=match.group()[:20] + "...",
                    recommendation="Redact immediately"
                ))
        for pattern, desc in self.pii_patterns:
            for match in re.finditer(pattern, text):
                threats.append(ThreatDetection(
                    threat_type=ThreatType.PII_EXPOSURE, severity="HIGH",
                    description=f"{desc} in output", location="output",
                    matched_pattern=match.group()[:20] + "...",
                    recommendation="Redact PII"
                ))
        return threats

    def sanitize_input(self, text: str) -> tuple[str, list[ThreatDetection]]:
        threats = self.scan_input(text)
        sanitized = text
        for t in threats:
            if t.threat_type == ThreatType.PROMPT_INJECTION:
                sanitized = sanitized.replace(t.matched_pattern, "[REDACTED]")
        return sanitized, threats

    def redact_output(self, text: str) -> tuple[str, list[ThreatDetection]]:
        threats = self.scan_output(text)
        redacted = text
        for pattern, desc in self.credential_patterns:
            redacted = re.sub(pattern, f"[REDACTED: {desc}]", redacted, flags=re.IGNORECASE)
        for pattern, desc in self.pii_patterns:
            redacted = re.sub(pattern, f"[REDACTED: {desc}]", redacted)
        return redacted, threats


_io_controls: Optional[IOControls] = None

def get_io_controls() -> IOControls:
    global _io_controls
    if _io_controls is None:
        _io_controls = IOControls()
    return _io_controls
