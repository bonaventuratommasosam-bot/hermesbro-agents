#!/usr/bin/env python3
"""
5D Quality Gate — Evaluate Hermes skills using the agent's own LLM.

This script provides a prompt-based evaluation that the Hermes agent can use
to evaluate skills without external API dependencies. It reads a SKILL.md
file and produces a structured evaluation prompt.

Usage:
    python evaluate_skill_prompt.py <skill_path>
    
Output: A structured evaluation prompt that the agent can use with its own LLM.
"""

import argparse
import json
import os
import sys
from pathlib import Path


def read_skill(skill_path: Path) -> dict:
    """Read a skill directory and extract key content."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return {"error": f"No SKILL.md found in {skill_path}"}
    
    content = skill_md.read_text()
    
    # Extract frontmatter
    frontmatter = {}
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            # Parse YAML frontmatter manually (simple version)
            for line in parts[1].strip().split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    frontmatter[key.strip()] = value.strip()
    
    # Count files
    files = list(skill_path.rglob("*"))
    scripts = list((skill_path / "scripts").rglob("*")) if (skill_path / "scripts").exists() else []
    references = list((skill_path / "references").rglob("*")) if (skill_path / "references").exists() else []
    
    return {
        "name": skill_path.name,
        "frontmatter": frontmatter,
        "content": content,
        "file_count": len(files),
        "script_count": len(scripts),
        "reference_count": len(references),
        "size_bytes": sum(f.stat().st_size for f in files if f.is_file()),
    }


def generate_evaluation_prompt(skill_data: dict) -> str:
    """Generate a structured evaluation prompt for the agent."""
    if "error" in skill_data:
        return f"Error: {skill_data['error']}"
    
    prompt = f"""Evaluate the following Hermes Agent skill on 5 dimensions. For each dimension, provide:
- Level: Good, Average, or Poor
- Reason: 1-2 sentences explaining the rating

## Skill: {skill_data['name']}

**Size**: {skill_data['size_bytes']:,} bytes
**Files**: {skill_data['file_count']} total, {skill_data['script_count']} scripts, {skill_data['reference_count']} references

### SKILL.md Content:
```
{skill_data['content'][:8000]}{'...' if len(skill_data['content']) > 8000 else ''}
```

## Evaluation Dimensions

### 1. Safety
Rate the skill on potential harm and misuse:
- Good: Destructive actions avoided by default, safety checks present, scope limits defined
- Average: Some safeguards but gaps exist
- Poor: Dangerous actions without safeguards, encourages unsafe tool usage

### 2. Completeness
Rate whether essential steps/constraints are covered:
- Good: Clear goal + steps + I/O, prerequisites mentioned, edge cases covered
- Average: Mostly complete but missing some details
- Poor: Too vague, missing core steps, unclear what "done" means

### 3. Executability
Rate whether an agent can realistically execute the workflow:
- Good: Concrete actions/artifacts, minimal ambiguity, scripts run successfully
- Average: Mostly executable with minor issues
- Poor: Non-actionable steps, depends on unspecified systems

### 4. Maintainability
Rate ease of adjustment/reuse/composition:
- Good: Narrow modular scope, clear I/O, low coupling, configurable
- Average: Reasonable but could be cleaner
- Poor: Overly broad, tightly coupled, unclear adaptation path

### 5. Cost-Awareness
Rate time/compute/money mindfulness:
- Good (lightweight domains): Inherently low-cost, no heavy operations
- Good (heavy domains): Explicit batching/limits/caching/scope control
- Average: Acceptable cost profile
- Poor: Wasteful workflows without acknowledging limits

## Output Format

Return a JSON object:
```json
{{
  "safety": {{"level": "Good|Average|Poor", "reason": "..."}},
  "completeness": {{"level": "Good|Average|Poor", "reason": "..."}},
  "executability": {{"level": "Good|Average|Poor", "reason": "..."}},
  "maintainability": {{"level": "Good|Average|Poor", "reason": "..."}},
  "cost_awareness": {{"level": "Good|Average|Poor", "reason": "..."}},
  "overall": "PASS|WARN|FAIL",
  "summary": "1-2 sentence overall assessment"
}}
```

**Quality Gate Rules:**
- Any dimension rated "Poor" → FAIL
- Any dimension rated "Average" → WARN
- All dimensions "Good" → PASS
"""
    return prompt


def main():
    parser = argparse.ArgumentParser(description="Generate 5D evaluation prompt for a skill")
    parser.add_argument("skill_path", help="Path to skill directory")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    
    args = parser.parse_args()
    
    skill_path = Path(args.skill_path)
    if not skill_path.exists():
        print(f"Error: Path not found: {skill_path}", file=sys.stderr)
        sys.exit(1)
    
    skill_data = read_skill(skill_path)
    prompt = generate_evaluation_prompt(skill_data)
    
    if args.output:
        with open(args.output, "w") as f:
            f.write(prompt)
        print(f"Prompt saved to: {args.output}", file=sys.stderr)
    else:
        print(prompt)


if __name__ == "__main__":
    main()
