# Local Marian Translation

A local-only CLI for checking parallel CSV data, running an existing Marian translation model, and deliberately starting CPU fine-tuning. This engineering pass extracts usable code from an experimental English/German translation notebook and fixes target-tokenization and padding problems. No pretrained model or corpus is bundled.

## Quick start

Python 3.11 or 3.12, Linux x86_64. Install uv first using its official instructions, then:

```sh
uv sync --locked --extra dev
uv run local-translation --help
uv run local-translation check-data --data examples/parallel.csv
uv run local-translation check-data --config .env.example
```

Actual example output:

```json
{"pairs": 3, "train_pairs": 2, "validation_pairs": 1}
```

`source,target` are required UTF-8 CSV headers. Other uniquely named columns are allowed. Blank pairs, malformed rows, and repeated case/whitespace-normalized source sentences fail rather than being silently dropped. `--config` is an opt-in dotenv file with `PARALLEL_CSV`; explicit `--data` wins. No credentials or service calls are needed.

The lock is scoped to Linux x86_64. Other operating systems are not verified. The ordinary install and Docker image provide **data checks only**, with no Torch import. Optional ML dependencies are much larger:

```sh
uv sync --locked --extra dev --extra ml
```

## Local model workflow

`translate MODEL TEXT...` and `train MODEL DATA OUTPUT` require the optional `ml` extra and a trusted local Marian directory containing tokenizer/config files and safetensors weights. Both loading calls use `local_files_only=True`; no model is selected or downloaded automatically. Pickle model weights and remote-code loading are not supported. Do not point at untrusted artifacts.

Use `local-translation translate --help` and `local-translation train --help` for arguments. The tested end-to-end example is the synthetic offline test below, not a downloaded model demonstration. A user-supplied pretrained model's language direction and license remain the user's responsibility.

- CPU-only inference, deterministic beam search, bounded input count and lengths.
- Target tokenizer mode, dynamic batch padding, target pad labels set to `-100`.
- Seeded source-disjoint split before fitting. Normalized duplicates are rejected.
- Explicit training with finite-loss checks; no auto-training on import or overwrite of existing output directories.
- Token-count-weighted teacher-forced validation loss, not BLEU or a translation-quality claim.

The model/tokenizer architecture comes from the supplied local artifact. The historical notebook used Helsinki-NLP Marian English-to-German and WMT16; the CLI does not fetch either. Truncation can discard long-text information. Source-disjoint splitting is not document/source/domain independence and is not an untouched evaluation set.

## Checks

```sh
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 OMP_NUM_THREADS=1 uv run pytest --cov=local_translation --cov-report=term-missing
uv run ruff check src tests
uv run ruff format --check src tests
uv run mypy src
uv run pre-commit run --all-files
uv run python -m local_translation --help
```

With the ML extra: **24 tests, 96% coverage**, including actual tiny random Marian forward/backward, local synthetic SentencePiece, target padding, one-epoch training, CLI inference, and safetensors save/load. This proves pipeline wiring, not translation quality. With only the light dependencies, backend tests are explicitly skipped. No real WMT fine-tuning, pretrained translation benchmark, BLEU, chrF or human evaluation was run.

## Docker

```sh
docker build --tag local-translation:ci .
docker run --rm local-translation:ci --help
docker run --rm -v "$PWD/examples/parallel.csv:/data.csv:ro" local-translation:ci check-data --data /data.csv
```

Multi-stage slim image, non-root runtime, no dev or ML dependencies. The container checks data, it does not translate or train. Hosted CI runs these build/run checks; see [verification](docs/verification.md) for the evidence boundary. No paid APIs, hosted training, self-hosted runners or deployment are configured. The workflow is restricted to public repositories and ordinary GitHub-hosted Linux runners.

## Layout and data flow

```text
CSV -> core.read_pairs -> source-disjoint split -> explicit CPU train
local safetensors + tokenizer -> model.encode / translate -> JSON
Typer CLI -> input validation -> core/model -> separate errors on stderr
```

`src/local_translation/core.py` owns CSV and split rules; `model.py` owns lazy ML loading, encoding, training and inference; `cli.py` is the interface. Tests build invented data and a random miniature model locally, with hub access disabled. CI uses pinned direct requirements via pip, while local reproduction uses `uv.lock`; pip is not claimed to enforce the full transitive uv lock.

## Historical notebook and limits

`Language Translation with .ipynb` is retained as a historical experiment with outputs cleared. Target tokenization, dynamic label padding and Transformers 4.49 Trainer names were corrected separately. It still contains explicit data/model download and training cells. **The notebook was not executed end to end.** Its online installation/download cells are not a free-compute service, and full training can be costly in time or on a billed host.

Next work: evaluate a licensed, appropriate pretrained local model on a genuinely untouched bilingual test set, inspect generated translations and failure modes, add length/domain slices, and measure BLEU/chrF with exact versions and signatures. No real-model quality, broad platform compatibility or production-readiness is claimed.

See [verification and phase notes](docs/verification.md), [changelog](CHANGELOG.md), and [copy-only GitHub presentation](docs/presentation.md). This review branch does not change the repository license, create a release/tag, merge main, or publish model/data artifacts.


## License scope

New project-owned package/engineering files use the owner's MIT default. See LICENSE and LICENSE-SCOPE.md. This is not permission to relicense historical notebooks, third-party code, datasets, models or weights. Their provenance and terms still need review. Earlier verification entries saying no license was added describe the initial pilot, not this follow-up.
