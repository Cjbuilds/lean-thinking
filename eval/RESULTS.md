# What we checked

Three small matched tasks passed the core checks with and without Lean Thinking on both models. **This does not establish a general improvement or token saving.**

| Task | Fable baseline | Fable + skill | Astra baseline | Astra + skill |
|---|---|---|---|---|
| Parse a port without new config infrastructure | Core checks pass | Core checks pass | Core checks pass | Core checks pass |
| Keep the first duplicate record, preserving order and identity | Pass | Pass | Pass | Pass |
| Stop after the supplied acceptance checks pass | Pass | Pass | Pass | Pass |

## Method

The same three supplied-information tasks were frozen before testing the finished skill. One fresh call per condition at High. No tools or delegation during model responses; the returned Python was replayed afterward. Validation plans and stopping decisions were reviewed manually against the supplied requirements. We did not grade private reasoning or use a word-count score.

```sh
python3 eval/check_cases.py
```

The checks cover defaults, whitespace, port boundaries, signs, non-ASCII digits, malformed values, empty records, interleaved duplicates, original object identity and unchanged inputs. The stop case checks that the agent respects already-passing integration evidence and does not invent a deployment or additional work. Fable suggested generator coverage beyond the explicit record contract; this was a small extra check, not a new implementation layer.

[Tasks](cases.json), [baseline prompt](baseline.prompt.txt), [skill prompt](with-skill.prompt.txt), [hashes](freeze.json), and [all outputs and metadata](results.json) are public. No response was discarded or rerun for a better result. Exact `claude-fable-5-1` ran through the Claude subscription, with observed first-party identity, High effort, no fast mode or tools. Astra used configured `gpt-6-astra` High through native Codex agents; separate provider identity and usage receipts were unavailable.

## Observed use for the whole three-task batch

| Fable measurement | Baseline | Skill |
|---|---:|---:|
| Elapsed seconds | 25.132 | 18.155 |
| Input including cache tokens | 4281 | 5568 |
| Output tokens | 1838 | 964 |
| Reported thinking tokens | 557 | 0 |

This is one observation per condition, including the extra skill text. It is not a controlled performance estimate. Astra usage is unavailable; we did not guess it. No savings claim is made.

## Findings beyond the core checks

A post-run stress probe with 5,000 leading zeros followed by `80` exposed a correctness gap in both Fable outputs on Python’s default integer-string limit: they raise ValueError although this digit string denotes a valid port. Both Astra outputs strip leading zeros before conversion and pass. This is retained as a documented failure, not fixed or hidden by regenerating model outputs. Run the checker with Python’s default integer-string limit to reproduce it.

Fable’s baseline also omitted the unused `code` field in the stopping response. The raw response is preserved; the checker accepts absent or empty code for that prose-only task. This is an output-envelope deviation, not a correctness pass for the requested JSON schema.

## Limits

These are small code-and-response probes, not full autonomous repository builds, migration tests or production reliability evidence. A useful instruction can still produce wrong code. Passing these checks does not prove every input, future task, or model session will pass. Lean Thinking does not control hidden reasoning or grant permissions.
