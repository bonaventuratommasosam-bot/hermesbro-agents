# External Code Vetting Checklist

Before importing code from third-party repos (GitHub, npm, PyPI, etc.) into the production environment.

## Step 1: Static File Scan

```bash
# Count files and size
du -sh . && find . -path ./.git -prune -o -type f -print | wc -l

# Find executables and binaries
find . -path ./.git -prune -o -type f \( -name "*.exe" -o -name "*.bin" -o -name "*.dll" -o -name "*.so" -o -name "*.elf" -o -name "*.war" -o -name "*.jar" -o -name "*.wasm" \) -print

# Find shell scripts
find . -path ./.git -prune -o -type f \( -name "*.sh" -o -name "*.bash" -o -name "*.zsh" \) -print

# Count scripts by type
find . -path ./.git -prune -o -type f -name "*.py" -print | wc -l
find . -path ./.git -prune -o -type f -name "*.js" -print | wc -l
```

## Step 2: Malicious Code Patterns

```bash
# Remote execution & code injection
grep -rl --include="*.py" -E "(eval\(|exec\(|__import__|compile\()" .
grep -rl --include="*.js" -E "(eval\(|new Function|child_process|vm\.runInNewContext)" .

# Reverse shells & C2
grep -rl -E "(reverse_shell|bind_shell|nc -|ncat |bash -i|/dev/tcp|mkfifo|socat )" .

# Data exfiltration
grep -rl --include="*.py" -E "(base64\.b64encode|requests\.post.*webhook|curl.*POST|wget.*POST)" .
grep -rl --include="*.js" -E "(fetch\(.*POST|axios\.post|XMLHttpRequest)" .

# Suspicious downloads
grep -rl -E "(curl.*\|.*bash|wget.*\|.*sh|pip install.*http|npm install.*http)" .

# Obfuscation
grep -rl --include="*.py" -E "(base64\.b64decode|codecs\.decode|rot13|chr\([0-9]+\)\.join)" .
```

## Step 3: Hardcoded Secrets Check

```bash
# Look for real credentials (not placeholders)
grep -rl -E "(api_key|apikey|secret_key|password|token)\s*=\s*['\"][A-Za-z0-9]{16,}" --include="*.py" --include="*.js" --include="*.json" --include="*.yml" .

# Distinguish from env var lookups (safe) vs hardcoded values (dangerous)
# SAFE:   os.environ.get("API_KEY"), process.env.API_KEY
# DANGER: api_key = "sk-abc123..." directly in source
```

## Step 4: CI/CD, Workflow, and Plugin Metadata Inspection

```bash
# Check GitHub Actions / CI for suspicious steps
cat .github/workflows/*.yml
# Look for: curl to external URLs, wget downloads, pip install from non-PyPI,
# npm install from non-registry, arbitrary shell execution in CI steps

# Check for preinstall/postinstall hooks (npm)
cat package.json | jq '.scripts'

# Check plugin/marketplace metadata (Claude, agentskills.io, Hermes, etc.)
cat .claude-plugin/*.json 2>/dev/null
cat .hermes-plugin/*.json 2>/dev/null
# Verify: no external URLs in plugin config, version matches repo, author matches
```

## Step 5: Network Calls Review

```bash
# Find all external URLs referenced in code (not documentation)
grep -roh 'https\?://[^ "'"'"')\]]*' --include="*.py" --include="*.js" --include="*.yml" . | sort -u

# Check for suspicious domains, pastebin, ngrok, requestbin, webhook.site
grep -rl -E "(pastebin|ngrok|requestbin|webhook\.site|burpcollaborator|interact\.sh)" .
```

## Step 6: Dependency Check

```bash
# Python: review requirements.txt for typosquatting
cat requirements.txt
# Check suspicious packages: very new, very few downloads, similar names to popular packages

# Node: review package.json dependencies
cat package.json | jq '.dependencies, .devDependencies'
```

## Decision Matrix

| Finding | Severity | Action |
|---------|----------|--------|
| Binary files (.exe, .dll, .so) | HIGH | Remove unless source-proven |
| Reverse shell patterns | CRITICAL | Reject entire repo |
| Hardcoded real credentials | HIGH | Remove, report upstream |
| Obfuscated code | HIGH | Manual review required |
| Scripts with network calls | MEDIUM | Review destinations, run sandboxed |
| CI workflow with external downloads | MEDIUM | Pin versions, verify checksums |
| Shell scripts | LOW-MED | Review content before execution |
| Plain config/docs/skills (YAML/MD) | SAFE | Copy freely |

## Import Strategy

After vetting:
1. Copy knowledge files (SKILL.md, references/) — always safe if vetted
2. Copy scripts ONLY if reviewed and dependencies are acceptable
3. Skip scripts that need external services you don't have
4. Never copy `.git/`, `.env`, credential files, or CI configs into production
5. Clone shallow (`git clone --depth 1`) to `/tmp` — never into production directly
6. Clean up `/tmp` clone after copying what you need

### Knowledge-Only Import (Recommended for Skill Libraries)

When importing a large skill collection (10+ skills), copy only SKILL.md + references/:

```python
import os, shutil

SRC = "/tmp/repo/skills"
DST = "/path/to/destination"

for skill_name in SELECTED_SKILLS:
    src_path = os.path.join(SRC, skill_name)
    dst_path = os.path.join(DST, skill_name)
    if os.path.isdir(src_path):
        os.makedirs(dst_path, exist_ok=True)
        # Copy SKILL.md
        skill_md = os.path.join(src_path, "SKILL.md")
        if os.path.exists(skill_md):
            shutil.copy2(skill_md, dst_path)
        # Copy references/ (standards, workflows, deep context)
        refs = os.path.join(src_path, "references")
        if os.path.isdir(refs):
            shutil.copytree(refs, os.path.join(dst_path, "references"), dirs_exist_ok=True)
        # SKIP scripts/ — they need external deps, review individually later
```

This imports the knowledge (when to use, workflow steps, verification) while avoiding
executable code that may need unvetted dependencies. Scripts can be imported later
on a case-by-case basis after dependency review.
