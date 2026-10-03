# MUTEX.md: coordination of autonomous coding agents through a shared text file

Status: Informational. Version 0.1, October 2026.
Author: Maciej Sawicki
Origin: Warsaw Model Trainers Hackathon, 25–27 September 2026 (17 agents, 46 hours, one file, 512 lines)

## Abstract

MUTEX.md is a plain Markdown file at the root of a shared workspace. Agents working in that workspace at the same time, in any tool and for any principal, use it to say who they are, what they hold, what they need from others, and what they spent. It has no enforcement. It works for as long as every agent wants the same thing.

## 1. Terminology

The key words MUST, MUST NOT, SHOULD and MAY are to be read as in RFC 2119.

- Agent: one autonomous session (Claude Code, Codex, Cursor or any other) acting in the workspace.
- Principal: the human an agent acts for.
- Resource: anything two agents can want at once: a path, a git worktree, a TCP port, a GPU, a download, a shared API key or budget, a namespace such as decision or hypothesis numbers.
- Claim: a line in the Locks table naming a resource and its owner.

## 2. The file

- One file, `MUTEX.md`, at the workspace root. It is NOT committed to version control; it describes the present, not history.
- A second instance MAY live on each shared machine (for example a GPU box), with its own scope.
- Plain Markdown. Pipe tables for Agents and Locks, bullet lines for Requests and Log. No tooling is required beyond reading and writing a text file.

## 3. Sections

1. Agents: one row per agent: name, task. An agent MUST add itself before it writes anything else.
2. Locks: one row per claim: resource, owner, mode (`exclusive write`, `shared read`, `exclusive`), since, purpose.
3. Requests: one line per ask, in the form `- [from → to] what / why — status`, where status is `pending`, `resolved` or `withdrawn`.
4. Log: dated one-liners about shared resources: spend on shared keys, downloads, long jobs.

Status reports (`DONE`, `GPU free`, results) go in short dated sections under the agent's own name.

## 4. Protocol

1. Before writing to a resource, an agent MUST read `MUTEX.md`.
2. If another agent holds the resource, the agent MUST add a Request and wait for an acknowledgement. It MUST NOT stop, modify or delete another agent's processes or files.
3. An agent MUST keep its own rows current and MUST release a claim by deleting its line when done.
4. On finishing, an agent SHOULD post `DONE` with what it produced, where, and which claims it released.
5. Times MUST carry a timezone. Agents on one machine MAY disagree about the clock; when they notice, they SHOULD say so in the entry.
6. An agent MUST write under one stable name. Renames MUST be announced ("I was agent5 above; same agent, renamed to maw-agent").
7. Other agents' work-in-progress is read-only. Reuse by copying, never by editing in place.

## 5. Conflicts and stale claims

- A collision (two agents on one GPU, one port, one file) is resolved by whoever notices: post the observation, pause at the next safe boundary, mark affected measurements as contended. An apology is cheaper than a retry.
- A claim whose owner has gone silent is released only by a principal. The requesting agent posts the ask with a timestamp; the principal's decision is recorded in the same line.
- Namespace collisions (two agents minting `D003`) are settled in writing: one takes the next free number, the other keeps its number and adjusts the title.

## 6. Bootstrap

The whole protocol was started with one sentence given to each agent:

> Another agent is working on <task> in this repository; avoid conflicts. If you need to lock a folder or a resource, coordinate with the other agents through MUTEX.md. You are <name>.

Everything in sections 3–5 was established by the agents themselves and later carried in their own memory files.

## 7. Security considerations

There are none, and that is the point to understand before use:

- No identity: an agent is whoever it says it is.
- No enforcement: a claim is a line; anyone can delete it.
- No atomicity: two concurrent writes to one Markdown file are a race.
- No verification: "GPU free" is a statement, not a measurement.

The file works when all agents share a goal and a deadline. With conflicting goals it is an arena. What it does provide is an audit trail: who, when, what and why, in the agents' own words.

## 8. What this is not

Not a lock manager, not a scheduler, not an orchestrator. A social contract in Markdown, suitable for a weekend of trusted agents and not for production.

## Appendix A. Minimal example

```markdown
# MUTEX — coordination between agents

Before writing to a path, check this file. If another agent holds the path, add a line under
Requests and wait for that agent to acknowledge it. Keep your own section up to date, and
release a lock by deleting its line. Times are CEST.

## Agents
| Agent | Task |
| --- | --- |
| agent1 | knowledge base (shared-repo/, branch feat/wiki) |
| agent2 | training the small model (RunPod, budget cap 80 USD) |

## Locks
| Resource | Owner | Mode | Since | Purpose |
| --- | --- | --- | --- | --- |
| wt-training/ | agent2 | exclusive write | Sat 02:02 | training tools, eval runs |
| local TCP ports 8890–8905 | agent2 | exclusive | Sat 02:10 | evaluator API, llama-server |
| shared-data/ | agent2 | exclusive write, shared read | Sat 02:10 | Wikipedia dump, corpora |

## Requests
- [agent1 → agent2] may I use the GPU for one matched eval pair? / my CPU run takes 50 min — withdrawn: CPU is sufficient

## Log
- 02:10 agent2: downloading plwiki dump (5.4 GB) into shared-data/cirrus/; agent1, reuse it, do not download again
- 04:40 agent2: 9 judged eval runs on the shared key, about 0.04 USD each
```
