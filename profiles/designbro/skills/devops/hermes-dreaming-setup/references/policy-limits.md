# Dreaming policy limits (from policy.py)

## TARGET_POLICY (per-proposal limits)
| target_kind | max_chars | max_lines | total_chars |
|-------------|-----------|-----------|-------------|
| memory      | 240       | 4         | 4000        |
| user        | 220       | 4         | 4000        |
| skill       | 900       | 24        | 12000       |
| fact        | 320       | 12        | 12000       |

## RUN_POLICY (per-run limits)
- max_changes: 3
- max_adds: 1
- max_new_chars: 250
- max_targets: 3

## Format rules
- memory/user entries MUST start with `-` (bullet)
- No double newlines within entries
- provenance: exact `path:line` format, no ranges
- target_path: relative to live_root (e.g. `user.md`, not `/root/.../user.md`)
- policy_flags: non-empty string list
- risk: low|medium|high
- priority: low|normal|high
