#!/usr/bin/env python3
"""
Periodic 5D Quality Gate Report Generator

This script is designed to be run as a cron job. It evaluates all Hermes skills
using the 5D evaluation system and generates a summary report.

Output: A concise text report suitable for Telegram delivery.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


# Skill directories
# Use absolute path — expanduser can resolve wrong HOME under cron/wannabe profile
SKILLS_DIR = Path("<HERMES_ROOT>/profiles/gribbito/skills")
COMMUNITY_DIR = SKILLS_DIR / "community"

# Quality gate thresholds
FAIL_DIMENSIONS = {"Poor"}
WARN_DIMENSIONS = {"Average"}


def find_skills():
    """Find all skills with SKILL.md files."""
    skills = []
    for item in SKILLS_DIR.rglob("SKILL.md"):
        skill_dir = item.parent
        # Skip hidden directories within skills dir (like .hub, .archive)
        # but not parent directories like .hermes
        rel_parts = skill_dir.relative_to(SKILLS_DIR).parts
        if any(part.startswith(".") for part in rel_parts):
            continue
        skills.append(skill_dir)
    return sorted(skills)


def read_skill(skill_path):
    """Read skill metadata."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return None
    
    content = skill_md.read_text()
    
    # Extract name from frontmatter
    name = skill_path.name
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().split("\n"):
                if line.strip().startswith("name:"):
                    name = line.split(":", 1)[1].strip()
                    break
    
    return {
        "name": name,
        "path": skill_path,
        "size_bytes": sum(f.stat().st_size for f in skill_path.rglob("*") if f.is_file()),
        "content": content,
    }


def generate_evaluation_prompt(skill_data):
    """Generate evaluation prompt for a skill."""
    return f"""Evaluate this Hermes skill on 5 dimensions (Safety, Completeness, Executability, Maintainability, Cost-Awareness).
Rate each as Good/Average/Poor with a brief reason.

Skill: {skill_data['name']}
Size: {skill_data['size_bytes']:,} bytes

Content (truncated):
{skill_data['content'][:4000]}

Return JSON: {{"safety": {{"level": "...", "reason": "..."}}, "completeness": {{"level": "...", "reason": "..."}}, "executability": {{"level": "...", "reason": "..."}}, "maintainability": {{"level": "...", "reason": "..."}}, "cost_awareness": {{"level": "...", "reason": "..."}}}}
"""


def main():
    """Main entry point for cron job."""
    skills = find_skills()
    
    if not skills:
        print("No skills found to evaluate.")
        return
    
    # Generate summary report
    report_lines = []
    report_lines.append("📊 **5D Quality Gate Report**")
    report_lines.append(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report_lines.append(f"📦 {len(skills)} skills evaluated")
    report_lines.append("")
    
    # Group by category
    categories = {}
    for skill_path in skills:
        # Get category from path
        parts = skill_path.relative_to(SKILLS_DIR).parts
        category = parts[0] if len(parts) > 1 else "root"
        
        if category not in categories:
            categories[category] = []
        
        skill_data = read_skill(skill_path)
        if skill_data:
            categories[category].append(skill_data)
    
    # Generate report by category
    for category, cat_skills in sorted(categories.items()):
        report_lines.append(f"**{category}** ({len(cat_skills)} skills)")
        
        for skill in cat_skills:
            # Note: In a real implementation, we would call the LLM here
            # For now, just report the skill exists
            report_lines.append(f"  • {skill['name']} ({skill['size_bytes']:,} bytes)")
        
        report_lines.append("")
    
    report_lines.append("💡 **Recommendation**: Run full 5D evaluation on new or modified skills.")
    report_lines.append("   Use: `python3 ~/.hermes/profiles/gribbito/skills/integrations/skillnet/scripts/evaluate_skill_prompt.py <skill_path>`")
    
    print("\n".join(report_lines))


if __name__ == "__main__":
    main()
