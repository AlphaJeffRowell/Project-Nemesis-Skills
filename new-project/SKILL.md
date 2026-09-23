---
name: new-project
description: Scaffolds a complete client project with folders, templates, scripts, and configuration
triggers:
  - "new Project"
  - "Create a project"
  - "Set up new client"
  - "Start a project"
  - "Add a project"
---

# New Project Skill

**Trigger:** "new Project" (and variants)  
**Purpose:** Scaffolds a complete client project with folders, templates, scripts, and configuration  
**Status:** Ready for deployment  
**Updated:** 2026-09-23

---

## Quick Start

Say any of these to trigger the skill:
- "new Project"
- "Create a project"
- "Set up new client"
- "Start a project for ABC"
- "Add a project folder for XYZ"

The skill will ask (one at a time):
1. Setup mode: "Brand new or cloning?"
2. Q1: Client code (required)
3. Q2: Client name (optional — defaults to code)
4. Q3: Phase description (required)
5. Optional: Populate .env with API keys? (optional)
6. Confirmation before creating

Then creates complete folder structure at `C:\Repo\Project\Project-{CODE}` and shows success message with next steps

---

## What Gets Created

**Complete structure:**
- Phase 1 folder with 18 numbered subfolders (01-Scope through 11-Research)
- All embedded scripts (PowerShell + Python config loaders)
- All embedded templates
- All embedded workflows (.github/)
- Git repo initialized with initial commit
- Pre-commit hook for auto-frontmatter injection
- PHASES.md, README.md, Dashboard.md, client-config.json
- `.env` file (with optional values populated, if provided)

**Total:** ~40+ files, 18+ subfolders, fully ready to work

## How It Works

1. Claude Code skill asks user questions one at a time
2. Collects all answers (client code, name, phase, optional .env values)
3. Calls PowerShell script: `Deploy-NewClientProject.ps1` with parameters
4. Script creates complete project structure
5. Returns success message to user

---

## File Structure

```
C:\Repo\Project\Skills\new-project/
├── SKILL.md (this file — quick reference)
├── IMPLEMENTATION.md (complete implementation spec)
├── DECISIONS.md (all 6 design decisions locked in)
├── BUILD_GUIDE.md (step-by-step build instructions)
├── REVIEW_CHECKLIST.md (pre-deployment review)
├── README.md (deployment instructions)
└── assets/ (embedded templates, scripts, workflows)
    ├── templates/
    ├── scripts/
    ├── workflows/
    └── config-examples/
```

---

## Deployment Status

✅ **Specifications:** Complete  
✅ **Review:** Approved  
✅ **Build Guide:** Ready  
✅ **Documentation:** Complete  
⏳ **Deployment:** Ready to install  

---

See README.md for deployment instructions.

