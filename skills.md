# Claude Skills — what's installed & how to fire it

Skills are loaded by Claude on every session. To activate one in a chat: **type `/<name>`** or just say something that matches the trigger.

Source of truth: `~/.claude/skills/<name>/SKILL.md`. Reference prompts: `~/.shemika/pro-master-prompts/`.

---

## Installed this week (2026-05-27)

| Skill | Slash | Fires automatically when you say… |
|-------|-------|-----------------------------------|
| **getting-unstuck** | `/getting-unstuck` | "I'm stuck", "I can't start", "I'm overwhelmed", "what was I doing", "this is boring", "I keep switching tasks" |
| **business-research-build** | `/business-research-build` | "Research [topic]", "Plan a [business]", "Validate this idea", "Competitive tear-down on X", "Financial model for X", "What am I missing" |
| **website-research-build** | `/website-research-build` | "Build me a landing page for…", "Redesign [URL]", "Add a pricing page with X", "Build a faceless content site about [niche]", "Audit [URL]" |
| **saas-company-builder** | `/saas-company-builder` | "Validate [SaaS idea]", "Plan [SaaS]", "Build MVP for [SaaS]", "Launch [SaaS]", "Grow [SaaS]", "Kill [feature]", "Competitor deep-dive on [SaaS]" |
| **wire-feedback-first** | `/wire-feedback-first` | About to build UI / content batch / design / data without a quality check wired. Discipline: name the judge first, iterate 2-3x. |
| **claude-as-unix-utility** | `/claude-as-unix-utility` | "Write a script that pipes git diff through claude -p", "Set up a CI step that…", "Batch transform these files with claude -p", "Make this a one-liner", commit-message generators, log triage |

### Notes on these 6

- **website-research-build** opens with PRECEDENCE block — `project_website_standard` (locked $100K+ bar) **overrides** the skill's default constraints
- **business / website / saas** mirror Shemika's pro-master-prompts at `~/.shemika/pro-master-prompts/`
- **wire-feedback-first** generalizes TDD beyond code → covers screenshots, scorers, sample diffs, brief CLI re-checks
- **claude-as-unix-utility** documents `--allowed-tools`, `--output-format json`, pipe-in/pipe-out, batch xargs patterns

---

## 3 ways to activate any skill

| Method | How |
|--------|-----|
| **Slash command** | `/<skill-name>` (explicit, force-load) |
| **Trigger phrase** | Just describe what you're doing — Claude auto-fires when message matches skill's description |
| **Direct ask** | `use the <skill-name> skill to <task>` (manual override) |

---

## Other skills available

### Process / discipline

| Skill | When to use |
|-------|-------------|
| `brainstorming` | Before any creative work — explore intent before implementation |
| `writing-plans` | Multi-step task, before touching code |
| `test-driven-development` | Implementing any feature/bugfix, write test first |
| `systematic-debugging` | Bug, test failure, or unexpected behavior |
| `verification-before-completion` | About to claim "done" / "fixed" / "passing" |
| `requesting-code-review` | Major feature complete, before merge |
| `receiving-code-review` | Got review feedback, before implementing it |
| `using-superpowers` | Start of any conversation |
| `writing-skills` | Creating/editing a skill |

### Execution

| Skill | When to use |
|-------|-------------|
| `executing-plans` | Have a written plan, executing in a separate session |
| `subagent-driven-development` | Executing plan with independent tasks in current session |
| `dispatching-parallel-agents` | 2+ independent tasks with no shared state |
| `using-git-worktrees` | Feature work needs isolation from current workspace |
| `finishing-a-development-branch` | Implementation complete, choosing merge path |

### OSINT

| Skill | When to use |
|-------|-------------|
| `osint-methodology` | Planning/executing recon against authorized targets |
| `offensive-osint` | Operational arsenal — wordlists, dorks, validators, vendor fingerprints |

### Claude Code system

| Skill | When to use |
|-------|-------------|
| `claude-api` | Building/debugging Claude API / Anthropic SDK apps |
| `cua-driver` | Drive a native macOS app via AX tree |
| `update-config` | Configure settings.json — permissions, env, hooks |
| `keybindings-help` | Customize keyboard shortcuts |
| `fewer-permission-prompts` | Scan transcripts → add allowlist to reduce prompts |
| `queue-resume` | Snapshot session, auto-resume after Max 5h window |
| `loop` | Run a prompt/command on a recurring interval |
| `schedule` | Cron-style scheduled remote agents |
| `verify` | Run the app, observe behavior, confirm change works |
| `run` | Launch and drive this project's app |
| `code-review` | Review current diff for correctness bugs |
| `security-review` | Security review of pending changes |
| `review` | Review a pull request |
| `init` | Initialize a new CLAUDE.md |

### Document formats (Anthropic)

| Skill | When to use |
|-------|-------------|
| `anthropic-skills:docx` | Create/edit Word documents |
| `anthropic-skills:xlsx` | Create/edit spreadsheets (xlsx/csv/tsv) |
| `anthropic-skills:pptx` | Create/edit slide decks |
| `anthropic-skills:pdf` | Read/create/edit/OCR PDFs |
| `anthropic-skills:skill-creator` | Bootstrap / improve / eval a skill |
| `anthropic-skills:consolidate-memory` | Reflective pass over memory files |

---

## Where things live

| What | Path |
|------|------|
| Skill source | `~/.claude/skills/<name>/SKILL.md` |
| Pro-master prompts (Shemika) | `~/.shemika/pro-master-prompts/` |
| Memory index | `~/.claude/projects/-Users-m2max/memory/MEMORY.md` |
| Per-memory files | `~/.claude/projects/-Users-m2max/memory/<name>.md` |

---

## Quick sanity check

- If a skill should auto-fire but doesn't, the trigger description didn't match.
- **Fix:** Update the skill's `description:` frontmatter (add the missing trigger phrase)
- **Fallback:** Use slash form `/<skill-name>`
- Skill changes are picked up on next chat session — no daemon to restart.
