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


### Engineering follow-up
- Use the committed uv lock in CI and key dependency-installer caching by that lock.
- Complete copy-only profile README drafts and clarify historical versus current verification.

### Synthetic demonstration follow-up

Added standalone invented-input backend demo, checked JSON output and documented limits. Opt-in ML container added where a model backend exists; default lightweight image unchanged. Hosted container verification is required separately.

## Portable notebook follow-up

Replace platform-specific notebook execution with safe-default local package entry points, explicit local input checks and opt-in training. Add notebook execution/argv/failure regressions. Historical model scores and full-scale data training are not claimed reproduced.
