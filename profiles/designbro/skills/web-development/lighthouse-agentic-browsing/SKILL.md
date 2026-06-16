---
name: lighthouse-agentic-browsing
description: "Audit websites for AI agent readiness using Lighthouse's Agentic Browsing category — WebMCP integration, llms.txt discoverability, agent accessibility, layout stability."
version: 1.0.0
author: gribbito
license: internal
metadata:
  hermes:
    tags: [lighthouse, ai-agents, webmcp, llms-txt, accessibility, auditing, google]
    homepage: https://developer.chrome.com/docs/lighthouse/agentic-browsing
---

# Lighthouse Agentic Browsing Audits

Google's new experimental Lighthouse category that evaluates how well a site is constructed for AI agent interaction. Announced at Google I/O 2026.

Use this skill when:
- Auditing a website for AI agent readiness
- Improving a site so bots/agents can interact with it
- Adding WebMCP, llms.txt, or agent accessibility to a site
- Running Lighthouse in CI/CD for agentic readiness

## What It Is

A new Lighthouse category (alongside Performance, SEO, Accessibility, Best Practices) with **deterministic audits** — no LLM scoring, no randomness. Suitable for CI/CD.

Unlike other categories, there's **no 0-100 score**. Instead:
- **Fractional score** — ratio of passed checks (e.g. 3/7)
- **Pass/Fail** per audit
- **Informational counts** for quick progress view

**Status: Experimental.** Based on proposed standards, not finalized specs.

## The 4 Audit Areas

### 1. WebMCP Integration

WebMCP (Model Context Protocol for Web) lets sites explicitly expose logic and forms to AI agents via a standardized API.

**Audits:**
- `Registered Web MCP tools` — site has registered tool definitions
- `Forms missing declarative Web MCP` — interactive forms should be declaratively exposed
- `Web MCP schema validity` — registered tool schemas are valid JSON

**How to implement:**
- **Declarative** — define tools in HTML markup (preferred)
- **Imperative** — register tools via JavaScript API
- Lighthouse monitors CDP's WebMCP domain for registration events

**Pitfall:** Imperative (JS) registrations depend on timing. If the tool registers late, Lighthouse may miss it during the snapshot. Prefer declarative where possible.

### 2. Discoverability

**Audits:**
- `llms.txt` — checks for a machine-readable summary at the domain root

**What is `llms.txt`?**
A file at `https://example.com/llms.txt` — like `robots.txt` but for AI. Contains a structured summary of what the site does, its key pages, and how agents should interact with it.

**Format** (emerging convention):
```
# Site Name

> One-line description

## Key Pages
- [Page Name](https://example.com/page): Description

## API Endpoints
- POST /api/action: Description

## Notes for AI Agents
- Authentication required for X
- Rate limits: Y requests/minute
```

### 3. Accessibility for Agents

**NOT the same as traditional a11y.** Traditional accessibility is for screen readers. Agent accessibility is for machine interaction.

**Audits:**
- `Accessibility for agents` — checks agent-critical a11y properties

**What agents need:**
- **Names and labels** — every interactive element has a programmatic name
- **Tree integrity** — roles and parent-child relationships are valid
- **Visibility** — content not hidden from a11y tree while being interactive

**Implementation:** Use semantic HTML + proper ARIA. The a11y tree is the "machine-eye view" of your page.

### 4. Layout Stability

**Audits:**
- `Layout stability` — CLS measured from agent perspective

**Why it matters:** If elements move while an agent tries to click them, interactions fail. Agents rely on element positioning, not visual recognition.

**Fix:** Set explicit dimensions on images/ads, avoid late content injection, minimize layout shifts.

## Running the Audit

```bash
# Install Lighthouse (if not already)
npm install -g lighthouse

# Run agentic browsing category
lighthouse https://example.com --only-categories=agentic-browsing --output=json --output-path=report.json

# In CI/CD
lighthouse https://example.com --only-categories=agentic-browsing --chrome-flags="--headless" --output=json
```

**Pitfall:** The `agentic-browsing` category may not be available in older Lighthouse versions. It was added in the v0.15.0 era (May 2026). Check `lighthouse --version` and update if needed.

## For [REDACTED — dati personali rimossi]'s Bots

When building dashboards, landing pages, or client-facing tools for Hermes Bots (Ratatouille, ContAIbile, LAWrenzo, Wannabe):
- Add `llms.txt` to every site — cheap, high signal
- Use semantic HTML — helps both humans and agents
- Consider WebMCP for exposing bot-specific actions
- Run Lighthouse agentic audits in CI

## References

- [Lighthouse Agentic Browsing Scoring](https://developer.chrome.com/docs/lighthouse/agentic-browsing/scoring)
- [WebMCP Integration](https://developer.chrome.com/docs/lighthouse/agentic-browsing/registered-web-mcp-tools)
- [llms.txt audit](https://developer.chrome.com/docs/lighthouse/agentic-browsing/llms-txt)
- [Agent Accessibility](https://developer.chrome.com/docs/lighthouse/agentic-browsing/accessibility-for-agents)
- [Layout Stability](https://developer.chrome.com/docs/lighthouse/agentic-browsing/layout-stability)
