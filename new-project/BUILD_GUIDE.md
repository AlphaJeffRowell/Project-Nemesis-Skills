---
name: new_project_skill_build
description: "Complete implementation of \"new Project\" Claude Code skill"
metadata: 
  node_type: memory
  type: project
  status: BUILDING
  build_date: 2026-09-16
  originSessionId: e2ac5b69-2811-4b07-bab0-b5ded7b00f46
  modified: 2026-09-16T23:27:17.504Z
---

# New Project Skill — Complete Implementation

## Skill Definition & Logic

### TRIGGER DETECTION
Pattern: `new Project|Create a project|Set up new client|Start a project|Add a project|New client`

### MAIN FLOW

```
User: "new Project"
  ↓
SKILL ACTIVATES
  ↓
Q0: "Brand new project, or cloning an existing one?"
  ↓
  ├─ User: "new" → NEW PROJECT FLOW
  │
  └─ User: "clone" → CLONE FLOW
```

---

## NEW PROJECT FLOW (Complete Implementation)

### Step 1: Setup Mode Detection

```
Input: User says "new" to Q0

Action: 
  → Set mode = "new"
  → Proceed to Q1
```

### Step 2: Q1 - Client Code (REQUIRED)

```
Prompt: "What's the client code? (e.g., ABC, XYZ)"

Validation:
  ✓ Not empty
  ✓ Alphanumeric + dash/underscore only
  ✓ No special characters (@, #, $, etc.)
  ✓ Project doesn't already exist at C:\Repo\Project\Project-{CODE}

On Invalid:
  → Show error message
  → Re-ask Q1
  
On Valid:
  → Store $clientCode
  → Proceed to Q2
```

### Step 3: Q2 - Client Name (OPTIONAL)

```
Prompt: "Client name? (typically we use the ClientCode)"

Behavior:
  ✓ If empty → Use $clientCode as default
  ✓ If provided → Use what user typed
  
Store: $clientName
Proceed: Q3
```

### Step 4: Q3 - Phase Description (REQUIRED)

```
Prompt: "What's the first phase called? (e.g., Onboarding, Implementation)"

Validation:
  ✓ Not empty

On Invalid:
  → Show error: "Phase description is required."
  → Re-ask Q3

On Valid:
  → Store $phaseDescription
  → Proceed to Confirmation
```

### Step 4b: Q4 - SharePoint Site Name (NEW - PROJECT-LEVEL)

```
Prompt: "SharePoint site name? (e.g., ALTS-DemoProject)"

Validation:
  ✓ Not empty
  
On Valid:
  → Store $sharePointSite
  → Proceed to Q5
```

### Step 4c: Q5 - SharePoint Base URL (NEW - PROJECT-LEVEL)

```
Prompt: "SharePoint base URL? (e.g., https://alphafmc183.sharepoint.com/sites/)"

Validation:
  ✓ Not empty
  ✓ Valid URL format

On Valid:
  → Store $sharePointBaseUrl
  → Proceed to Q6
```

### Step 4d: Q6 - SharePoint Path (NEW - PHASE-LEVEL)

```
Prompt: "SharePoint path for this phase? (e.g., Client/Active Projects)"

Validation:
  ✓ Not empty

On Valid:
  → Store $sharePointPath
  → Proceed to Q7
```

### Step 4e: Q7 - SharePoint Meeting Notes URL (NEW - PHASE-LEVEL)

```
Prompt: "SharePoint URL for this phase's meeting notes folder?"

Validation:
  ✓ Not empty
  ✓ Valid URL format (or leave empty to skip)

On Valid:
  → Store $sharePointMeetingNotesUrl
  → Proceed to Q8
```

### Step 4f: Q8 - SharePoint Status Decks URL (NEW - PHASE-LEVEL)

```
Prompt: "SharePoint URL for this phase's status decks folder?"

Validation:
  ✓ Not empty
  ✓ Valid URL format (or leave empty to skip)

On Valid:
  → Store $sharePointStatusDecksUrl
  → Proceed to Q9
```

