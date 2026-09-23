# **AsanaTaskUpdate — Beginner Implementation Guide**

## **What Is It?**
AsanaTaskUpdate turns meeting notes into Asana task updates automatically. Write notes → system matches them to Asana tasks → system posts comments and updates tasks.

---

## **Step 1: Set Up Your Project Folder**

Make sure you have a project folder like:
```
C:\Repo\Project\Project-TWG\
└── Phase 1\
    ├── 08 - Meeting Notes\     (← Meeting notes go here)
    └── .env                     (← Config file — you'll create this)
```

**If you don't have Phase 1 folder yet, create it:**
- Right-click in Windows Explorer → New → Folder
- Name it `Phase 1`

---

## **Step 2: Create the Configuration File (.env)**

1. **Open a text editor** (Notepad, VS Code, etc.)
2. **Copy this template** and fill in YOUR values:

```env
# Project Configuration
PROJECT_NAME=TWG
PROJECT_CODE=TWG
PHASE_NUMBER=1

# SharePoint Meeting Notes Source (if using SharePoint)
SHAREPOINT_SITE=ALTS-TWG
SHAREPOINT_BASE_URL=https://alphafmc183.sharepoint.com/sites/
SHAREPOINT_PATH=Client/Active Projects

# Local Repo Meeting Notes Source
LOCAL_NOTES_PATH=C:\Repo\Project\Project-TWG\Phase 1\08 - Meeting Notes

# Asana Configuration (optional — leave as is if unsure)
ASANA_PROJECT_GID=123456789
```

3. **Replace values with YOUR project:**
   - `PROJECT_NAME` → Your project name (e.g., TWG, BDT, Chimera)
   - `PROJECT_CODE` → Short code (e.g., TWG)
   - `PHASE_NUMBER` → Which phase (usually 1)
   - `LOCAL_NOTES_PATH` → Your meeting notes folder (the `08 - Meeting Notes\` path above)

4. **Save as `.env`** in `Phase 1\` folder:
   - File → Save As
   - Name: `.env` (exactly that, no .txt)
   - Location: `C:\Repo\Project\Project-TWG\Phase 1\.env`
   - Format: All Files (not Text)

---

## **Step 3: Create a Meeting Notes File**

1. **Create a markdown file** in `08 - Meeting Notes\` folder
2. **Name it:** `2026-09-16-Meeting-Notes.md` (use today's date)
3. **Write bullet points:**

```markdown
- Q4 timeline confirmed
- Technical requirements approved
- Update project plan
```

That's it! Simple bullet points.

---

## **Step 4: Use AsanaTaskUpdate in Claude Code**

1. **Open Claude Code** (desktop app or web)
2. **Navigate to your project** folder (e.g., `Project-TWG`)
3. **Type in the chat:**

```
sync meeting notes
```

4. **Press Enter**

---

## **Step 5: Review & Confirm**

Claude will show you a confirmation screen:

```
[1] "Q4 timeline confirmed"
    Detected: Q4 Planning (Task ID: 123456)
    → [YES] [NO] [Manual ID]

[2] "Technical requirements approved"
    Detected: Tech Review (Task ID: 234567)
    → [YES] [NO] [Manual ID]
```

**What to do:**
- Click `[YES]` if the detected task is correct
- Click `[NO]` if it's wrong
- Click `[Manual ID]` if you know the exact task ID

---

## **Step 6: Done!**

Once you confirm, Claude posts your notes as comments to the Asana tasks. Your meeting notes are now linked to Asana.

---

## **Troubleshooting**

| Problem | Solution |
|---------|----------|
| System can't find .env | Make sure `.env` is in `Phase 1\` folder, not elsewhere |
| No Asana tasks found | Check your Asana task names match what you typed in notes |
| Meeting notes not found | Make sure file is in `08 - Meeting Notes\` folder and ends with `.md` |
| System says file already processed | This is intentional — prevents duplicate posts. Notes already sent. |

---

## **Advanced: Adding Actions**

You can do more than just comments. Add actions like setting due dates:

```markdown
- Q4 timeline confirmed
  @action: set_due_date
  @due_date: 2026-10-01
```

This sets the task due date to October 1, 2026.

---

**That's it! Your coworker is ready to use AsanaTaskUpdate.** 🎯
