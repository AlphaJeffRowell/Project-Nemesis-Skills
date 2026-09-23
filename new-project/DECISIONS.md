---
name: project_nemesis_decisions
description: Recorded decisions from skill implementation planning session
metadata: 
  node_type: memory
  type: project
  originSessionId: 23306f3d-93af-4492-8a12-5f0dbcafc048
  modified: 2026-09-16T23:23:31.838Z
---

# Project Nemesis Skill — Implementation Decisions

## Decision 1: Trigger Scope ✅ DECIDED

**Question:** Single trigger ("new Project" only) or multi-purpose ("new/update/retrofit")?

**Decision:** Keep it simple — **only new projects**

**Details:**
- Primary trigger: "new Project"
- Accept variants (provide options but not limited to):
  - "Create a project"
  - "Set up new client"
  - "Start a project"
  - "Add a project for [NAME]"
  - "New client: [NAME]"
- **OUT OF SCOPE:** Retrofit, update, migrate commands (separate skills if needed)
- **Rationale:** Single-purpose, simpler implementation, easier to test

**Implementation Impact:** 
- Trigger detection: straightforward regex/pattern matching
- No conditional branching for different project states
- Clear error message if user asks about retrofitting (point them to docs)

---

## Decision 2: Parameters & Setup Mode ✅ DECIDED (UPDATED)

**Question:** Which parameters required vs. optional? What flow?

**CRITICAL FIRST QUESTION: Setup Mode**

Before anything else, ask:

**"Is this a brand new project setup, or are you cloning an existing project?"**

- **Mode A: NEW PROJECT** → Ask all parameters (code, name, phase, GitHub, external repo)
- **Mode B: CLONING EXISTING** → Skip all setup questions, just help with clone/credentials

**Decision for Mode A (New Project):**

| Parameter | Status | Notes |
|-----------|--------|-------|
| `clientCode` | **REQUIRED** | No default |
| `clientName` | Optional | Notify user: "typically we'd use the ClientCode" |
| `phaseDescription` | **REQUIRED** | (different from original spec) |

**Decision for Mode B (Cloning Existing):**

| Action | What to do |
|--------|-----------|
| Ask repo URL | "What's the repo URL?" |
| Point to clone docs | "Run: `git clone <URL> C:\Repo\Project\Project-<CODE>`" |
| Done | No need for setup |

**Details:**
- **New Mode:** 3 questions only (code REQUIRED, name OPTIONAL, phase REQUIRED)
- **Clone Mode:** Just get the URL, print clone instructions, done
- Key insight: Different users have different needs — new project creators vs. team members joining
- Rationale: Simplify setup flow; GitHub and external repo are optional next steps, not part of initial creation

**Implementation Impact:**
- First question determines entire flow
- New project: streamlined 3-question wizard
- Clone existing: minimal helper flow
- GitHub and external repo: handled by deploy script defaults (can be edited in config after)

---

## Decision 3: Pre-Flight Validation & Dependencies ✅ DECIDED (FINAL)

**Question:** What's actually a hard requirement vs. a warning? Where do templates come from?

**Clarification from user:**
- Skill is self-contained (no external Project-BDT dependency)
- Skill embeds templates/scripts from Project-BDT in its own memory/config
- Only outputs to: `C:\Repo\Project\Project-<CODE>`
- Project Nemesis Deploy script is called, but all templates are already embedded in skill

**Decision:**

