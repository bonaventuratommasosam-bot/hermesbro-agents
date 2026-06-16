# Cross-Profile Skill Deployment

Deploy skills to other Hermes profiles from your current session.

## Pattern

When the user asks to add a skill to another profile (e.g., "add this to Sentinel and Machiavelli"):

### 1. Copy the files via terminal
```bash
mkdir -p <HERMES_ROOT>/profiles/<target>/skills/
cp -r /path/to/skill <HERMES_ROOT>/profiles/<target>/skills/<skill-name>
```

### 2. Create SKILL.md with cross_profile=True
```python
write_file(
    path="<HERMES_ROOT>/profiles/<target>/skills/<skill-name>/SKILL.md",
    content="...",
    cross_profile=True  # Required for cross-profile writes
)
```

### 3. Verify the deployment
```bash
ls -la <HERMES_ROOT>/profiles/<target>/skills/<skill-name>/
```

## Important Notes

- **cross_profile=True** is required when writing to another profile's skills directory
- The cross-profile guard is a soft guard — terminal tool can bypass it
- Always verify the deployment worked by listing the files
- Test the skill from the target profile if possible

## Example: Deploying to Sentinel and Machiavelli

```bash
# Copy to both profiles
cp -r /home/[REDACTED — dati personali rimossi]/ai-stack/agents/sentinel/zero_trust \
      <HERMES_ROOT>/profiles/sentinel/skills/zero-trust
cp -r /home/[REDACTED — dati personali rimossi]/ai-stack/agents/sentinel/zero_trust \
      <HERMES_ROOT>/profiles/machiavelli/skills/zero-trust

# Create SKILL.md for each (with cross_profile=True)
write_file(
    path="<HERMES_ROOT>/profiles/sentinel/skills/zero-trust/SKILL.md",
    content=skill_md_content,
    cross_profile=True
)
write_file(
    path="<HERMES_ROOT>/profiles/machiavelli/skills/zero-trust/SKILL.md",
    content=skill_md_content,
    cross_profile=True
)
```

## Profiles

Known profiles and their purposes:
- **gribbito** — Main agent (current session)
- **sentinel** — Security monitoring
- **machiavelli** — Strategic operations
- **contabile** — Financial management
- **lawrenzo** — Legal operations
- **groot** — Infrastructure management
- **wannabe** — Marketing operations
- **designbro** — Design operations
- **el-froggo** — Social media
- **ducato** — Vehicle management
