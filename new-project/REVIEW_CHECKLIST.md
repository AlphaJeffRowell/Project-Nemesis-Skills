---
name: skill_review_checklist
description: Complete review checklist for New Project skill specifications
metadata: 
  node_type: memory
  type: project
  originSessionId: e2ac5b69-2811-4b07-bab0-b5ded7b00f46
  modified: 2026-09-16T23:25:39.857Z
---

# New Project Skill — Complete Review Checklist

**Status:** Ready for your review before implementation  
**Date:** 2026-09-16

---

## 1. TRIGGER & SCOPE

- [x] Primary trigger: **"new Project"**
- [x] Variants accepted (not limited to):
  - "Create a project"
  - "Set up new client"
  - "Start a project"
  - "Add a project for [NAME]"
  - "New client: [NAME]"
- [x] Scope: **New projects only** (no retrofit, update, or migrate)

**Review Question:** Does the trigger phrase and variants feel right?

---

## 2. USER INTERACTION FLOW

### Step 1: Setup Mode (First Question)
```
"Brand new project, or cloning an existing one?"
├─ If "new" → proceed to new project flow
└─ If "clone" → proceed to clone flow
```

### Step 2: NEW PROJECT FLOW (3 Questions)

**Q1: Client Code [REQUIRED]**
```
"What's the client code? (e.g., ABC, XYZ)"
├─ Validation: alphanumeric + dash/underscore only
├─ Check: doesn't already exist at C:\Repo\Project\Project-{CODE}
├─ Re-ask if empty or invalid
└─ Store as: $clientCode
```

**Q2: Client Name [OPTIONAL]**
```
"Client name? (typically we use the ClientCode)"
├─ Default: use $clientCode if empty
└─ Store as: $clientName
```

**Q3: Phase Description [REQUIRED]**
```
"What's the first phase called? (e.g., Onboarding, Implementation)"
├─ Validation: non-empty
├─ Re-ask if empty
└─ Store as: $phaseDescription
```

**Confirmation:**
```
Summary:
  Client code: {CODE}
  Client name: {NAME}
  Phase: Phase 1 - {DESCRIPTION}

"Shall I go ahead?"
├─ "yes" → proceed
├─ "no" → stop gracefully (no changes made)
└─ Invalid input → re-ask
```

### Step 3: CLONE PROJECT FLOW

```
"Repo URL or local path?"
├─ Store: $repoUrl
└─ Output: Clone instructions
```

**Review Question:** Does the question order feel right? Any changes?

---

## 3. PRE-FLIGHT VALIDATION

| Check | Condition | Action |
|-------|-----------|--------|
| Workspace root | C:\Repo\Project\ exists | HARD STOP if missing |
| Git in PATH | git command available | WARN only (create anyway) |
| PowerShell | Version 5.1+ | WARN only (create anyway) |
| Project exists | Project-{CODE} not found | HARD STOP if found |

**Decision:** Create project even if Git/PowerShell missing. Just warn user with actionable message.

**Review Question:** Correct approach?

---

## 4. WHAT GETS CREATED (Complete Structure)

### Root-Level Folders
- ✅ `Phase 1 - {DESCRIPTION}/` (main phase folder)
- ✅ `scripts/` + `scripts/hooks/`
- ✅ `_templates/`
- ✅ `_documents/`
- ✅ `.claude/`
- ✅ `.github/`
- ✅ `.git/`

### Phase 1 Subfolders (18 total)
- ✅ 01 - Scope Items/
- ✅ 02 - Business Requirements/
- ✅ 03 - Project Management/
- ✅ 04 - Technical Requirements/
  - ✅ Shared/
- ✅ 05 - User Stories/
- ✅ 06 - Meeting Notes/
- ✅ 06 - Release Notes/
- ✅ 07 - Database/
  - ✅ Functions/
  - ✅ Sample Data/
  - ✅ Stored Procedures/
  - ✅ Tables/
  - ✅ Views/
- ✅ 08 - Deployment/
- ✅ 09 - Test Cases/
- ✅ 10 - Packages/
- ✅ 11 - Research/

