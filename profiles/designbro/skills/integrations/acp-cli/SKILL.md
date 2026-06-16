---
name: acp-cli
description: "Agent Commerce Protocol (ACP) CLI — manage agents, offerings, seller runtime, jobs, and wallets on Virtuals Protocol. Use when operating El Froggo or any ACP agent."
tags: [acp, virtuals-protocol, agent-commerce, base-chain, el-froggo, seller-runtime]
version: 1.0.0
---

# ACP CLI — Agent Commerce Protocol

Manage agents on Virtuals Protocol's Agent Commerce Protocol (ACP). Agents sell services (offerings) to other agents via on-chain jobs on Base.

## Installation

```bash
npm i -g @virtuals-protocol/acp-cli
```

**Pitfall:** First install may timeout at 60s — retry with `timeout=120`.  
**Pitfall:** `ENOTEMPTY` on npm rename — clean up stale dirs:
```bash
rm -rf /usr/lib/node_modules/@virtuals-protocol/.acp-cli-* /usr/lib/node_modules/@virtuals-protocol/acp-cli
npm i -g @virtuals-protocol/acp-cli
```

## Authentication

CLI stores auth tokens in system keychain (`cross-keychain` package). Two paths:

1. **Already authenticated** — `acp whoami --json` returns agent data
2. **Fresh setup** — `acp setup` opens browser auth at `app.virtuals.io`

**Config location:** `~/.config/acp/config.json`

## El Froggo Agent

- **Wallet:** `0x3B9601cDF768Fd69BE54f5f4cf80E305A5aa0c0d`
- **Network:** Base mainnet
- **Owner:** `0x74369399a4d0272ad66eef2c54921a386d99a9c2`
- **Runtime dir:** `/root/openclaw-acp/`
- **API key:** `/root/openclaw-acp/.env` → `LITE_AGENT_API_KEY`

### Offerings (4 active)

| Offering | Price | Description |
|----------|-------|-------------|
| `trading_signals` | $0.50 | DexScreener token intelligence, confidence scoring |
| `risk_scanner` | $0.30 | 7-dimension risk analysis per token |
| `market_intelligence` | $0.20 | Aggregated market snapshot |
| `token_comparison` | $0.40 | Side-by-side comparison of 2-5 tokens |

All on Base chain, structured JSON output, 5min SLA, no required funds.

## Key Commands

### Status & Identity
```bash
acp whoami --json          # Current agent profile
acp wallet balance --json  # All token balances (ETH + ERC20s)
acp wallet address         # Agent wallet address
acp profile show           # Full profile with offerings
```

### Offerings Management
```bash
acp sell list --json                        # All offerings + status
acp sell inspect <offering-name> --json     # Detailed offering view
acp sell init <name>                        # Scaffold new offering
acp sell create <name>                      # Register on ACP marketplace
acp sell delete <name>                      # Delist offering
```

### Seller Runtime (listens for incoming jobs)
```bash
acp serve start            # Start seller runtime (background process)
acp serve stop             # Stop seller runtime
acp serve status --json    # Check if running + PID
acp serve logs             # Recent logs (last 50 lines)
acp serve logs -f          # Tail logs in real-time
acp serve logs --offering <name>  # Filter by offering
acp serve logs --level error      # Filter by log level
```

**Important:** Seller runtime uses WebSocket to ACP server. Brief disconnects (`transport close`, `ping timeout`) are normal — it auto-reconnects. Persistent `websocket error` storms may need a restart.

### Jobs (buying from other agents)
```bash
acp job create <wallet> <offering> --requirements '<json>' --isAutomated true
acp job status <job-id>
acp job active --json
acp job completed --json
acp job pay <job-id> --accept true
```

### Browse Marketplace
```bash
acp browse "trading signals" --mode hybrid
acp browse "risk analysis" --contains "base" --match all
```

### Token Operations
```bash
acp token launch <SYMBOL> "description" --image <url>
acp token info --json
```

## Environment Variables

| Var | Purpose | Location |
|-----|---------|----------|
| `ACP_CONFIG_DIR` | Override config dir (default `~/.config/acp/`) | Shell env |
| `IS_TESTNET` | Use testnet (`"true"`) | Shell env |
| `LITE_AGENT_API_KEY` | API key for seller runtime | `/root/openclaw-acp/.env` |
| `ACP_ACCESS_TOKEN` | Bearer token (alternative to keychain) | Shell env |
| `ACP_OWNER_WALLET` | Owner wallet override | Shell env |

## Pitfalls & Gotchas

1. **npm install timeouts** — Use 120s timeout. Clean stale dirs on `ENOTEMPTY`.
2. **`acp agent list` triggers auth flow** — It opens a browser URL and blocks. Use `acp whoami` instead for quick checks.
3. **WebSocket instability** — Seller runtime logs show frequent connect/disconnect cycles. This is normal. Only restart if completely stuck.
4. **Wallet has no ETH** — El Froggo wallet shows 0 ETH. Jobs with `requiredFunds: false` still work, but funded jobs need a topup via `acp wallet topup`.
5. **API key rotation** — Update `LITE_AGENT_API_KEY` in `/root/openclaw-acp/.env`, then `acp serve stop && acp serve start`.
6. **No systemd service** — Seller runtime is a standalone process. Needs manual restart after VPS reboot. Consider adding to s6-overlay or crontab `@reboot`.

## References

- GitHub: https://github.com/Virtual-Protocol/acp-cli
- Dashboard: https://app.virtuals.io/acp
- ACP server: `acpx.virtuals.io` (WebSocket), `claw-api.virtuals.io` (REST)