### Step 4g: Q9 - Asana Project GID (NEW - PHASE-LEVEL - OPTIONAL)

```
Prompt: "Asana project GID for this phase? (leave blank if not available)"

Behavior:
  ✓ If empty → Store as empty string (optional)
  ✓ If provided → Validate format and store

On Valid:
  → Store $asanaProjectGid
  → Proceed to Confirmation
```

### Step 5: Confirmation

```
Display Summary:
  Client code: {$clientCode}
  Client name: {$clientName}
  Phase: Phase 1 - {$phaseDescription}
  SharePoint site: {$sharePointSite}

Prompt: "Shall I go ahead?"

On "yes"/"go ahead":
  → Proceed to Pre-Flight
  
On "no"/"cancel":
  → Message: "Cancelled. Just say 'new Project' again when ready."
  → STOP (no changes made)
  
On Invalid:
  → Re-ask confirmation
```

### Step 6: Pre-Flight Validation

```
Check 1: C:\Repo\Project\ exists
  ✓ Pass → Continue
  ✗ Fail → STOP with message: "Workspace root C:\Repo\Project\ not found. Create it first."

Check 2: Project-{CODE} doesn't exist
  ✓ Pass → Continue
  ✗ Fail → STOP with message: "Project-{CODE} already exists at C:\Repo\Project\Project-{CODE}. Use a different code."

Check 3: Git in PATH
  ✓ Pass → Continue
  ✗ Fail → WARN: "Git not found. You'll need it to push repos. Install from https://git-scm.com"
         → Continue anyway (don't stop)

Check 4: PowerShell 5.1+
  ✓ Pass → Continue
  ✗ Fail → WARN: "PowerShell 5.1+ needed. Current: {version}"
         → Continue anyway (don't stop)

After all checks:
  → Proceed to Deployment
```

### Step 7: Project Creation (Deployment)

#### 7A: Create Folder Structure

```
Create: C:\Repo\Project\Project-{$clientCode}/

Root folders:
  - scripts/
  - scripts/hooks/
  - _templates/
  - _documents/
  - .claude/
  - .github/

Phase folder:
  - Phase 1 - {$phaseDescription}/

Phase 1 subfolders (18 total):
  - 01 - Scope Items/
  - 02 - Business Requirements/
  - 03 - Project Management/
  - 04 - Technical Requirements/
    - Shared/
  - 05 - User Stories/
  - 06 - Meeting Notes/
  - 06 - Release Notes/
  - 07 - Database/
    - Functions/
    - Sample Data/
    - Stored Procedures/
    - Tables/
    - Views/
  - 08 - Deployment/
  - 09 - Test Cases/
  - 10 - Packages/
  - 11 - Research/
```

#### 7B: Create Files

**PHASES.md** — Populated:
```markdown
# Phases — Project-{$clientCode}

| Phase | Description | Status | Started | Closed |
|---|---|---|---|---|
| Phase 1 - {$phaseDescription} | {$phaseDescription} | Active | {TODAY} | — |
```

