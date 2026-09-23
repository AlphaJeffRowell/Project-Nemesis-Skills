# New Project Skill — Deployment & Usage Guide

**Status:** ✅ Ready for Deployment  
**Version:** 1.0  
**Created:** 2026-09-16

---

## What This Skill Does

Scaffolds a complete client project with one command:

```
User: "new Project"
↓
Skill: Creates C:\Repo\Project\Project-{CODE}/ with:
  • Phase 1 folder + 18 numbered subfolders
  • All embedded scripts (PS1 + Python)
  • All embedded templates
  • Git repo + initial commit
  • Dashboard.md (Dataview-driven)
  • client-config.json (populated)
  • .env (project-level config)
  • Phase 1/.env (phase-level config)
  • Pre-commit hook (auto-frontmatter)
↓
User gets: Fully functional project with SharePoint & Asana integration, ready to work
```

---

## Deployment Instructions

### Step 1: Verify Location

The skill is now at:
```
C:\Repo\Project\Skills\new-project/
├── SKILL.md (quick reference)
├── DEPLOYMENT.md (ready-to-deploy spec)
├── IMPLEMENTATION.md (complete implementation)
├── BUILD_GUIDE.md (step-by-step build)
├── DECISIONS.md (6 design decisions)
├── REVIEW_CHECKLIST.md (review before deployment)
└── README.md (this file)
```

### Step 2: Register Skill (If Applicable)

If Claude Code has a skill registry:
1. Copy this folder path to your Claude Code configuration
2. Or symlink from `.claude/skills/new-project` to this folder
3. Skill becomes available in next session

### Step 3: Test the Skill

In any Claude Code session:
```
User: "new Project TEST"
```

Expected output:
1. Mode question: "Brand new or cloning?"
2. Q1: "Client code?" → TEST
3. Q2: "Client name?" → TEST
4. Q3: "Phase?" → Onboarding
5. Q4-Q9: SharePoint site, base URL, path, URLs + Asana GID
6. Confirmation
7. Folder created: C:\Repo\Project\Project-TEST/
8. .env files created (project + phase level)
9. Success message

---

## File Reference

### Quick References
- **SKILL.md** — Start here. One-page overview.
- **DEPLOYMENT.md** — Ready-to-deploy skill definition with flowcharts.

### Implementation Details
- **BUILD_GUIDE.md** — Step-by-step, line-by-line build instructions.
- **IMPLEMENTATION.md** — Complete spec with all file structures, embedded assets, logic.
- **DECISIONS.md** — All 6 design decisions (trigger, parameters, dependencies, etc.)

### Review & QA
- **REVIEW_CHECKLIST.md** — Pre-deployment review checklist (10 sections, all locked in).

---

## What Gets Embedded (Assets)

The skill embeds these once:

**From Project-BDT:**
- All templates from `_templates/`
- All PowerShell scripts from `scripts/`
- All Python scripts from `scripts/`
- Pre-commit hook + frontmatter script
- CONTRIBUTING.md, requirements.txt
- .github/ workflows

**From Project Nemesis library:**
- Folder structure templates
- Dashboard.md template
- client-config.json schema

---

## Key Features

✅ **Self-contained** — No external dependencies at runtime  
✅ **Complete** — 42+ files, 18+ subfolders created  
✅ **Integrated** — Captures SharePoint, Asana, meeting notes configs  
✅ **Smart** — Validates input, checks for conflicts, warns on missing tools  
✅ **Flexible** — Handles both new projects and cloning  
✅ **Multi-phase ready** — Each phase can have different configs  
✅ **Day-1 ready** — Users get fully functional project structure  
✅ **Documented** — README, Dashboard, client-config, .env all auto-populated  

---

## Trigger Phrases (All Supported)

- "new Project"
- "Create a project"
- "Set up new client"
- "Start a project for ABC"
- "Add a project folder for XYZ"
- "New client: Acme"
- Any variant matching pattern: "new Project|Create a project|Set up new client|Start a project|Add a project"

---

## Error Handling

| Scenario | Behavior |
|----------|----------|
| C:\Repo\Project\ missing | HARD STOP with clear message |
| Project already exists | HARD STOP with clear message |
| Invalid code (special chars) | Re-ask question |
| Git not found | WARN, create project anyway |
| PowerShell < 5.1 | WARN, create project anyway |
| User cancels | Stop gracefully, no changes |

---

## Folder Structure Created

```
Project-{CODE}/
├── Phase 1 - {DESCRIPTION}/
│   ├── 01 - Scope Items/
│   ├── 02 - Business Requirements/
│   ├── 03 - Project Management/
│   ├── 04 - Technical Requirements/
│   │   └── Shared/
│   ├── 05 - User Stories/
│   ├── 06 - Meeting Notes/
│   ├── 07 - Database/
│   │   ├── Functions/
│   │   ├── Sample Data/
│   │   ├── Stored Procedures/
│   │   ├── Tables/
│   │   └── Views/
│   ├── 08 - Deployment/
│   ├── 09 - Test Cases/
│   ├── 10 - Packages/
│   └── 11 - Research/
├── scripts/
│   ├── hooks/
│   ├── Get-ClientConfig.ps1
│   ├── client_config.py
│   └── [all embedded scripts]
├── _templates/
├── _documents/
├── .claude/
├── .github/
├── .env (project-level configuration)
├── Phase 1 - {DESCRIPTION}/
│   └── .env (phase-level configuration)
├── PHASES.md
├── README.md
├── Dashboard.md
├── client-config.json
├── CONTRIBUTING.md
├── requirements.txt
└── .git/ (initialized)
```

---

## Success Criteria

✅ Skill recognizes trigger phrase  
✅ Mode determined (new vs clone)  
✅ User asks for 9 parameters (new project: code, name, phase, 4 SP config, Asana GID)  
✅ Workspace root exists  
✅ Project doesn't already exist  
✅ Project created at C:\Repo\Project\Project-{CODE}  
✅ All 18 Phase 1 subfolders present  
✅ Project-root .env created with config  
✅ Phase-level .env created with config  
✅ All files created and populated  
✅ Git repo initialized with commit (includes .env files)  
✅ Pre-commit hook installed  
✅ Success message displayed  

---

## Next Steps

1. **Deploy** — Register skill in Claude Code
2. **Test** — Run "new Project TEST"
3. **Verify** — Check C:\Repo\Project\Project-TEST/ created correctly
4. **Document** — Update Claude Code docs/help if needed
5. **Use** — Start using: "new Project ABC"

---

## Questions?

Refer to the appropriate file:
- **How does it work?** → SKILL.md
- **What gets created?** → BUILD_GUIDE.md
- **Why these design decisions?** → DECISIONS.md
- **Ready to deploy?** → REVIEW_CHECKLIST.md
- **Step-by-step implementation?** → IMPLEMENTATION.md

---

**Skill: READY FOR DEPLOYMENT ✅**

