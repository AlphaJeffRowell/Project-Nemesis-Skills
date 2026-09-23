# Claude Code Skill: New Project

**Type:** Interactive Project Scaffolding  
**Triggers:** "new Project", "Create a project", "Set up new client", "Start a project"  
**Status:** Ready for deployment

---

## Skill Behavior

When user says any trigger phrase, this skill:

1. **Determines mode** — "Brand new project" or "Cloning existing"?
2. **For new projects:** Asks 3 questions (code, name, phase)
3. **Creates complete structure** at `C:\Repo\Project\Project-{CODE}` with:
   - Phase 1 folder with 18 numbered subfolders
   - All embedded scripts, templates, config files
   - Git repo with initial commit
   - Pre-commit hook installed
4. **Shows success message** with next steps

---

## Implementation Logic

```
TRIGGER DETECTED: "new Project" variant
  ↓
ESTABLISH MODE
  Q: "Brand new project, or cloning an existing one?"
  ├─ "new" → NEW PROJECT FLOW
  └─ "clone" → CLONE FLOW

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NEW PROJECT FLOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COLLECT PARAMETERS
  Q1 (REQUIRED): "What's the client code? (e.g., ABC, XYZ)"
     Validate: alphanumeric + dash/underscore, not empty, doesn't exist
     Store: $clientCode
     
  Q2 (OPTIONAL): "Client name? (typically we use the ClientCode)"
     Default: $clientCode if empty
     Store: $clientName
     
  Q3 (REQUIRED): "What's the first phase called? (e.g., Onboarding, Implementation)"
     Validate: not empty
     Store: $phaseDescription

CONFIRM
  Show summary:
    Client code: {$clientCode}
    Client name: {$clientName}
    Phase: Phase 1 - {$phaseDescription}
  Q: "Shall I go ahead?"
  ├─ "yes" → Proceed
  └─ "no" → Cancel gracefully

PREFLIGHT CHECKS
  ✓ C:\Repo\Project\ exists → HARD STOP if missing
  ✓ Project-{CODE} doesn't exist → HARD STOP if exists
  ⚠ Git in PATH → WARN only
  ⚠ PowerShell 5.1+ → WARN only

CREATE PROJECT
  1. Create folder structure:
     - C:\Repo\Project\Project-{CODE}/
     - Phase 1 - {DESCRIPTION}/ + 18 subfolders
     - scripts/, _templates/, _documents/, .claude/, .github/
  
  2. Create and populate files:
     - PHASES.md (with code, description, today's date)
     - README.md (with quick links)
     - Dashboard.md (Dataview template, placeholders replaced)
     - client-config.json (populated with user values)
     - client-config.example.json (template reference)
     - .claude/settings.local.json (AI settings)
     - CONTRIBUTING.md (from embedded)
     - requirements.txt (from embedded)
  
  3. Copy embedded assets:
     - All scripts (*.ps1, *.py) to scripts/
     - All templates to _templates/
     - All workflows to .github/
     - Pre-commit hook to scripts/hooks/
  
  4. Initialize git:
     - git init
     - git branch -M main
     - git add .
     - git commit -m "Initial project structure for {clientName}"
     - Install pre-commit hook at .git/hooks/pre-commit

SUCCESS OUTPUT
  ✅ Project-{CODE} created successfully!
  
  Created at: C:\Repo\Project\Project-{CODE}
  
  What was set up:
    ✓ Folder structure (Phase 1 - {DESCRIPTION})
    ✓ 18 numbered project folders
    ✓ Git repository (local)
    ✓ Dashboard.md (Dataview-driven)
    ✓ client-config.json
    ✓ Pre-commit hook (auto-frontmatter)
    ✓ Scripts and templates
    ✓ Initial commit on 'main'
  
  Next steps:
    1. Start working: Add files to Phase 1 folders
    2. GitHub integration (optional): Create repo, add remote, push
    3. External repo (optional): Edit client-config.json

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CLONE FLOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COLLECT REPO INFO
  Q: "Repo URL or local path?"
  Store: $repoUrl

OUTPUT INSTRUCTIONS
  "To clone this repo:
   git clone {$repoUrl} C:\Repo\Project\Project-{CODE}
   cd C:\Repo\Project\Project-{CODE}
   Done!"
```

---

## Error Handling

```
ERROR SCENARIOS:

C:\Repo\Project\ missing
  → "Workspace root C:\Repo\Project\ not found. Create it first."
  → HARD STOP

Project already exists
  → "Project-{CODE} already exists. Use a different code."
  → HARD STOP

Invalid client code
  → "Use alphanumeric + dash/underscore only."
  → Re-ask Q1

Empty required field
  → "Client code/phase is required."
  → Re-ask question

User cancels
  → "Cancelled. Say 'new Project' again when ready."
  → Stop (no changes made)

Git not found
  → WARN: "Git not found. Install from https://git-scm.com"
  → Create project anyway

PowerShell < 5.1
  → WARN: "PowerShell 5.1+ needed. Current: {version}"
  → Create project anyway
```

---

## What Gets Embedded (Captured Once)

### From Project-BDT
- All templates from `_templates/`
- All PowerShell scripts from `scripts/`
- All Python scripts from `scripts/`
- Pre-commit hook + frontmatter script
- CONTRIBUTING.md
- requirements.txt
- .github/ workflows

### From Project Nemesis Library
- Folder structure templates
- Dashboard.md template
- client-config.json schema

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
│   └── [all embedded templates]
├── _documents/
├── .claude/
│   └── settings.local.json
├── .github/
│   └── [all embedded workflows]
├── PHASES.md
├── README.md
├── Dashboard.md
├── client-config.json
├── client-config.example.json
├── CONTRIBUTING.md
├── requirements.txt
└── .git/ (initialized)
```

---

## Files Created & Populated

- **PHASES.md** — Phase tracking with user's code, description, today's date
- **README.md** — Project overview with quick links to Dashboard, Decision Log
- **Dashboard.md** — Dataview template with [CLIENT], [PHASE] replaced
- **client-config.json** — Populated with code, name, phase, paths
- **.claude/settings.local.json** — AI assistant permissions
- All other files copied from embedded assets

---

## Success Criteria

✅ Trigger detected  
✅ Mode determined (new or clone)  
✅ 3 questions asked and answered (new project flow)  
✅ Pre-flight checks pass  
✅ C:\Repo\Project\Project-{CODE} created  
✅ All 18 Phase 1 subfolders present  
✅ All files present and populated  
✅ Git repo initialized with commit  
✅ Pre-commit hook installed  
✅ Success message displayed  
✅ Clone flow works (clone project flow)  

---

## Deployment Notes

- **Self-contained:** Embeds all templates/scripts; no external dependencies at runtime
- **No GitHub automation:** User creates repos manually
- **Both loaders:** PowerShell AND Python config loaders included
- **Day-1 ready:** Users get fully functional project structure
- **Flexible:** Projects can use PowerShell, Python, or both

---

## Status

✅ Specifications complete  
✅ Review approved  
✅ Ready for implementation  

**Build date:** 2026-09-16  
**Version:** 1.0  