**README.md** — Populated:
```markdown
# Project {$clientName}

> **Client:** {$clientName} | **Status:** In Progress
> **Current phase:** Phase 1 - {$phaseDescription} — see `PHASES.md` for the full phase history

## Quick Links

| Resource | Link |
|----------|------|
| Phase log | [PHASES.md](PHASES.md) |
| Dashboard (Dataview) | [Dashboard.md](Dashboard.md) |
| Decision Log | [Phase 1 - {$phaseDescription}/03 - Project Management/Decision Log.md](Phase%201%20-%20{$phaseDescription}/03%20-%20Project%20Management/Decision%20Log.md) |
| Session Log | [Phase 1 - {$phaseDescription}/03 - Project Management/Session Log.md](Phase%201%20-%20{$phaseDescription}/03%20-%20Project%20Management/Session%20Log.md) |

---

## Repository Structure

Numbered folders live inside the current phase folder (`Phase 1 - {$phaseDescription}/`); root-level items are shared across all phases.

| Folder | Purpose |
|--------|---------|
| `Phase 1 - {$phaseDescription}/01 - Scope Items/` | One file per scope item |
| `Phase 1 - {$phaseDescription}/02 - Business Requirements/` | Detailed functional requirements per module |
| `Phase 1 - {$phaseDescription}/03 - Project Management/` | Decision Log, Project Task Log, Session Log |
| `Phase 1 - {$phaseDescription}/04 - Technical Requirements/` | Developer-facing TRs per functional area |
| `Phase 1 - {$phaseDescription}/05 - User Stories/` | Lightweight story tracking |
| `Phase 1 - {$phaseDescription}/10 - Packages/` | BXP deployment package docs |
| `scripts/` | PowerShell and Python maintenance scripts (shared across phases) |

---

## How We Work

1. **Create a scope item** in `Phase 1 - {$phaseDescription}/01 - Scope Items/` for each functional area
2. **Draft requirements** in `Phase 1 - {$phaseDescription}/02 - Business Requirements/` using the BR template
3. **Track decisions** as their own file in `Phase 1 - {$phaseDescription}/03 - Project Management/` with `type: decision-paper` frontmatter
4. **Log sessions** in `Phase 1 - {$phaseDescription}/03 - Project Management/Session Log.md` after each working session
```

**Dashboard.md** — Populated with {$clientCode} and {$phaseDescription}:
```markdown
[Template with [CLIENT], [PHASE], [CLIENT NAME] replaced]
```

**client-config.json** — Populated:
```json
{
  "clientCode": "{$clientCode}",
  "clientName": "{$clientName}",
  "projectRoot": "C:\\Repo\\Project\\Project-{$clientCode}",
  "currentPhase": "Phase 1 - {$phaseDescription}",
  "versionControl": {
    "enabled": false,
    "remoteUrl": "",
    "notes": "Scaffolded by new-project-skill on {TODAY}"
  },
  "deployment": {
    "sendsPath": "C:\\Repo\\Clients\\{$clientCode}\\Sends"
  },
  "azureDevOps": {
    "organization": "",
    "project": ""
  },
  "paths": {
    "packagesFolder": "Phase 1 - {$phaseDescription}/10 - Packages",
    "databaseFolder": "Phase 1 - {$phaseDescription}/07 - Database",
    "dependencyCatalogPath": "Phase 1 - {$phaseDescription}/07 - Database/dependencies/catalog.db"
  },
  "externalRepos": []
}
```

**.claude/settings.local.json**:
```json
{
  "permissions": {
    "allow": [
      "Bash(python -c ' *)",
      "mcp__visualize__read_me",
      "mcp__visualize__show_widget"
    ]
  }
}
```

**Project-root .env** (NEW - in `C:\Repo\Project\Project-{$clientCode}\.env`):
```
# Project Configuration
PROJECT_NAME={$clientName}
PROJECT_CODE={$clientCode}

# SharePoint Base Sources
SHAREPOINT_SITE={$sharePointSite}
SHAREPOINT_BASE_URL={$sharePointBaseUrl}
```

**Phase-level .env** (NEW - in `C:\Repo\Project\Project-{$clientCode}\Phase 1 - {$phaseDescription}\.env`):
```
# Phase Configuration
PHASE_NUMBER={$phaseNumber}

# SharePoint Meeting Notes Source
SHAREPOINT_PATH={$sharePointPath}
SHAREPOINT_MEETING_NOTES_FOLDER_URL={$sharePointMeetingNotesUrl}
SHAREPOINT_STATUS_DECKS_FOLDER_URL={$sharePointStatusDecksUrl}

# Local Repo Meeting Notes Source
LOCAL_NOTES_PATH=C:\Repo\Project\Project-{$clientCode}\Phase 1 - {$phaseDescription}\06 - Meeting Notes

# Asana Configuration (optional)
ASANA_PROJECT_GID={$asanaProjectGid}
```

