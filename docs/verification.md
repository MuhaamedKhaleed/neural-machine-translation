# Verification record

## Scope and behavior changes

The original repository contained one experimental translation notebook, no reusable package or tests. Notebook output was removed, overlapping preprocessing cells consolidated, target tokenizer mode used, labels padded by a seq2seq collator with `-100`, obsolete Trainer argument names updated to Transformers 4.49, and an unused classification-accuracy loader removed. The notebook's full online workflow remains unrerun. Its historical dependencies/download cells are not the supported package install path.

The new CLI is an explicit, local-only CPU path. It does not silently start notebook training. It rejects normalized duplicate sources, uses source-disjoint train/validation pairs, and refuses existing output folders or pickle weights. These are deliberate validation and interface changes, not a claim of byte-for-byte notebook outputs. Runtime/API guards do not establish that arbitrary artifacts are safe; use trusted local files.

## Commands and results

Run from the repository after `uv sync --locked --extra dev --extra ml`:

| Check | Result |
| --- | --- |
| `HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 OMP_NUM_THREADS=1 uv run pytest --cov=local_translation --cov-report=term-missing` | 24 passed, 96% statement coverage |
| `uv run ruff check src tests` | Passed |
| `uv run ruff format --check src tests` | Passed |
| `uv run mypy src` | Passed, strict package checks |
| `uv run pre-commit run --all-files` | Passed |
| `uv run local-translation check-data --data examples/parallel.csv` | 3 pairs, 2 training, 1 validation |
| `uv run local-translation check-data --config .env.example` | Same JSON |
| `uv run python -m local_translation --help` | Passed |

A fresh light-only locked install also runs the data CLI without Torch; its model test module is skipped, explicitly. The offline test builds a miniature Marian configuration, a tokenizer trained only on six invented lines, and random weights. It checks actual forward/backward, ignore-label padding, target mode, generation, one-epoch training, CLI and local reload. Loss is teacher-forced and token-weighted. Random-model generation has no linguistic meaning and is not a pretrained model evaluation.

Container verification is performed by hosted CI, not by a local Docker daemon. CI builds the exact Dockerfile and runs help plus mounted parallel-CSV checks in the non-root light image. It uses pip/direct dependency pins rather than claiming uv's full lock. No credentials, paid services or training artifacts are required. A private-repository workflow is skipped to avoid billable Actions assumptions.

## Phase accounting

1. Installable src package and explicit module/console entry points.
2. Typed CSV/split, ML adapter, thin CLI; no unused helpers.
3. Validation, separate stderr logging, nonzero expected-error exits.
4. Opt-in dotenv, example only, caches/env/model outputs ignored.
5. Runtime/dev/ML dependency groups and scoped uv lock.
6. Offline meaningful data, CLI and actual synthetic ML tests.
7. Ruff, mypy and pre-commit commands.
8. Public-only CI with pip caching and pinned action revisions.
9. Multi-stage non-root data-only image, hosted build/run validation.
10. Explicit check-data, train and translate commands.
11. Working example output, architecture and honest limits.
12. Review branch and changelog. No main merge, release or tag.
13. Copy-only repo metadata and profile snippet, not applied to account settings.

No license change, real corpus, checkpoint or model publication. Main remains separate. Generic web-editor file commits are not a fabricated phase-perfect Conventional Commit history. Notebook bug fixes and reusable-package work are separate logical changes locally; remote commits remain inspectable rather than squashed into a fake original history.

## Still unverified

Real pretrained English/German translation quality; full notebook/WMT16 run; BLEU/chrF; human error review; domain/document-independent held-out quality; GPU, Windows, macOS or ARM behavior; production serving, throughput, resource exhaustion safeguards and atomic multi-file artifact writes. Large local CPU training needs its own time/resource decision.

Reference checked: https://huggingface.co/docs/transformers/v4.49.0/en/tasks/translation . It supports target text tokenization and seq2seq label-padding mechanics, not any claim about this project's model quality.
