# Hermes Desktop

Native desktop app for Hermes Agent — install, configure, and chat with a GUI.

## Overview

Instead of managing the CLI by hand, Hermes Desktop walks through install, provider setup, and day-to-day usage in one place. Uses the official Hermes install script, stores Hermes in `~/.hermes`, and gives you a GUI for chat, sessions, profiles, memory, skills, tools, scheduling, messaging gateways, and more.

## Features

- **Guided first-run install** — Progress tracking and dependency resolution
- **Local or remote backend** — Run locally on `127.0.0.1:8642`, or connect to remote API server
- **Multi-provider support** — OpenRouter, Anthropic, OpenAI, Google, xAI, Nous, Qwen, MiniMax, HF, Groq, local endpoints
- **Streaming chat UI** — SSE streaming, tool progress, markdown, syntax highlighting
- **Token usage tracking** — Live prompt/completion token counts and cost display
- **22 slash commands** — /new, /clear, /fast, /web, /image, /browse, /code, /shell, /usage, etc.
- **Session management** — Full-text search (SQLite FTS5), date-grouped history
- **Profile switching** — Create, delete, switch between separate environments
- **14 toolsets** — web, browser, terminal, file, code execution, vision, image gen, TTS, skills, memory, session search, clarify, delegation, MoA, task planning
- **Memory system** — View/edit, user profile, capacity tracking, memory providers
- **Persona editor** — Edit/reset SOUL.md
- **Saved models** — CRUD per configurazioni modello
- **Scheduled tasks** — Cron job builder con 15 delivery targets
- **16 messaging gateways** — Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Mattermost, Email, SMS, iMessage, DingTalk, Feishu, WeCom, WeChat, Webhooks, Home Assistant
- **Hermes Office (Claw3d)** — Interfaccia 3D visuale
- **Backup & debug** — Backup/restore completo e diagnostica
- **Auto-updater** — Aggiornamenti automatici via electron-updater
- **i18n ready** — Framework internazionalizzazione

## Tech Stack

- **Electron 39** — Shell desktop cross-platform
- **React 19** — UI framework
- **TypeScript 5.9** — Type safety
- **Tailwind CSS 4** — Styling
- **Vite 7 + electron-vite** — Dev server e build
- **better-sqlite3** — Storage locale con FTS5
- **i18next** — Internazionalizzazione
- **Vitest** — Test runner

## Supported Providers

### LLM Providers
- OpenRouter (200+ models)
- Anthropic (Claude)
- OpenAI (GPT)
- Google (Gemini)
- xAI (Grok)
- Nous Portal
- Qwen
- MiniMax
- Hugging Face (20+ models)
- Groq
- Local/Custom (LM Studio, Atomic Chat, Ollama, vLLM, llama.cpp)

### Messaging Platforms
Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Mattermost, Email (IMAP/SMTP), SMS (Twilio/Vonage), iMessage (BlueBubbles), DingTalk, Feishu/Lark, WeCom, WeChat (iLink Bot), Webhooks, Home Assistant

### Tool Integrations
Exa Search, Parallel API, Tavily, Firecrawl, FAL.ai, Honcho, Browserbase, Weights & Biases, Tinker

## Development

```bash
npm install
npm run dev          # Start dev
npm run lint         # Lint
npm run typecheck    # Type check
npm run test         # Tests
npm run build        # Build
npm run build:mac    # macOS
npm run build:win    # Windows
npm run build:linux  # Linux
npm run build:rpm    # Fedora/RHEL
```

## Links

- **GitHub**: https://github.com/fathah/hermes-desktop
- **Core Agent**: https://github.com/NousResearch/hermes-agent
- **Stars**: 8.7k
- **Forks**: 1.1k

## Notes

- The project is in active development — features may change
- Windows installer is not code-signed (SmartScreen warning on first launch)
- Fedora .rpm is not GPG-signed
- Auto-update not supported for .rpm builds (reinstall new .rpm to update)