| Dependency | Status | Action |
|-----------|--------|--------|
| `C:\Repo\Project\` | **REQUIRED** | Fail if missing (workspace root where projects are created) |
| Git in PATH | **OPTIONAL** | Create structure anyway, warn user: "You'll need git to push and manage repos" |
| PowerShell 5.1+ | **OPTIONAL** | Create structure anyway, warn user: "You'll need PowerShell 5.1+ to run scripts" |

**What Gets Embedded in Skill (from Project-BDT & Project Nemesis):**
- All templates from `Project-BDT\_templates\`
- All scripts from `Project-BDT\scripts\`
- `CONTRIBUTING.md` template
- `.github\` workflows/templates
- `requirements.txt`
- Pre-commit hook + Dataview scripts
- Client-config.json schema
- README/Dashboard templates

**What Gets Created (COMPLETE folder & object structure):**

Root-level folders:
- `Phase 1 - {DESCRIPTION}/` (phase folder)
- `scripts/` + `scripts/hooks/` (all embedded scripts + pre-commit hook)
- `_templates/` (all embedded templates from Project-BDT)
- `_documents/`
- `.claude/` (with settings.local.json)
- `.github/` (workflows from Project-BDT, if exists)

Inside Phase 1 folder (all 18 numbered subfolders):
- `01 - Scope Items/`
- `02 - Business Requirements/`
- `03 - Project Management/`
- `04 - Technical Requirements/` + `Shared/`
- `05 - User Stories/`
- `06 - Meeting Notes/` + `Release Notes/`
- `07 - Database/` + `Functions/`, `Sample Data/`, `Stored Procedures/`, `Tables/`, `Views/`
- `08 - Deployment/`
- `09 - Test Cases/`
- `10 - Packages/`
- `11 - Research/`

Root-level files:
- `PHASES.md` (phase tracking)
- `README.md` (project overview with quick links)
- `Dashboard.md` (Dataview-driven progress dashboard)
- `client-config.json` (populated with code, name, phase)
- `client-config.example.json` (template reference)
- `CONTRIBUTING.md` (from Project-BDT)
- `requirements.txt` (if exists in Project-BDT)

Git:
- `.git/` folder (local repo initialized)
- Initial commit on `main` branch

All embedded inside:
- Get-ClientConfig.ps1 (PowerShell config loader)
- client_config.py (Python config loader) — both included for flexibility
- Pre-commit hook (auto-frontmatter injection)
- add_missing_frontmatter.py (hook logic)
- All scripts from Project-BDT
- All templates from Project-BDT
- All items from Project-BDT/.github/

**Total output: Complete, functional client project ready to use**

---

## Decision 6: Script Loaders ✅ DECIDED

**Question:** Include both PowerShell and Python config loaders, or just one?

**Decision:** **Both loaders in every project (Option A)**

**Details:**
- `Get-ClientConfig.ps1` always included (PowerShell automation)
- `client_config.py` always included (Python automation)
- Projects can use either or both depending on their tooling
- No "Which language?" question during setup
- Keeps projects flexible from day 1

**Rationale:** Some projects use PowerShell scripts, others use Python. Both loaders are lightweight; including both gives projects maximum flexibility without asking users to choose upfront.

**Details:**
- Skill is 100% self-contained
- No dependency on Project-BDT or Project Nemesis existing on user's machine
- Templates captured ONCE when skill is created; updates to Project-BDT templates require skill refresh
- User output: clean `C:\Repo\Project\Project-<CODE>` folder with everything ready to use

**Rationale:** Skill is portable, works without external dependencies, ensures consistent project structure across all uses.

---

## Decision 4: External Repo Handling ✅ DECIDED

**Question:** When user says "yes" to external repo, ask for path now or create stub?

**Decision:** **Option B — Create stub, fill in later**

**Details:**
- Don't ask for external repo URL/path during setup
- When user chooses `withExternalRepo=true`, create stub entry in `client-config.json`
- Print instruction: "Edit client-config.json after creation and add the real path/URL to `externalRepos.localPath`"
- Keep setup flow uncluttered

**Rationale:** 
- User may not have the URL handy during setup
- Reduces setup questions
- Can be filled in immediately after if needed
- Aligns with "escape hatch" philosophy from Decision 2

**Implementation Impact:**
- External repo question in Mode A: just "yes/no"
- No follow-up question for URL
- Success message includes: "Don't forget to update externalRepos in client-config.json"

---

## Decision 5: GitHub Repo Creation ✅ DECIDED

**Question:** Should skill automate GitHub repo creation or let user handle it?

**Decision:** **NO AUTOMATION** — User creates repo manually on GitHub

**Details:**
- Don't use `gh` CLI to create repos
- Skill sets up LOCAL git repo only
- If user says "yes" to GitHub option:
  - Create local git repo with `main` branch
  - Print instructions: "Create this repo on GitHub manually, then run: `git remote add origin https://github.com/YOUR-ORG/project-<CODE>` and `git push -u origin main`"