### Root-Level Files
- ✅ PHASES.md (populated with code, description, today's date)
- ✅ README.md (with quick links to Dashboard, Decision Log, Session Log)
- ✅ Dashboard.md (Dataview template with placeholders replaced)
- ✅ client-config.json (populated with code, name, phase, paths)
- ✅ client-config.example.json (template reference)
- ✅ CONTRIBUTING.md (from embedded)
- ✅ requirements.txt (from embedded)
- ✅ .claude/settings.local.json (AI assistant settings)

### Scripts & Templates (Embedded)
- ✅ Get-ClientConfig.ps1 (PowerShell config loader)
- ✅ client_config.py (Python config loader)
- ✅ All *.ps1 from Project-BDT/scripts/
- ✅ All *.py from Project-BDT/scripts/
- ✅ pre-commit hook (in scripts/hooks/)
- ✅ add_missing_frontmatter.py (hook logic)
- ✅ All templates from Project-BDT/_templates/
- ✅ All workflows from Project-BDT/.github/

### Git
- ✅ .git/ initialized
- ✅ main branch created
- ✅ Initial commit made
- ✅ pre-commit hook installed at .git/hooks/pre-commit

**Review Question:** Is this the complete structure you want?

---

## 5. EMBEDDED ASSETS (Captured Once at Skill Creation)

### From Project-BDT
- ✅ `_templates/*` — all templates
- ✅ `scripts/*.ps1` — PowerShell scripts
- ✅ `scripts/*.py` — Python scripts
- ✅ `scripts/hooks/*` — pre-commit files
- ✅ `CONTRIBUTING.md`
- ✅ `.github/*` — workflows
- ✅ `requirements.txt`

### From Project Nemesis Library
- ✅ `02-client-config/client-config.example.json`
- ✅ `05-dataview-integration/pre-commit`
- ✅ `05-dataview-integration/add_missing_frontmatter.py`

**Decision:** Both PowerShell AND Python loaders included in every project (flexibility).

**Review Question:** Any additional embedded files needed?

---

## 6. SUCCESS MESSAGE

```
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

  1. Start working:
     - Add files to Phase 1 folders
     - Dashboard.md auto-tracks progress

  2. GitHub integration (optional):
     - Create repo on GitHub manually
     - git -C C:\Repo\Project\Project-{CODE} remote add origin https://github.com/YOUR-ORG/project-{code}
     - git -C C:\Repo\Project\Project-{CODE} push -u origin main

  3. External repo configuration (optional):
     - Edit: C:\Repo\Project\Project-{CODE}\client-config.json
     - Set: externalRepos.localPath to actual path/URL
```

**Review Question:** Does the success message and next steps look complete?

---

## 7. ERROR HANDLING

| Scenario | Message | Action |
|----------|---------|--------|
| C:\Repo\Project\ missing | "Workspace root C:\Repo\Project\ not found. Create it first." | STOP |
| Project already exists | "Project-{CODE} already exists at C:\Repo\Project\Project-{CODE}. Use a different code." | STOP |
| Invalid code (special chars) | "Client code '{CODE}' contains invalid characters. Use alphanumeric + dash/underscore." | Re-ask Q1 |
| Empty code | "Client code is required." | Re-ask Q1 |
| Empty phase | "Phase description is required." | Re-ask Q3 |
| User cancels at confirm | "Cancelled. Just say 'new Project' again when ready." | STOP (no changes) |
| Git missing | WARN: "Git not found. You'll need it to push repos. Install from https://git-scm.com" | Create anyway |
| PowerShell < 5.1 | WARN: "PowerShell 5.1+ needed. Current: {version}" | Create anyway |

**Review Question:** Are the error messages clear and actionable?

---

## 8. DEPENDENCIES

| Dependency | Status | Notes |
|-----------|--------|-------|
| C:\Repo\Project\ | REQUIRED | Workspace root must exist |
| Git in PATH | Optional | Warn if missing, create anyway |
| PowerShell 5.1+ | Optional | Warn if missing, create anyway |
| Project-BDT | Not needed at runtime | Assets embedded in skill |
| Project Nemesis | Not needed at runtime | Assets embedded in skill |

**Decision:** Skill is completely self-contained. No external dependencies at runtime.

**Review Question:** Correct?

---

## 9. IMPLEMENTATION PHASES

- [ ] Phase A: Skill file creation + trigger detection
- [ ] Phase B: New project flow (3 questions, confirmation)
- [ ] Phase C: Project creation (all folders, files, scripts)
- [ ] Phase D: Git initialization + success message
- [ ] Phase E: Clone flow
- [ ] Phase F: Error handling
- [ ] Phase G: Testing

**Timeline:** ~5-7 hours total

---

## 10. FINAL SIGN-OFF CHECKLIST

**Before implementing, verify:**

- [ ] Trigger phrase and variants are correct
- [ ] 3 questions (code, name, phase) and order are correct
- [ ] Setup mode question feels right
- [ ] All 18 Phase 1 subfolders listed
- [ ] All root-level files correct
- [ ] Success message complete
- [ ] Error handling comprehensive
- [ ] Dependencies clarified (workspace only)
- [ ] Embedded assets complete
- [ ] Both loaders (PS + Python) should be included

---

## Review Instructions

Please review all sections above and confirm:

1. **Is everything correct as specified?**
2. **Any changes, additions, or deletions needed?**
3. **Ready to proceed with implementation?**

Simply confirm or point out what needs to change, and I'll build the skill.

