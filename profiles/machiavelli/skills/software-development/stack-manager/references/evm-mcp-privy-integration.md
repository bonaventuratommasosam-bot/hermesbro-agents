# EVM MCP Server + Privy Wallet Integration

## Pattern

When configuring blockchain/wallet MCP servers for Hermes profiles, the `@mcpdotdirect/evm-mcp-server` provides 22 tools across 60+ EVM chains (Base, Ethereum, Polygon, etc.).

## Configuration

Add to `config.yaml` on the target profile(s):

```yaml
mcp_servers:
  evm:
    command: "npx"
    args: ["-y", "@mcpdotdirect/evm-mcp-server"]
    env:
      EVM_DEFAULT_CHAIN: "base"
    timeout: 60
    connect_timeout: 30
```

For write operations (transfers, swaps), add the wallet private key:
```yaml
    env:
      EVM_DEFAULT_CHAIN: "base"
      EVM_PRIVATE_KEY: "<PRIVATE_KEY_PLACEHOLDER>"
```

## Privy Custodial Wallets (Read-Only Mode)

The wallet is on **Privy** (custodial MPC wallet) — there is NO raw private key to extract.

**What works in read-only (no EVM_PRIVATE_KEY):**
- Balance checking (`get_balance`)
- Transaction history
- Token holdings
- Contract reads (view/pure functions)
- Block/transaction data
- ENS resolution

**What does NOT work without a private key:**
- Native token transfers
- ERC20/721/1155 transfers
- Contract writes
- Message signing

**For write operations**, use Privy's API directly (credentials in el-froggo `.env`):
- `PRIVY_APP_ID`, `PRIVY_APP_SECRET`, `PRIVY_AUTH_KEY`
- `PRIVY_WALLET_ID`, `PRIVY_WALLET_ADDRESS`
- `PRIVY_CHAIN=base`

## Current Setup

- **Profile:** el-froggo only (EVM + RootEdge MCP). GribbitO does NOT have MCP servers — domain tools go to domain bots.
- **Chain:** Base
- **Wallet:** `<WALLET_ADDRESS>` (Privy, shared)
- **Mode:** Read-only (no private key in MCP env)
- **MCP servers on el-froggo:**
  - `evm` — `@mcpdotdirect/evm-mcp-server` (balance, tx, contract reads)
  - `rootedge` — `https://app.rootedge.ai/api/mcp` (DEX search, trending, news, Fear & Greed, Hyperliquid)
- **Prerequisite:** `pip install mcp --break-system-packages` (PEP 668 on Debian)

## Pitfalls

- **MCP servers go to domain bots, NOT GribbitO.** RootEdge (crypto/DEX) → El Froggo. Don't add domain-specific MCP to the orchestrator.
- **MCP servers are discovered at startup only.** Adding `mcp_servers` to config.yaml requires a gateway restart — no hot-reload.
- **Multi-profile config:** Each profile's `config.yaml` needs its own `mcp_servers` block. They are independent.
- **Privy wallets have no raw private key.** Don't ask the user for one — check `.env` for `PRIVY_*` vars first.
- **npm install on first run:** `npx -y` downloads the package on first invocation. This can be slow (30-60s). Set `connect_timeout: 30` to avoid premature failure.
- **Node.js required:** The EVM MCP server is a Node.js package. Ensure `npx` is available on the system.
