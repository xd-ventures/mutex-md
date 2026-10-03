# MUTEX.md: coordination of autonomous coding agents through a shared text file

Status: Informational. Version 0.1, October 2026.
Author: Maciej Sawicki
Origin: Warsaw Model Trainers Hackathon, 25–27 September 2026 (17 agents, 46 hours, one file, 512 lines)
Canonical copy: https://mutex.md · Source and history: https://github.com/xd-ventures/mutex-md

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
- A second instance MAY live on each shared machine (for example a GPU box), with its own scope. There, agents of several principals meet, so the file SHOULD be edited through a small claim/release wrapper that serializes writes (`flock`) and owners SHOULD carry the principal's name: `maciej-claude`, `radek-codex`. In the words of the wrapper's own comment: "everyone is root here, so say it".
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
- A claim whose owner has gone silent is released only by a principal. The requesting agent posts the ask with a timestamp; the principal's decision is recorded in the same line. On a shared machine a fixed rule works better: a claim older than three hours with no running process MAY be removed by anyone who writes a Log line about it.
- Static allocation beats locking where it fits: one port range per principal (8890–8929 and 8930–8969, one Ollama port each) removed a whole class of claims.
- Agents MUST NOT kill another agent's process, whoever it belongs to.
- Namespace collisions (two agents minting `D003`) are settled in writing: one takes the next free number, the other keeps its number and adjusts the title.

## 6. Bootstrap

The whole protocol was started with one sentence given to each agent:

> Another agent is working on <task> in this repository; avoid conflicts. If you need to lock a folder or a resource, coordinate with the other agents through MUTEX.md. You are <name>.

Everything in sections 3–5 was established by the agents themselves and later carried in their own memory files.

## 7. Security considerations

There are none, and that is the point to understand before use:

- No identity: an agent is whoever it says it is. Two agents of two people carried the same name for a day and nobody noticed until the audit.
- No enforcement: a claim is a line; anyone can delete it.
- No atomicity: two concurrent writes to one Markdown file are a race, unless a wrapper serializes them, and then only for the table it manages.
- No verification: "GPU free" is a statement, not a measurement.

The file works when all agents share a goal and a deadline. With conflicting goals it is an arena. What it does provide is an audit trail: who, when, what and why, in the agents' own words.

## 8. What this is not

Not a lock manager, not a scheduler, not an orchestrator. A social contract in Markdown, suitable for a weekend of trusted agents and not for production.

## 9. Contributing

The text lives in a public repository: https://github.com/xd-ventures/mutex-md. The site is built from `mutex-md-spec.md` on the `main` branch.

- A correction, a counter-example or a rule that worked for you: open an issue or a pull request against `mutex-md-spec.md`. One change per pull request; say which section it touches and what you observed.
- A report from your own workspace (how many agents, which tools, what collided, what the file looked like afterwards) is the most useful kind of contribution. Verbatim quotes beat summaries.
- Requests follow the format of section 3: `[you → maintainer] what / why`. Status is set by the maintainer. There is no lock on any section; edits to the same paragraph are resolved the way section 5 says.
- Version numbers move when a MUST changes. Everything else is a patch.

## Appendix A. Minimal example (workstation variant)

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

## Appendix B. Shared-machine variant (header as written by the agents)

```markdown
# MUTEX — shared resources on white

- Before you use a GPU, a port, a shared path or the submission folder, claim it with
  `bin/mutex claim <owner> <resource> <purpose>`. When you are done, release it with
  `bin/mutex release <owner> <resource>`. See who holds what with `bin/mutex show`.
- One resource per line. Keys: `gpu0`, `gpu1`, `port:<n>`, `path:<dir>`, `submission`.
- If a resource is claimed by someone else: wait, pick another (other GPU / port range), or ask the holder
  (write under "Requests" and ping them). Never kill someone else's process.
- Claims older than 3 hours with no running process may be removed by anyone — write a line under "Log" when you do.
- Edit by hand only under "Requests" and "Log"; the table is managed by the `mutex` command (it locks the file).
```

The wrapper is 50 lines of bash: `show`, `check`, `claim`, `release`, `flock` on a sidecar lock file, and a `TZ` line so that at least one of the two files agrees with itself about the time.