**Note on $phaseNumber:** Auto-extracted from {$phaseDescription} by regex match (e.g., "Phase 1 - Implementation" → "1")

**client-config.example.json** — Copy from embedded template

**CONTRIBUTING.md** — Copy from embedded (Project-BDT)

**requirements.txt** — Copy from embedded (Project-BDT)

#### 7C: Copy Embedded Scripts & Templates

**Into `scripts/`:**
```
- Get-ClientConfig.ps1 (from embedded)
- client_config.py (from embedded)
- All *.ps1 from embedded Project-BDT/scripts/
- All *.py from embedded Project-BDT/scripts/
```

**Into `scripts/hooks/`:**
```
- pre-commit (from embedded)
- add_missing_frontmatter.py (from embedded)
```

**Into `_templates/`:**
```
- All templates from embedded Project-BDT/_templates/
```

**Into `.github/`:**
```
- All workflows from embedded Project-BDT/.github/
```

#### 7D: Initialize Git Repository

```
cd C:\Repo\Project\Project-{$clientCode}

git init
git branch -M main
git add .
git commit -m "Initial project structure for {$clientName}"

Install pre-commit hook:
  Copy: scripts/hooks/pre-commit → .git/hooks/pre-commit
  chmod +x .git/hooks/pre-commit (if on Unix)
```

### Step 8: Success Output

```
✅ Project-{$clientCode} created successfully!

Created at: C:\Repo\Project\Project-{$clientCode}

What was set up:
  ✓ Folder structure (Phase 1 - {$phaseDescription})
  ✓ 18 numbered project folders
  ✓ Git repository (local)
  ✓ Dashboard.md (Dataview-driven)
  ✓ client-config.json
  ✓ Pre-commit hook (auto-frontmatter)
  ✓ Scripts and templates
  ✓ Initial commit on 'main'

Next steps:

  1. Start working:
     - Add files to Phase 1 folders
     - Dashboard.md auto-tracks progress

  2. GitHub integration (optional):
     - Create repo on GitHub manually
     - Run: git -C C:\Repo\Project\Project-{$clientCode} remote add origin https://github.com/YOUR-ORG/project-{code}
     - Run: git -C C:\Repo\Project\Project-{$clientCode} push -u origin main

  3. External repo configuration (optional):
     - Edit: C:\Repo\Project\Project-{$clientCode}\client-config.json
     - Set: externalRepos.localPath to actual path/URL
```

---

## CLONE FLOW (Complete Implementation)

### Step 1: Setup Mode Detection

```
Input: User says "clone" to Q0

Action:
  → Set mode = "clone"
  → Proceed to clone question
```

### Step 2: Clone Question

```
Prompt: "Repo URL or local path?"

Capture: $repoUrl

Output:
  "To clone this repo:
   git clone {$repoUrl} C:\Repo\Project\Project-{CODE}
   cd C:\Repo\Project\Project-{CODE}
   Done!"
```

---

## ERROR SCENARIOS (Complete)

| Scenario | Message | Action |
|----------|---------|--------|
| C:\Repo\Project\ missing | "Workspace root C:\Repo\Project\ not found. Create it first or adjust path." | HARD STOP |
| Project already exists | "Project-{CODE} already exists at C:\Repo\Project\Project-{CODE}. Use a different code." | HARD STOP |
| Invalid code (special chars) | "Client code '{CODE}' contains invalid characters. Use alphanumeric + dash/underscore." | Re-ask Q1 |
| Empty code | "Client code is required." | Re-ask Q1 |
| Empty phase | "Phase description is required." | Re-ask Q3 |
| User cancels | "Cancelled. Just say 'new Project' again when ready." | STOP (no changes) |
| Git not found | WARN: "Git not found. You'll need it to push repos. Install from https://git-scm.com" | Create anyway |
| PowerShell < 5.1 | WARN: "PowerShell 5.1+ needed. Current: {version}" | Create anyway |

---

## Implementation Ready ✅

This document is the complete, step-by-step implementation guide for the skill.

**Ready to code now.**

