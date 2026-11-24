# Portable notebook migration, 24 November 2026

The root notebook is now a safe-default local entry point into the supported package. It no longer executes the inherited platform-specific experiment. This is a workflow replacement, not historical-score reproduction or preservation of all old APIs/plots/widgets. Git history/main are unchanged. The package CLI remains the documented supported interface.

Default notebook execution performs no install, download, credentials, model load, training or subprocess. Explicit input checking uses existing local settings. Training, where implemented, is separately opt-in, CPU, one epoch by default, and refuses an existing output. Data/model rights, representative evaluation and private material publication remain separate. No fresh model/data artifacts are committed.

Regression tests execute all default code cells in order and check the explicit input-check argv/error path. The package's existing real-backend tests and synthetic demo separately test underlying training. No full-scale real-data training or legacy notebook metric reproduction is implied.
