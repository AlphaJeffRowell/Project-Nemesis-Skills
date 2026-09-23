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

---

## Quick Start

Say any of these to trigger the skill:
- "new Project"
- "Create a project"
- "Set up new client"
- "Start a project for ABC"
- "Add a project folder for XYZ"

The skill will:
1. Ask if this is a brand new project or cloning existing
2. For new: Ask 3 questions (code, name, phase)
3. Create complete folder structure at `C:\Repo\Project\Project-{CODE}`
4. Show success message with next steps

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

**Total:** ~40+ files, 18+ subfolders, fully ready to work

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