- If user says "no" to GitHub:
  - Create local git repo only
  - Done

**Rationale:**
- GitHub repo creation is a shared organizational action
- No single default org to use (varies per team/company)
- User should be explicit about where repos live
- Avoids permission issues, org mismatches, unintended repos

**Implementation Impact:**
- No `gh` CLI required
- No GitHub org question needed
- Success message includes manual GitHub setup instructions (if user said "yes")

---

## Final Action Plan ✅ COMPLETE

### Skill Overview
- **Name:** "new Project" skill
- **Trigger:** "new Project" + variants ("Create a project", "Set up new client", etc.)
- **Scope:** New project creation only (not clone, retrofit, or update)
- **Outcome:** Fully scaffolded project at `C:\Repo\Project\Project-<CODE>/` with git, structure, config, hooks

---

### User Flow

```
USER SAYS: "new Project"
    ↓
SKILL: "Brand new project setup, or cloning an existing one?"
    ↓
    ├─→ "New project"
    │   ├─ Q1: "Client code?" [REQUIRED]
    │   ├─ Q2: "Client name?" [OPTIONAL, default: code]
    │   ├─ Q3: "Phase description?" [REQUIRED]
    │   ├─ CONFIRMATION: Show summary, ask "Go ahead?"
    │   ├─ PRE-FLIGHT: Check C:\Repo\Project\ exists
    │   │             Warn if Git/PowerShell missing (don't fail)
    │   ├─ DEPLOY: Run Deploy-NewClientProject.ps1
    │   ├─ SUCCESS: Print what was created + next steps
    │   └─ DONE
    │
    └─→ "Cloning existing"
        ├─ Q: "Repo URL/path?"
        ├─ PRINT: Clone instructions
        └─ DONE
```

---

### Question Details

**SETUP MODE (First Question)**
```
"Is this a brand new project, or are you cloning an existing project?"
  → If "new": Go to New Project Flow
  → If "clone": Go to Clone Flow
```

**NEW PROJECT FLOW**

Q1: Client Code (REQUIRED)
```
"What's the client code? (e.g., ABC, XYZ)"
  → Must be alphanumeric + dash/underscore
  → No default
  → If empty: Re-ask
```

Q2: Client Name (OPTIONAL)
```
"Client name? (typically we use the ClientCode)"
  → Press Enter or type name
  → If empty: Use clientCode
```

Q3: Phase Description (REQUIRED)
```
"What's the first phase called? (e.g., Onboarding, Implementation)"
  → Must be provided
  → No default
  → If empty: Re-ask
```

**CONFIRMATION**
```
Summary:
  Client code: {code}
  Client name: {name}
  Phase: Phase 1 - {description}

"Shall I go ahead?"
  → "yes"/"go ahead" = Proceed
  → "no"/"cancel" = Stop (no changes made)
```

---

### Pre-Flight Checks (Warnings Only, Don't Fail)

| Check | Status | Action |
|-------|--------|--------|
| C:\Repo\Project\ exists | HARD STOP | Fail if missing: "Workspace root C:\Repo\Project\ not found" |
| Git in PATH | WARN | If missing: "Git not found. You'll need it to push repos. Install from https://git-scm.com" |
| PowerShell 5.1+ | WARN | If missing: "PowerShell 5.1+ needed. You'll need it for scripts. Current: {version}" |

**Decision:** Even if Git/PowerShell missing, CREATE THE PROJECT ANYWAY. Just warn user.

---

### Deployment

```
Calls: C:\repo\Project Nemesis\Deployment\Deploy-NewClientProject.ps1
Parameters:
  -ClientCode {code}
  -ClientName "{name}"
  -PhaseDescription "{description}"

Output: Stream real-time to user
Exit codes: 0 = success, anything else = failure
```

---

