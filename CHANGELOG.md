# Changelog

## [Unreleased]

### Fixed
- Notebook target tokenization, ignored-label dynamic padding and current Trainer API names.
- Removed an unrelated classification-accuracy loader and stale cell output.

### Added
- Typed local-only Marian CLI, strict parallel CSV validation and source-disjoint splits.
- Explicit CPU fine-tuning/inference, safetensors-only loading and finite-loss checks.
- Meaningful offline data/CLI/tiny Marian tests, uv lock, Ruff/mypy/hooks, CI and light Docker image.
- Exact limitations and review-only GitHub presentation notes.
