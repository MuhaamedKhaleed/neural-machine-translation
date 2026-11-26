# Local Marian Translation (English/German)

A local CLI for validating parallel CSV data, translating with a local Marian model, and running explicit CPU fine-tuning. Extracted from an experimental English/German notebook, fixing target-tokenization and padding bugs along the way.

## Results (honest)

- Fresh clone translates real sentences with a pinned public model (Helsinki-NLP `opus-mt-en-de`, ~300 MB). Recorded 25 Nov 2026: "The weather is nice today." -> "Das Wetter ist heute schön.".
- The bundled fine-tune runs on 12 sentence pairs. It proves the train/save/reload wiring; it is not a quality improvement.
- Validation metric is token-weighted teacher-forced loss. No BLEU, chrF, WMT benchmark or human evaluation has been run.
- 24 tests, 96% statement coverage (tiny random Marian forward/backward, synthetic SentencePiece, safetensors save/load). Coverage proves wiring, not translation quality.

## Quickstart (fresh clone, about 3 minutes)

Needs Python 3.11 or 3.12 (locked wheels have no 3.13+ build), Linux x86_64, internet for the first install/downloads, ~2 GB free RAM.

```sh
uv sync --python 3.11 --locked --extra dev --extra ml
uv run --no-sync python scripts/fetch_german.py --output ./german-source       # pinned opus-mt-en-de + Tatoeba exports
uv run --no-sync local-translation translate ./german-source "The weather is nice today."
uv run --no-sync python scripts/prepare_german.py --data ./german-source --output ./german-pairs
uv run --no-sync python scripts/train_german.py --model ./german-source --data ./german-pairs/pairs.json --output ./german-model
```

To fine-tune on your own data, build a `source,target` CSV and run `local-translation train ./german-source YOUR.csv ./my-model --epochs N`.

Data checks run without the ML stack: `uv sync --locked --extra dev` then `local-translation check-data --data examples/parallel.csv` returns `{"pairs": 3, "train_pairs": 2, "validation_pairs": 1}`.

## Limits

- You must supply a trusted local Marian model (loaded with `local_files_only=True`); no model is bundled or auto-downloaded, and its language direction and license are your responsibility.
- Source-disjoint splitting is not document/domain independence and not an untouched test set.
- CPU-only, deterministic beam search, bounded input lengths; truncation can drop long-text information.
- The historical notebook is kept with outputs cleared but was not executed end to end; its download/training cells can be costly.
- Verified on Linux x86_64 only; the container runs data checks, not translation. Hosted CI (free public-repo runners) checks tests, lint, CLI and the Docker build.

## License

MIT for the new project-owned code (see `LICENSE` and `LICENSE-SCOPE.md`). Historical notebooks, third-party models, datasets and corpora keep their own terms; no rights clearance is claimed for them. Details and evidence: `docs/verification.md`, `docs/real-data.md`, `docs/real-german.md`, `CHANGELOG.md`.