### Success Message

```
✅ Project-{CODE} created successfully!

Created at: C:\Repo\Project\Project-{CODE}

What was set up:
  ✓ Folder structure (Phase 1 - {DESCRIPTION})
  ✓ 11 numbered project folders (01-Scope through 11-Research)
  ✓ Git repository (local)
  ✓ Dashboard.md (Dataview-driven)
  ✓ client-config.json (project config)
  ✓ Pre-commit hook (auto-frontmatter)
  ✓ Scripts and templates
  ✓ Initial commit on 'main'

Next steps:

  1. Start working:
     - Add files to Phase 1 folders
     - Dashboard.md auto-tracks progress

  2. GitHub integration (optional):
     - Create repo on GitHub manually
     - Run: git -C C:\Repo\Project\Project-{CODE} remote add origin https://github.com/YOUR-ORG/project-{code}
     - Run: git -C C:\Repo\Project\Project-{CODE} push -u origin main

  3. External repo configuration (optional):
     - Edit: C:\Repo\Project\Project-{CODE}\client-config.json
     - Set: externalRepos.localPath to actual path/URL
```

---

### Error Handling

| Error Scenario | Action |
|---|---|
| C:\Repo\Project\ doesn't exist | STOP: "Workspace root not found at C:\Repo\Project\. Create it first or adjust path." |
| Project-{CODE} already exists | STOP: "Project-{CODE} already exists. Use a different code." |
| Deployment script fails | PRINT error output, SUGGEST: "Check Project Nemesis library is installed, or run manually" |
| User cancels confirmation | STOP: "Cancelled. Just say 'new Project' again when ready." |
| Git missing | WARN: "Git not found. Project created but you'll need git to use it." |

---

### CLONE EXISTING Flow

```
Q: "Repo URL or local path?"
  → User provides URL

PRINT:
  "To clone this repo:
   git clone {URL} C:\Repo\Project\Project-<CODE>
   cd C:\Repo\Project\Project-<CODE>
   Done!"
```

---

### Implementation Phases

**Phase A: Build Skill Structure**
- [ ] Create skill file (syntax appropriate for Claude Code skills)
- [ ] Implement trigger detection ("new Project" + variants)
- [ ] Implement setup mode detection (new vs. clone)

**Phase B: New Project Flow**
- [ ] Q1-Q5 parameter collection
- [ ] Confirmation flow
- [ ] Pre-flight validation
- [ ] Deploy-NewClientProject.ps1 execution
- [ ] Success message generation

**Phase C: Clone Flow**
- [ ] Simple repo URL capture
- [ ] Clone instruction printing

**Phase D: Error Handling**
- [ ] All error scenarios from table above
- [ ] Graceful failures with actionable messages

**Phase E: Testing**
- [ ] Run test suites from project_nemesis_test_plan.md
- [ ] Verify both flows work
- [ ] Edge case testing

**Phase F: Refinement**
- [ ] UX review
- [ ] Message polish
- [ ] Documentation update

---

## Status: READY FOR IMPLEMENTATION ✅

All decisions locked in. Document is final. Ready to build the skill.

**Go-live checklist:**
- [ ] Skill created and tested
- [ ] Both user flows working (new + clone)
- [ ] All 18 subfolders created in Phase 1
- [ ] All embedded files (scripts, templates, config) present
- [ ] Git repo initialized with commit
- [ ] Success message displayed
- [ ] Error handling functional
- [ ] QA test suite passed

---

## Summary of All Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Trigger Scope | New projects only (variants OK) | Keep it simple |
| Parameters | Only 3 questions: Code (REQUIRED), Name (optional), Phase (REQUIRED) | Streamline setup, fewer questions |
| Setup Mode | Ask "new or clone?" first | Different user needs |
| Dependencies | Only C:\Repo\Project\ (REQUIRED) | Workspace root only; skill is self-contained |
| Templates & Scripts | Embedded in skill (from Project-BDT) | Skill is portable, no external dependencies |
| GitHub & External Repo | User configures after creation (optional) | Keep setup focused, not in-wizard questions |

