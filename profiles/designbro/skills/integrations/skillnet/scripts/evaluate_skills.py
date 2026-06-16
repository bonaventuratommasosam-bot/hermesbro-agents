#!/usr/bin/env python3
"""
5D Quality Gate — Evaluate Hermes skills using SkillNet's 5D evaluation.

Usage:
    python evaluate_skills.py [skill_dir] [--output report.json] [--format json|text]
    
Evaluates all skills in the given directory (default: ~/.hermes/profiles/gribbito/skills/)
using the SkillNet 5D evaluation system. Produces a quality report with pass/fail status.

Exit codes:
    0: All skills pass quality gate
    1: One or more skills have "Poor" ratings
    2: Evaluation error
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# Quality gate thresholds
FAIL_DIMENSIONS = {"Poor"}  # Any dimension rated "Poor" = FAIL
WARN_DIMENSIONS = {"Average"}  # Any dimension rated "Average" = WARNING


def find_skills(skills_dir: Path) -> List[Path]:
    """Find all skills with SKILL.md files in the given directory."""
    skills = []
    for item in skills_dir.rglob("SKILL.md"):
        skill_dir = item.parent
        # Skip hidden directories within skills dir (like .hub, .archive)
        # but not parent directories like .hermes
        rel_parts = skill_dir.relative_to(skills_dir).parts
        if any(part.startswith(".") for part in rel_parts):
            continue
        skills.append(skill_dir)
    return sorted(skills)


def evaluate_skill(skill_path: Path) -> Optional[Dict]:
    """Evaluate a single skill using skillnet evaluate."""
    try:
        result = subprocess.run(
            ["skillnet", "evaluate", str(skill_path)],
            capture_output=True,
            text=True,
            timeout=120,
        )
        
        if result.returncode != 0:
            return {"error": result.stderr.strip() or "Evaluation failed"}
        
        # Parse the output - skillnet evaluate outputs JSON
        try:
            # Try to parse as JSON directly
            data = json.loads(result.stdout)
            return data
        except json.JSONDecodeError:
            # Try to extract JSON from rich table output
            lines = result.stdout.strip().split("\n")
            # Look for JSON-like content
            for line in lines:
                line = line.strip()
                if line.startswith("{"):
                    try:
                        return json.loads(line)
                    except json.JSONDecodeError:
                        continue
            
            # If no JSON found, parse the text output
            return parse_text_evaluation(result.stdout)
            
    except subprocess.TimeoutExpired:
        return {"error": "Evaluation timed out (120s)"}
    except Exception as e:
        return {"error": str(e)}


def parse_text_evaluation(text: str) -> Dict:
    """Parse text output from skillnet evaluate into structured data."""
    result = {}
    current_dim = None
    
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
            
        # Look for dimension headers
        for dim in ["Safety", "Completeness", "Executability", "Maintainability", "Cost-Awareness"]:
            if dim.lower() in line.lower():
                current_dim = dim.lower().replace("-", "_")
                # Extract level if on same line
                for level in ["Good", "Average", "Poor"]:
                    if level.lower() in line.lower():
                        result[current_dim] = {"level": level, "reason": ""}
                        break
        
        # Look for level indicators
        if current_dim and not result.get(current_dim):
            for level in ["Good", "Average", "Poor"]:
                if level.lower() in line.lower():
                    result[current_dim] = {"level": level, "reason": line}
                    break
    
    return result if result else {"error": "Could not parse evaluation output"}


def check_quality_gate(evaluation: Dict) -> Tuple[bool, List[str], List[str]]:
    """
    Check if a skill passes the quality gate.
    
    Returns:
        (passed, failures, warnings)
    """
    failures = []
    warnings = []
    
    if "error" in evaluation:
        return False, [f"Evaluation error: {evaluation['error']}"], []
    
    dimensions = ["safety", "completeness", "executability", "maintainability", "cost_awareness"]
    
    for dim in dimensions:
        if dim in evaluation:
            level = evaluation[dim].get("level", "Unknown")
            reason = evaluation[dim].get("reason", "")
            
            if level in FAIL_DIMENSIONS:
                failures.append(f"{dim}: {level} — {reason}")
            elif level in WARN_DIMENSIONS:
                warnings.append(f"{dim}: {level} — {reason}")
    
    passed = len(failures) == 0
    return passed, failures, warnings


def generate_report(results: List[Dict], output_format: str = "text") -> str:
    """Generate a quality report from evaluation results."""
    if output_format == "json":
        return json.dumps(results, indent=2)
    
    # Text format
    lines = []
    lines.append("=" * 60)
    lines.append("5D QUALITY GATE REPORT")
    lines.append(f"Generated: {datetime.now().isoformat()}")
    lines.append("=" * 60)
    
    passed_count = 0
    failed_count = 0
    warned_count = 0
    
    for result in results:
        skill_name = result["skill"]
        evaluation = result["evaluation"]
        passed, failures, warnings = result["gate_status"]
        
        if passed and not warnings:
            status = "✅ PASS"
            passed_count += 1
        elif passed:
            status = "⚠️ WARN"
            warned_count += 1
        else:
            status = "❌ FAIL"
            failed_count += 1
        
        lines.append(f"\n{status} {skill_name}")
        lines.append("-" * 40)
        
        if "error" in evaluation:
            lines.append(f"  Error: {evaluation['error']}")
            continue
        
        dimensions = ["safety", "completeness", "executability", "maintainability", "cost_awareness"]
        for dim in dimensions:
            if dim in evaluation:
                level = evaluation[dim].get("level", "?")
                reason = evaluation[dim].get("reason", "")
                icon = {"Good": "✓", "Average": "~", "Poor": "✗"}.get(level, "?")
                lines.append(f"  {icon} {dim}: {level}")
                if reason and level != "Good":
                    lines.append(f"    → {reason[:80]}")
        
        if failures:
            lines.append(f"  FAILURES: {', '.join(failures)}")
        if warnings:
            lines.append(f"  WARNINGS: {', '.join(warnings)}")
    
    lines.append("\n" + "=" * 60)
    lines.append(f"SUMMARY: {passed_count} passed, {warned_count} warnings, {failed_count} failed")
    lines.append(f"Total skills evaluated: {len(results)}")
    lines.append("=" * 60)
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="5D Quality Gate for Hermes Skills")
    parser.add_argument(
        "skill_dir",
        nargs="?",
        default="<HERMES_ROOT>/profiles/gribbito/skills",
        help="Directory containing skills to evaluate (default: ~/.hermes/profiles/gribbito/skills)",
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file for report (default: stdout)",
    )
    parser.add_argument(
        "--format", "-f",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--skill", "-s",
        help="Evaluate a specific skill by name",
    )
    parser.add_argument(
        "--skip-community",
        action="store_true",
        help="Skip community-installed skills",
    )
    
    args = parser.parse_args()
    
    skills_dir = Path(args.skill_dir)
    if not skills_dir.exists():
        print(f"Error: Skills directory not found: {skills_dir}", file=sys.stderr)
        sys.exit(2)
    
    # Find skills
    if args.skill:
        # Find specific skill
        skill_path = None
        for item in skills_dir.rglob("SKILL.md"):
            if item.parent.name == args.skill or args.skill in str(item.parent):
                skill_path = item.parent
                break
        
        if not skill_path:
            print(f"Error: Skill '{args.skill}' not found in {skills_dir}", file=sys.stderr)
            sys.exit(2)
        
        skills = [skill_path]
    else:
        skills = find_skills(skills_dir)
        
        # Skip community skills if requested
        if args.skip_community:
            skills = [s for s in skills if "community" not in s.parts]
    
    if not skills:
        print("No skills found to evaluate.", file=sys.stderr)
        sys.exit(0)
    
    print(f"Evaluating {len(skills)} skills...", file=sys.stderr)
    
    # Evaluate each skill
    results = []
    for skill_path in skills:
        skill_name = skill_path.name
        print(f"  Evaluating: {skill_name}...", file=sys.stderr)
        
        evaluation = evaluate_skill(skill_path)
        gate_status = check_quality_gate(evaluation)
        
        results.append({
            "skill": skill_name,
            "path": str(skill_path),
            "evaluation": evaluation,
            "gate_status": gate_status,
            "timestamp": datetime.now().isoformat(),
        })
    
    # Generate report
    report = generate_report(results, args.format)
    
    if args.output:
        with open(args.output, "w") as f:
            f.write(report)
        print(f"\nReport saved to: {args.output}", file=sys.stderr)
    else:
        print(report)
    
    # Exit with appropriate code
    any_failed = any(not r["gate_status"][0] for r in results)
    sys.exit(1 if any_failed else 0)


if __name__ == "__main__":
    main()
