<h1 align="center">WinrarPassWordCrackerByLoko V2</h1>
<p align="center"><strong>Concurrent, series-based RAR password recovery — built with Python</strong></p>
<p align="center">🚧 <strong>Under active development — V2 is a foundation, not a working concurrent cracker yet.</strong> 🚧</p>

![Project banner](Docs/banner.png)

## Overview

**WinrarPassWordCrackerByLoko V2** is an educational, open-source Python project to recover passwords from **RAR archives you own or are authorized to access**. Its design goal is to test password candidates using a **fixed number of concurrent worker threads**, assigning each thread its own non-overlapping mathematical series.

V1 used a sequential engine. V2 is a **fresh implementation informed by V1**, preserving useful ideas (termite colonies, dependency injection, clean interfaces, RAR validation, and recoverable work) while redesigning execution and persistence for concurrency. This repository currently contains only part of the foundation; the capabilities described below are **planned unless explicitly marked otherwise**.

> **Project status (October 2026):** V2 scaffold exists, including the entry point, core configuration/logging infrastructure, controller, and selected earlier components/contracts. The concurrent engine, per-worker checkpoints, and shared completion signal are **not implemented yet**. See [Development roadmap](#development-roadmap).

## The idea: termite colonies + mathematical series

The project models each password candidate as a **termite**, and candidates of the same password length as a **colony**. A worker thread processes a unique sequence of termite indices. Only one colony length is active at a time.

Given:

- `W`: effective number of workers, fixed when a recovery job is created;
- `k`: worker ID, from `0` to `W - 1`;
- `n`: iteration number, starting at `0`;
- `i`: candidate index within the current colony;

we assign work using:

\[
i = Wn + k
\]

**Example: two workers**

| Worker | Mathematical series | Candidate indices |
| --- | --- | --- |
| 0 | `2n` | `0, 2, 4, 6, 8, ...` |
| 1 | `2n + 1` | `1, 3, 5, 7, 9, ...` |

**Example: three workers**

| Worker | Mathematical series | Candidate indices |
| --- | --- | --- |
| 0 | `3n` | `0, 3, 6, 9, ...` |
| 1 | `3n + 1` | `1, 4, 7, 10, ...` |
| 2 | `3n + 2` | `2, 5, 8, 11, ...` |

With `W = 1`, the same concurrent engine launches **one worker thread** and visits `0, 1, 2, ...`. There will be **no separate sequential attack mode**.

### Why do the series never collide?

Suppose two workers produce the same index:

`W*n1 + k1 = W*n2 + k2`.

Then `W*(n1 - n2) = k2 - k1`. Because both worker IDs are between `0` and `W - 1`, the right-hand side has absolute value less than `W`. The only multiple of `W` in that range is zero, so `k1 = k2` and `n1 = n2`. Thus **each index belongs to exactly one worker**.

Coverage is also complete: for any index `i >= 0`, choose `k = i % W` and `n = i // W`; then `i = Wn + k`.

For a character set of size `C` and candidate length `L`, the colony contains `M = C^L` candidates, with valid indices `0 <= i < M`. Workers stop when their series reaches or exceeds `M`.

**Important:** mathematical uniqueness prevents duplicate assignments *within one correctly configured job*; it does not by itself guarantee safe checkpoints, file operations, or recovery after failures. Those are separate engineering requirements.

## Planned capabilities

- **Concurrent-by-default execution:** Python threads coordinate independent calls to the external `UnRAR.exe` process.
- **Configurable concurrency:** `TERMITES_CONCURRENCY_ATTACK` sets the requested worker count; the design hard-caps it at **8**, using the effective count in the persisted job. Values below 1 or nonnumeric values will be rejected.
- **Immutable worker count:** restarting a job with a different effective `W` will be rejected rather than silently redistributing candidates.
- **Series-based scheduling:** each worker owns `Wn + k` indices, one candidate at a time within its series.
- **Direct candidate lookup:** derive the password represented by an index without enumerating all preceding combinations (base-`C` conversion).
- **Colony lifecycle:** complete all assigned series for a length before advancing to the next length.
- **Recoverable execution:** `TEMP/work.json` schema V2 will track archive identity, character set, password lengths, immutable worker count, and **per-worker checkpoints**.
- **Single-writer persistence:** the coordinator will serialize state changes and write JSON atomically.
- **Shared success signal:** `threading.Event` will notify live threads; a separate `TEMP/attack.signal` file (planned values `0`/`1`, associated with the current job) will persist completion state. It is **not** a substitute for checkpoints.
- **Graceful cancellation:** finding a valid password will stop new attempts and coordinate completion of in-flight work.
- **Clear validation outcomes:** distinguish valid password, invalid password, and technical error; do not advance a checkpoint on a technical error.
- **Termite lifecycle:** the original `.txt` termite idea is being evaluated for on-demand generation instead of creating millions of files upfront.
- **Logging, tests, and performance benchmarks:** test exclusivity, completeness, interruption/restart, and measurable throughput.

### Recovery principle

Each worker stores the **last durably confirmed index** from its own uninterrupted series. If worker `k` completed index `i`, its next candidate is `i + W`; if it has no confirmed candidate yet, it starts at `k`.

Example with `W = 3`:

| Worker | Last confirmed | Next index |
| --- | ---: | ---: |
| 0 | 12 | 15 |
| 1 | 10 | 13 |
| 2 | 8 | 11 |

A crash may cause a candidate to be **retried** if confirmation was not saved; **skipping an unverified candidate is unacceptable**. The presence or absence of a termite `.txt` alone is not sufficient proof that its password was checked.

## Target architecture (planned)

We are retaining the **Application / Infrastructure separation**, with contracts defined in Application and implementations in Infrastructure. The following tree represents the **target design**, **not a claim that all these files exist today**:

```text
WinrarPassWordCrackerByLokoV2/
├── main.py
├── .env                         # local configuration (not committed)
├── .env.example                 # planned shareable template
├── characters.txt               # planned input character set
├── requirements.txt
├── CLAUDE.md                     # planned project instructions
├── Docs/
│   ├── banner.png               # optional project artwork
│   ├── Backlog.txt               # development tasks
│   └── ConcurrentSeriesDesign.txt
├── INPUT/                        # local test RARs
├── OUTPUT/                       # local results and logs
├── TEMP/                         # work.json, attack.signal, termite artifacts
├── src/
│   ├── CORE/
│   │   ├── Config.py
│   │   ├── Logger.py
│   │   ├── FolderController.py
│   │   └── DependencyInjector.py
│   ├── Models/
│   │   ├── Entities/
│   │   │   ├── WorkState.py
│   │   │   ├── WorkerState.py
│   │   │   └── ColonyState.py
│   │   └── Enums/
│   │       ├── WorkStatus.py
│   │       ├── WorkerStatus.py
│   │       └── PasswordTestResult.py
│   ├── Application/
│   │   ├── repositories/IWorkRepository.py
│   │   ├── services/
│   │   │   ├── IBruteForceService.py
│   │   │   ├── IWorkerService.py
│   │   │   ├── IPasswordCombinationService.py
│   │   │   └── IAttackSignalService.py
│   │   └── use_cases/
│   ├── Infrastructure/
│   │   ├── repositories/JsonWorkRepository.py
│   │   └── services/
│   │       ├── CRACKER/
│   │       │   ├── ConcurrentBruteForceService.py
│   │       │   └── TermiteWorkerService.py
│   │       ├── GENERATORS/PasswordCombinationGenerator.py
│   │       ├── WINRAR/WinrarService.py
│   │       ├── TERMITES/TermiteService.py
│   │       └── SIGNALS/AttackSignalService.py
│   └── controllers/Controller.py
└── tests/
    ├── unit/
    └── integration/
```

The folder layout and exact contracts may evolve as we build and test the software. Existing V1 code is reused only after it is adapted to the V2 invariants.

## Planned configuration

The following is an **illustrative target configuration**, not a promise that all variables are supported by the current scaffold:

```dotenv
RAR_FILE_TO_CRACK="INPUT/123.rar"
UNRAR_SOFTWARE_FILE_PATH="UnRAR.exe"
GEN_CONFIG_CHARACTERS_ARR_INPUT_FILE="characters.txt"
GEN_CONFIG_LEN_MIN_SIZE_CHAR_SELECT_TO_CRACK="2"
GEN_CONFIG_LEN_MAX_SIZE_CHAR_SELECT_TO_CRACK="4"
TERMITES_CONCURRENCY_ATTACK="2"
```

The V2 design sets `MAX_TERMITES_CONCURRENCY = 8` in code. If a user requests more than eight workers, the effective worker count will be capped at eight and logged as a warning. The **effective** count is immutable once the job is created.

For example, with digits `0–9` and lengths `2–4`, there are `10^2 + 10^3 + 10^4 = 11,100` candidate passwords across three colonies. This count is a search-space illustration, not an estimated completion time.

## Requirements and installation (development target)

- **Windows** and **Python 3**. The prior version was developed on Windows 11; V2 compatibility must be verified.
- **WinRAR / UnRAR.exe**, obtained separately from the official vendor. The executable is **not bundled** with the project. See [RARLAB](https://www.rarlab.com/).
- Project dependencies specified in `requirements.txt` as development progresses.

Once the new engine is implemented, the intended setup is:

```powershell
python --version
python -m pip install -r requirements.txt
# Copy .env.example to .env and configure your own archive and charset.
# Provide a licensed, locally available UnRAR.exe path.
python main.py
```

**Do not expect this command to perform concurrent password recovery yet.** The current V2 repository is still being built. The application will be considered usable only after its integration tests pass.

## Development roadmap

| Milestone | Goal | Status |
| --- | --- | --- |
| 1. Foundation and domain | Fix scaffold, configuration, `WorkState` V2 and `WorkerState` | Planned |
| 2. Mathematical series | Implement `Wn + k` and direct index-to-password mapping | Planned |
| 3. Durable recovery | Per-worker checkpoints, single writer, archive/job identity | Planned |
| 4. Concurrent engine | Thread pool, worker lifecycle and safe RAR validation | Planned |
| 5. Shared stop signal | `attack.signal`, `threading.Event`, graceful cancellation | Planned |
| 6. Integration and cleanup | Wire dependencies and retire sequential-only concepts | Planned |
| 7. Validation | Race-condition, crash-recovery, and benchmark tests | Planned |

The detailed backlog uses **AC01–AC42** task IDs. Technical completion will require coverage and exclusivity proofs **and** passing integration tests; no performance improvement is assumed without benchmarks.

## Why Python threads?

The objective is not to execute Python bytecode in parallel for its own sake. Python orchestrates multiple **external `UnRAR.exe` subprocesses**. The traditional CPython GIL does not prevent multiple external programs from running simultaneously. The optimal number of workers is hardware- and workload-dependent; more threads do not necessarily mean a faster attack.

## Responsible use

This project is for **learning, experimentation, and recovery of archives you own or have explicit permission to access**. Password search may be expensive and is not guaranteed to find a password outside the configured character set and length range. Do not use the tool on third-party archives without authorization. Be mindful of CPU, storage, and process limits.

## Technology

Python · `threading` / `concurrent.futures` (planned) · `subprocess` · JSON persistence · mathematical combinatorics · hexagonal architecture · UnRAR.exe (external dependency)

## Author

Developed by **[FelipedelosH](https://github.com/felipedelosh)**.

---

*V2 is a rebuild of the execution engine, not a claim that the concurrent algorithm is already complete. Contributions and issue reports are welcome as the milestones are implemented.*
