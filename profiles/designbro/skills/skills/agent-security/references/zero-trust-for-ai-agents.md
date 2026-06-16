# Zero Trust for AI Agents — Anthropic eBook (2026-05-18)

Source: https://cdn.prod.website-files.com/6889473510b50328dbb70ae6/6a1611a04085d7cd3dadc924_Claude-eBook-Zero-Trust-for-AI-Agents-05182026.pdf

36-page guide from Anthropic on applying Zero Trust principles to agentic AI deployments.

## Three Core Principles

1. **Never trust, always verify** — Every access request authenticated regardless of origin
2. **Assume breach** — Design for compromise, limit damage, segment by identity
3. **Least privilege** — Minimum access necessary for specific task

## New Agentic Concepts

- **Blast radius** — Potential damage if agent is compromised. Match security investment to exposure.
- **Least agency** (OWASP term) — Extends least privilege to agent tools: restrict WHAT each tool can do, HOW OFTEN, and WHERE
- **Memory-based privilege retention** — Cached credentials across sessions enable privilege escalation

## Threat Landscape (OWASP)

### Prompt Injection
- **Direct**: Explicit instruction overrides, Base64/hex encoding, adversarial suffixes
- **Indirect**: Malicious instructions in external data sources (web pages, emails). LLMs cannot reliably distinguish informational context from actionable instructions

### Tool & Resource Misuse
- **Tool poisoning**: Compromised MCP tool descriptors/schemas/metadata
- **Rug pull attacks**: Legitimate tool secretly replaced after approval
- **Tool shadowing**: Attacker registers tools with same interface as legitimate ones

### Privilege Escalation
- **Unscoped privilege inheritance**: Manager agent delegates without least-privilege scoping
- **Confused deputy**: Low-privilege agent relays valid-looking instructions to high-privilege agent
- **Memory-based privilege retention**: Cached credentials reused across sessions without segmentation

### Supply Chain
- **Model poisoning**: 250 malicious documents can backdoor LLMs (600M-13B params), persists through RLHF
- **RAG poisoning**: Malicious data in vector databases
- **Shared context poisoning**: Exploits reused contexts in multi-tenant environments

## Three-Tier Framework

### Foundation (Entry Level)
- Unique cryptographic identifiers per agent instance
- Short-lived tokens from identity provider (minutes, not days)
- Static least-privilege roles per agent function
- Basic sandboxed execution
- Comprehensive logs with timestamps
- Manual behavior pattern definition
- Alerting to security teams

### Enterprise (Target for Most)
- Certificate-based authentication (X.509) with lifecycle management
- mTLS with automatic rotation
- Dynamic privilege adjustment based on task requirements
- Sandbox with filesystem/network isolation
- OpenTelemetry end-to-end tracing
- Automated baseline learning
- Automatic containment (session termination, credential revocation)

### Advanced (High-Stakes Environments)
- Hardware-backed identity (HSM/TPM) with remote attestation
- Continuous authorization with real-time policy evaluation
- Just-In-Time (JIT) / Just-Enough-Administration (JEA) with auto-expiration
- Hardware isolation (confidential computing enclaves)
- Decision explainability for compliance
- Continuous baseline refinement with drift detection
- Orchestrated SOAR playbooks with graduated escalation

## Implementation Workflow (7 Phases)

### Phase 1: Identify Requirements
- Regulatory requirements (HIPAA, FINRA, GDPR, FedRAMP, EU AI Act)
- Operational goals and constraints
- Align security, legal, compliance, business stakeholders

### Phase 2: Manage Supply Chain
- **AI-BOM** (AI Bill of Materials): Track model provenance, training data lineage, fine-tuning parameters
- **OpenSSF Scorecard**: Auto-score dependencies on branch protection, fuzzing, signed releases, maintainer activity
- **Cryptographic signing**: Sign models/software at every stage, verify at runtime
- **Vendor assessments**: Ask suppliers how they prepare for AI-accelerated exploit timelines

### Phase 3: Define Agent Boundaries
- Unique cryptographically rooted identifier per agent
- Approved/prohibited actions lists
- Escalation triggers for human review
- Scope limits (Least Agency + deny-by-default)
- Blast radius analysis using "impossible vs tedious" test

### Phase 4: Protect Input/Output
- Input sanitization against injection
- Output filtering for sensitive data patterns
- Semantic analysis of outputs (not just pattern matching)
- Human-in-the-loop for high-risk actions

### Phase 5: Secure Tool Access
- **Tool allow-listing**: Explicit approved tools per agent function, deny-by-default
- **Capability restrictions**: Limit what permitted tools can do (read-only, no send/delete)
- **Sandboxing**: Filesystem and network isolation per tool
- **Approval escalation**: High-risk tool invocations pause for human review
- Tool authentication: Certificate-based or short-lived tokens (NEVER static API keys)

### Phase 6: Protect Agent Credentials
- Short-lived, identity-provider-issued credentials as baseline
- Certificate-based identity with CA enrollment
- Credential isolation: Unique credentials per agent instance
- Inject credentials at runtime from secrets management (never in code/config)
- **JIT access**: Grant only when needed, revoke immediately after use

### Phase 7: Safeguard Agent Memory
- **Memory isolation**: Strict boundaries between sessions and users
- **Context integrity validation**: Cryptographic hashes detect unauthorized modification
- **Retention policies**: TTL on sensitive context, auto-expire unverified memory
- Source attribution for each memory element
- Store hashes in tamper-resistant logs separate from content

## Key Metrics

- **Dwell time**: Anomaly occurrence → human awareness (target: <1 hour for critical systems)
- **Coverage**: Fraction of alerts that get investigated
- **Detection speed**: How quickly team becomes aware of unexpected behavior
- **Behavioral conformance**: Alignment with intended policies and expected patterns

## Defensive Operations

### Autonomous Defense
- Automate evidence collection, enrichment, correlation, documentation
- Keep humans on containment calls, disclosure calls, customer-comms calls
- Put a model at the front of your alert queue (structured disposition before human sees it)

### Practical Start
Pick one noisy rule with known-high false positive rate → wire frontier model with read-only SIEM access → measure agreement against human reviewer for 2 weeks → expand if tolerable

### Tabletop Exercises
Run for 5 simultaneous incidents, not 1. Intake, triage, remediation tracking must scale.

### Emergency Changes
Two-week change-approval cycle is itself a security risk. Decide in advance who can authorize, how fast, what evidence required.

## Claude Code Security Features (from doc)

- Deny-by-default permissions requiring explicit approval
- Sandboxed execution with OS-level filesystem/network isolation
- OpenTelemetry metrics for tracking/audit
- Command injection detection
- Input sanitization and command blocklist
- Isolated context windows for web content
- OS credential store (not config files) for API credentials
- Ephemeral sub-agents with isolated context windows
- Managed settings for organization-wide policy enforcement

## Key Quote

> "The organizations best positioned for this shift will not necessarily be the ones with the most advanced AI. They will be the ones whose fundamentals are strong enough that AI-assisted scanning finds fewer bugs in the first place, and whose agent deployments were architected for breach from day one."
