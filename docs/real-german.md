# Real English-German CPU reproduction

The original generic translation direction now has an actual pinned pretrained German inference run and8train/4development CPU fine-tune. French remains a separate portable example in real-data.md. Actual German results are recorded in german-output.json. Low teacher-forced loss is not BLEU/chrF or unseen translation accuracy.

Model: https://huggingface.co/Helsinki-NLP/opus-mt-en-de , revision6183067f769a302e3861815543b9f312c71b0ca4. Model card CC BY4.0, separate from the French checkpoint's Apache2.0. Preserve credit to Helsinki-NLP and its model card. Official tensor state is checksum-verified before weights_only conversion; package inference accepts local safetensors only. No arbitrary pickle or remote model code.

Corpus: official Tatoeba detailed German/English exports and bilingual links,21November2026 snapshot. Source https://downloads.tatoeba.org/exports/per_language/deu/ and https://downloads.tatoeba.org/exports/per_language/eng/ . Terms https://tatoeba.org/en/terms_of_use are CC BY2.0 France with author attribution. Sentence IDs/authors are retained for every selected pair. The first12 linked unique IDs are a tiny development slice; no overlap guarantee with pretraining. No source text or weights committed. ManyThings German archive returned406 here, so this route uses original Tatoeba exports instead of an unverified mirror.

```sh
uv sync --locked --extra dev --extra ml
uv run --no-sync python scripts/fetch_german.py --output ./german-source
uv run --no-sync python scripts/prepare_german.py --data ./german-source --output ./german-pairs
uv run --no-sync python scripts/train_german.py --model ./german-source --data ./german-pairs/pairs.json --output ./german-model
```

Explicit downloads about300MB model plus57MB compressed text exports, excluding dependencies/checkpoints. Helpers pin every source hash and refuse existing output; an updated export fails the hash instead of silently replacing the snapshot. Pass --cached with those exact source files to avoid network. Training and inference use separate processes with batch1. No portable RAM minimum or guarantee for all laptops. The general package is locked/tested on Linux x86_64/Python3.11, not Windows/macOS certified. The final test, useful training schedule and generated-text benchmark remain work before any quality claim.
