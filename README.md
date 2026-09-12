![Lean Thinking banner](assets/banner.png)

# lean-thinking

Lean Thinking helps AI coding agents stay focused and finish the job. It tells them to plan enough, build what is needed, check the result, and stop.

Use it when an agent spends too long planning, keeps adding extra work, or rebuilds things that already work. Simple tasks stay simple. Risky tasks still get the checks they need.

## How it works

- Understand the task first.
- Make a simple plan.
- Reuse what already works.
- Build only what is needed.
- Check that it works.
- Fix any problems found in the task.
- Stop when it is done and checked.
- Explain what changed and any remaining limits.

It follows your requirements and asks for permission when needed. It does not skip necessary work just to make the answer shorter.

## Install

Clone this repository, then copy the skill folder into your project:

```sh
git clone https://github.com/Cjbuilds/lean-thinking.git
```

Replace `/path/to/lean-thinking` below with the clone location. Review an existing installed copy before replacing it.

For Codex:

```sh
mkdir -p .agents/skills
cp -R /path/to/lean-thinking/skills/lean-thinking .agents/skills/
```

For Claude Code:

```sh
mkdir -p .claude/skills
cp -R /path/to/lean-thinking/skills/lean-thinking .claude/skills/
```

## Use

Invoke it by name in a request:

```text
Use $lean-thinking to add CSV export to this report page.
```

The agent reads the relevant code, makes a plan, does the work, and checks the result.

## Check the package

The checker uses only the Python standard library:

```sh
python3 scripts/check.py
```

It validates the skill metadata and package structure, required installation instructions, and local README links.

## Files

```text
lean-thinking/
├── assets/
│   └── banner.png
├── eval/
│   └── RESULTS.md
├── scripts/
│   └── check.py
├── skills/
│   └── lean-thinking/
│       └── SKILL.md
├── LICENSE
└── README.md
```

## What the tests showed

We tested Fable 5.1 and GPT-6 Astra on three small tasks, with and without the skill. Both models passed the same core checks in both conditions.

In the recorded Fable test batch, output tokens fell from 1,838 to 964 with the skill. Input tokens, including cached tokens, rose from 4,281 to 5,568. Total input plus output tokens therefore increased. Astra's token usage was not available.

This small test does not prove token savings. Passing the same core checks also does not prove that output quality stays the same on every task. An extra stress test found a bug in both Fable versions.

See the [full test results and limits](eval/RESULTS.md).

## Limits

This skill cannot recover missing evidence, grant permissions, or make risky changes safe. Its result still depends on the agent's tools, available context, and judgment. It does not promise to control private reasoning or reduce token use.

## License

[MIT](LICENSE). Use it, adapt it, and share it.
