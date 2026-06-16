# Eval Loop — Quality Gate for Agent Outputs

Source: "How To Fix AI Slop (Using Hermes)" by Machina (@EXM7777 on X)
Reference: weeklyaiops.com, t.me/aifirstbrain

## Core Insight

AI slop is an output-side problem, not an input-side problem. Better prompts/models/instructions/memory won't fix it. The fix is an eval loop that scores output against a gold standard BEFORE shipping.

## 6-Step Eval Loop

### 1. Connect Hermes to Telegram (or any messenger with approval buttons)
- Enables human-in-the-loop gating
- Telegram supports inline buttons for approve/reject/edit

### 2. Build gold standards
- 20-50 best pieces of output (emails, copy, landing pages, code patterns)
- Stored in memory so judge LLM can reference them
- Maps to: `gold-examples.md` in Shared Knowledge

### 3. Create a rubric → judge skill
- LLM-as-a-judge pattern: use a separate model to score outputs
- Output: 0-1 score + reasoning
- Stored as a Hermes skill (e.g., `judge-output`)
- Rubric dimensions: tone match, factual accuracy, completeness, brand voice

### 4. Build a test suite
- Known inputs → expected quality threshold
- Not a spreadsheet — a Hermes skill with test cases
- Run against any prompt/template change before deploying

### 5. Regression test + approval gate
- Every change to prompts/skills/templates goes through the test suite
- Telegram approval button for borderline scores (e.g., 0.7-0.9)
- Auto-approve above threshold, auto-reject below

### 6. Monitor production with feedback loop
- Cron job samples recent outputs
- Scores them against rubric
- Alerts on quality degradation
- Logs to `feedback.md` for trend tracking

## Mapping to Knowledge Maturity Model

| Knowledge Area | Eval Loop Step |
|---|---|
| 3. Gold examples | Step 2 (gold standards) |
| 8. Feedback loops | Step 6 (production monitoring) |
| Skills (SOPs) | Step 3 (judge skill) + Step 4 (test suite) |

## Implementation Status (as of 2026-06-07)

- Steps 1-2: ✅ Infrastructure exists (Telegram bots, gold-examples.md)
- Steps 3-4: ❌ No judge skill or test suite yet
- Steps 5-6: ❌ No regression pipeline or production monitoring

## Next Action

Build a `judge-output` skill that:
1. Takes an output + category as input
2. Loads gold examples for that category from gold-examples.md
3. Scores 0-1 on: tone, accuracy, completeness, brand voice
4. Returns structured JSON: {score, reasoning, suggestions}
5. Can be called from any bot's workflow before shipping
