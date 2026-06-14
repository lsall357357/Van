# 早期项目问题定位助手

`early-stage-startup-problem-finder` is a universal AI skill for early-stage startup problem location. It is designed for Codex, Claude Code, OpenClaw, and other agents that can load a standard `SKILL.md` skill directory.

It helps founders and early financing professionals locate where an idea, BP, fundraising material, or investor conversation may get stuck. It is most useful from idea stage through Series A and pre-Series-A preparation.

## What It Does

- Reviews startup ideas, BP text, decks, one-pagers, memos, and pasted project descriptions.
- Reads available material first, then asks one material-grounded intake round.
- Locates problems in the value anchor, business model, fundraising story, BP structure, investor blockers, meeting risks, and funding path.
- Lists investor questions without providing answer templates.
- Keeps follow-up discussions tied to the user's original material and diagnosed issues.
- Gives search-query suggestions when current public facts are needed but search is unavailable.

## What It Does Not Do

- Write BP copy or page-ready rewrites.
- Write fundraising story copy.
- Provide investor answer templates or meeting scripts.
- Provide valuation, dilution, deal, legal, tax, securities, investment, or fundraising-success advice.
- Help fabricate evidence, conceal risk, mislead investors, or evade rules.

## Installation

### Codex

Copy the full folder into:

```text
~/.codex/skills/early-stage-startup-problem-finder
```

Keep `SKILL.md`, `references/`, `agents/`, `scripts/`, and `examples/` together.

### Claude Code

Copy the full folder into the skills or workspace location your Claude Code setup reads from. The required entrypoint is `SKILL.md`; the reference files under `references/` must stay in the same relative location.

### OpenClaw

Copy the full folder into the OpenClaw workspace skills directory. Do not flatten the `references/` directory.

### Generic Agents

Load `SKILL.md` first. When the instructions mention a reference file, read that file from `references/` before answering.

## Example Prompts

```text
我有个创业想法，帮我看看有没有问题
```

```text
帮我看 BP 哪里会被投资人卡住
```

```text
投资人可能会问什么
```

```text
我的价值锚点清不清楚
```

```text
BP 第一页帮我看哪里不清楚
```

```text
估值开多少合适
```

## Expected First-Step Behavior

For a normal project request, the assistant should not immediately diagnose. It should first read the material already provided by the user, then ask one short intake round based on project facts and material gaps.

The user can skip the questions and ask the assistant to start directly. The assistant should then diagnose based on the available material and mark judgment limits.

## Validation

Run:

```bash
python3 scripts/validate_skill.py .
```

Optional package build:

```bash
python3 scripts/package_skill.py .
```

The packaging script creates a zip in `dist/` and excludes local caches, system files, private listing files, and generated archives.

## Privacy And Safety

This package contains no external links, API clients, network calls, crawlers, or upload code. Material handling depends on the host assistant and tools that load the skill.

Before sharing materials, remove unnecessary sensitive information such as personal IDs, phone numbers, customer lists, bank accounts, credentials, private keys, contracts, and unpublished financial details.

See `SECURITY.md` for refusal boundaries and reporting guidance.
