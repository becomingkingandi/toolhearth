# Build Workflow

Every new project starts with `brief`. Claude Code never touches code without a finished design brief.

---

## 1. Start a session on m2

- RDP / Screen Share into m2, open Terminal
- Create a new tmux session:
  ```bash
  tmux new -s build
  ```
- Reconnect after a drop:
  ```bash
  tmux attach -s build
  ```

---

## 2. Run the design brief

```bash
cd ~/Code/PROJECTNAME && brief
```

| Detail | Value |
|--------|-------|
| Duration | 8–14 adaptive questions (~10 min) |
| Requirement | 3+ reference URLs before it finishes |
| Outputs | `DESIGN_BRIEF.md` + `CLAUDE.md` to project folder |
| Archive | `~/.shemika/briefs/DATE-PROJECT-*.md` |

Resume a dropped session:
```bash
brief --resume
```

---

## 3. Start the build

```bash
claude
```

- Claude Code reads `CLAUDE.md` automatically
- **Rule:** hero section only first → screenshot → approval → next section

---

## 4. Gate checklist

Before starting any new project:
```bash
cat ~/.shemika/SAAS_GATES.md
```

- One project in BUILD at a time
- Done = first dollar, not deployed

---

## Key paths

| What | Where |
|------|-------|
| `brief` binary | `/usr/local/bin/brief` |
| DeepSeek key | `~/.shemika/deepseek.key` |
| Brief archive | `~/.shemika/briefs/` |
| SaaS gate checklist | `~/.shemika/SAAS_GATES.md` |
| Projects | `~/Code/` |

---

## If Claude goes away

`brief` and `claude` both run independently — no active Claude session required.

```bash
cd ~/Code/PROJECT && brief    # generates the brief without this chat
claude                         # builds with Claude Code standalone
```

The design brief (`DESIGN_BRIEF.md` + `CLAUDE.md`) is the handoff doc. Any Claude Code session that opens that folder picks up exactly where you left off.
