---
name: new-project-prompt
description: Claude Code skill prompt - defines the user interaction flow
---

# New Project Skill — Prompt Instructions

This defines what Claude Code should do when triggered with "new Project" or variants.

## Trigger Recognition

Pattern: `new Project|Create a project|Set up new client|Start a project|Add a project`

## User Interaction Flow

### Q0: Setup Mode

**Prompt:** "Brand new project, or cloning an existing one?"

**Handling:**
- If user says "clone" or "existing" → go to Clone Flow (below)
- If user says "new" or "brand new" → proceed to Q1
- If unclear → re-ask

---

### Clone Flow (alternative path)

**Prompt:** "What's the repo URL or local path?"

**Output:**
```
To clone this repo:
  git clone {URL} C:\Repo\Project\Project-{CODE}
  cd C:\Repo\Project\Project-{CODE}
```

**Then:** Stop (don't proceed further)

---

### Q1: Client Code (REQUIRED)

**Prompt:** "What's the client code? (e.g., ABC, XYZ)"

**Validation:**
- Not empty
- Alphanumeric + dash/underscore only (no special chars)
- Project doesn't already exist

**On Invalid:**
- Show error: "Use alphanumeric characters, dash, or underscore only"
- Re-ask Q1

**Store:** `$clientCode`

---

### Q2: Client Name (OPTIONAL)

**Prompt:** "Client name? (typically we use the ClientCode)"

**Handling:**
- If empty → Use `$clientCode` as default
- If provided → Use user's input

**Store:** `$clientName`

---

### Q3: Phase Description (REQUIRED)

**Prompt:** "What's the first phase called? (e.g., Onboarding, Implementation)"

**Validation:**
- Not empty

**On Invalid:**
- Show error: "Phase description is required"
- Re-ask Q3

**Store:** `$phaseDescription`

---

### Q4: .env Setup (OPTIONAL)

**Prompt:** "Would you like to configure external service credentials? (optional — you can fill these in later)"

**Handling:**
- If "no" or "skip" → Skip to Confirmation
- If "yes" → Ask for credentials

**If Yes, Ask (only non-Claude services):**

**Azure DevOps (optional):**
- "ADO organization URL? (e.g., https://dev.azure.com/YourOrg)"
- "ADO Personal Access Token?"
- "ADO Repository ID?"

**Asana (optional):**
- "Asana project name?"
- "Asana project ID?"

**SharePoint (optional):**
- "SharePoint client folder URL? (e.g., https://org.sharepoint.com/sites/Clients/CLIENT)"
- "SharePoint documents URL?"

**Everest UAT (optional):**
- "Everest UAT base URL?"
- "Everest UAT token URL?"
- "Everest UAT client ID?"
- "Everest UAT client secret?"

**Everest PROD (optional):**
- "Everest PROD base URL?"
- "Everest PROD token URL?"
- "Everest PROD client ID?"
- "Everest PROD client secret?"

**Note:** Anthropic, OpenAI, and GitHub credentials are handled by Claude Code connectors (no need to ask)

**Store:** All provided values in `$envValues` map

---

### Confirmation

**Display Summary:**
```
Client code:        {$clientCode}
Client name:        {$clientName}
Phase:              Phase 1 - {$phaseDescription}
.env values:        {count provided}
```

**Prompt:** "Shall I go ahead?"

**Handling:**
- If "yes" / "go ahead" / "proceed" → Execute deployment
- If "no" / "cancel" → Stop gracefully, no changes made
- If unclear → re-ask confirmation

---

## Deployment Execution

Once confirmed, call PowerShell script with collected parameters:

```powershell
& "C:\Repo\Project Nemesis\Deployment\Deploy-NewClientProject.ps1" `
  -ClientCode $clientCode `
  -ClientName $clientName `
  -PhaseDescription $phaseDescription `
  -ADO_ORG_URL $adoOrgUrl `
  -ADO_PAT $adoPat `
  -ADO_REPO_ID $adoRepoId `
  -EVEREST_UAT_BASE_URL $everestUatBaseUrl `
  -EVEREST_UAT_TOKEN_URL $everestUatTokenUrl `
  -EVEREST_UAT_CLIENT_ID $everestUatClientId `
  -EVEREST_UAT_CLIENT_SECRET $everestUatClientSecret `
  -EVEREST_PROD_BASE_URL $everestProdBaseUrl `
  -EVEREST_PROD_TOKEN_URL $everestProdTokenUrl `
  -EVEREST_PROD_CLIENT_ID $everestProdClientId `
  -EVEREST_PROD_CLIENT_SECRET $everestProdClientSecret
```

---

## Success Output

Display:
```
✅ Project-{$clientCode} created successfully!

Created at: C:\Repo\Project\Project-{$clientCode}

What was set up:
  ✓ Folder structure (Phase 1 - {$phaseDescription})
  ✓ 18 numbered project folders
  ✓ Git repository (local)
  ✓ Dashboard.md (Dataview-driven)
  ✓ client-config.json
  ✓ .env (with provided values)
  ✓ Pre-commit hook (auto-frontmatter)
  ✓ Scripts and templates
  ✓ Initial commit on 'main'

Next steps:
  1. Start working: Add files to Phase 1 folders
  2. GitHub integration (optional): Create repo, add remote, push
  3. External repo (optional): Edit client-config.json
```

---

## Error Handling

**Workspace root missing:**
```
Workspace root C:\Repo\Project\ not found. Create it first.
STOP (hard stop)
```

**Project already exists:**
```
Project-{CODE} already exists at C:\Repo\Project\Project-{CODE}. Use a different code.
STOP (hard stop)
```

**Invalid client code:**
```
✗ Use alphanumeric characters, dash, or underscore only.
Re-ask Q1
```

**Empty required field:**
```
✗ {Field} is required.
Re-ask the question
```

**User cancels:**
```
Cancelled. Say 'new Project' again when ready.
STOP (no changes made)
```

**Git not found:**
```
⚠ Git not found. You'll need it to push repos. Install from https://git-scm.com
(Create project anyway, warn is not a blocker)
```

**PowerShell < 5.1:**
```
⚠ PowerShell 5.1+ needed. Current: {version}
(Create project anyway, warn is not a blocker)
```

---

## Summary

- **Required parameters:** ClientCode, PhaseDescription
- **Optional parameters:** ClientName (defaults to code), all .env values
- **User interactions:** 4 required + optional .env questions
- **Estimated time:** 2-3 minutes with answers
- **Result:** Fully functional project at C:\Repo\Project\Project-{CODE}/
