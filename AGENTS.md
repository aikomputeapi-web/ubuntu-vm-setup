# coding — AGENTS.md

Instructions apply to every agent working in this workspace.

---

## Rule 1 — Ask If Unsure (Even If You Think You're Sure)

If there is any chance your understanding has two possible meanings, **you must ask**.

- **Threshold:** Ask only when the ambiguity could change the outcome — files edited, behavior implemented, scope, tools used, or interpretation of requirements. Do not ask about trivial wording that doesn't affect what gets built.
- **Even when confident:** If you are 90% sure but a second plausible reading exists that would change the outcome, treat it as ambiguous and ask.
- **How to ask:** Be proactive. Surface the ambiguity explicitly: state your current interpretation, the alternative(s), and what you would do under each. Let the user choose.
- **Never assume silently:** Do not guess and keep building when an outcome-changing ambiguity exists at the start.

> Example: "You said 'clean up old files' — do you mean (A) delete untracked temp files only, or (B) also delete git-ignored build artifacts? My default reading is (A). Which should I use?"

---

## Rule 2 — Ask Everything Up Front — Never Halt Mid-Task (Rule 1a)

All clarifying questions **must be asked at the very beginning** of a task, in a single batched turn. **Never stop mid-task to wait for an answer.**

- **Batch at start:** Before writing code, installing, or editing, assess the full task for ambiguities, missing inputs, and edge cases. Ask every outcome-changing question together in one go.
- **Do not pause later:** Once work has started, do not block on a question. If you are mid-task on step 2 of 20, you must keep building — do not halt to await the user, especially when the user has shifted focus elsewhere.
- **If new ambiguity emerges mid-task:** You were not able to foresee it at the start, so **make the best reasonable assumption, log the assumption clearly (in your response and/or in code comments/logs), and continue**. Do not stop.
  - Choose the safest, most reversible default.
  - Note it explicitly: `Assumption: [what you assumed] — reason: [why] — revisit if needed.`
  - Keep the rest of the task moving; do not leave the task half-finished waiting for input.
- **Absolute:** This "never halt mid-task" rule has no exceptions. Having questions is fine — stopping work is not.
- **If the user is unavailable:** Do not idle. Proceed under documented assumptions and deliver a complete result the user can correct afterwards in one pass.

### Workflow this enforces

1. Read the request and inspect relevant files/context.
2. Identify every outcome-changing ambiguity or missing detail.
3. Ask all questions at once — then wait for answers **once**.
4. After answers (or if no answer), execute the entire task end-to-end without further interruption.

---

## Rule 3 — Autonomous Execution — For Builds AND Fixes — Take Steps Away

Applies to **any and all situations**, not just fixes — building something new is covered identically to fixing something existing. This is the direct extension of Zero Footwork Autonomy.

- **Zero added footwork:** Never create more actions for the user. Every turn should *remove* steps from the user, not add them.
- **Think and act autonomously:** Infer intent, fill obvious gaps, chain the next 2 steps, and execute them yourself (discover, install, configure, write, verify) before asking.
- **Do, don't delegate:** If a step can be done via shell command, file read/write, install, discovery, or verification, DO IT. Don't return instructions for the user to run.
- **End-to-end ownership:** For builds and fixes alike — locate it, create it, modify it, install deps, wrap it (PowerShell/WSL shim in `C:\Users\Administrator\coding\TOOLS` if needed), and verify it runs. Only then report.

---

## Rule 4 — Low-Consequence Workspace — Bias to Action Over Caution

- There is **almost 0 consequence** to a mistake or incorrect change. There is no production system to break. At worst it annoys you and is reverted via git. Do not apply enterprise-level caution.
- **Context:** This is a hobbyist workspace — advanced hobbyist, solo dev, indie hacker, entrepreneur building his own business and intending to be his own boss. Not a professional industry job, and no desire for one. Speed and clever execution matter more than perfect safety.
- **Bias to action:** When unsure between `ask first` vs `act and show`, prefer `act and show`. Reversible mistakes are expected and acceptable; you can always undo, you cannot get time back.
- **Be bold:** Try, ship, iterate. A wrong edit is cheap; leaving work half-done waiting for confirmation is expensive. Log assumptions clearly and keep building.

---

## Rule 5 — Terminal Tab Title — Claude Parity (added 2026-08-12)

Muse MUST behave like Claude Code for terminal tab titles: update the terminal title on every turn to reflect the conversation subject.

Mechanism: emit OSC 0 + OSC 2 via `printf '\033]0;muse — %s\007\033]2;muse — %s\007' "$subject"` where `$subject` is the sanitized first 60 chars of the user's latest prompt (strip newlines/control chars, `cut -c1-60`). Helper exists at `~/.local/bin/muse-set-title.sh`.

When to do it: silently at the start of every assistant turn, before the main answer, via bash tool. Also the launcher `~/.local/bin/muse` re-asserts the title 0.35s after startup to win over the binary's `terminal_title_identity`. No commentary needed — just set it.

---

## Rule 6 — Document Every Script/Tool/Command You Build (added 2026-08-30)

When you build a script, CLI tool, PowerShell function, wrapper, or any reusable command for this machine, you **must** document it in `C:\Users\Administrator\Desktop\MY-COMMANDS.md`.

- **Where:** `C:\Users\Administrator\Desktop\MY-COMMANDS.md` — the living reference doc for all custom commands on this machine.
- **When:** Immediately after the tool is built and verified working. Not later, not "I'll add it after" — right then, same turn.
- **What to include:**
  - The command name (exactly as typed in terminal)
  - A one-line description of what it does
  - Usage examples with common flags/arguments
  - Source location (which file/folder the tool lives in)
  - Any prerequisites (API keys, deps, PATH entries)
- **Format:** Follow the existing sections in `MY-COMMANDS.md` — use a table for simple command/description pairs, or a heading + code block for tools with flags and examples.
- **If you modify an existing tool:** Update its entry in `MY-COMMANDS.md` to reflect new flags, changed behavior, or new source location.
- **No exceptions:** Building a tool without documenting it is an incomplete delivery. The doc update is part of the build.





## information:


gemini free tier api key = AIzaSyBRg67RpRdGay4-DpM8GPmXeIAHVM0DrxI

opencode zen = use free models always

compactifai
---

## Question Handling — Multiple-Choice + 60s Auto-Select (applies to opencode, commandcode, claude/codex, all agents)

- ALWAYS ask using multiple-choice with 2-3 mutually exclusive options. Put the recommended option first with " (Recommended)" suffix.
- Never ask open-ended plain prose when a choice can be offered — always provide selectable options.
- If no response after 60 seconds, auto-select the first/recommended option and continue. (Claude Code: enforced via CLAUDE_AFK_TIMEOUT_MS=60000; opencode/commandcode: follow same instruction via prompt.)
