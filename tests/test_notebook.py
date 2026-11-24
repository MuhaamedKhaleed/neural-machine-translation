"""Portable notebook safe-default and explicit input-check regression."""

import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest


def cells():
    notebook = json.loads(Path("Language Translation with .ipynb").read_text())
    return ["".join(c["source"]) for c in notebook["cells"] if c["cell_type"] == "code"]


def test_notebook_safe_default(monkeypatch):
    for key in ("NOTEBOOK_CHECK_DATA", "NOTEBOOK_RUN_TRAINING"):
        monkeypatch.delenv(key, raising=False)
    runner = Mock(side_effect=AssertionError("Default must not start subprocesses"))
    monkeypatch.setattr("subprocess.run", runner)
    namespace = {"__name__": "__main__"}
    for source in cells():
        exec(compile(source, "notebook", "exec"), namespace)
    runner.assert_not_called()


def test_notebook_explicit_check(monkeypatch, tmp_path):
    monkeypatch.setenv("NOTEBOOK_CHECK_DATA", "1")
    monkeypatch.delenv("NOTEBOOK_RUN_TRAINING", raising=False)
    path = tmp_path / "local-input"
    path.touch()
    monkeypatch.setenv("PARALLEL_CSV", str(path))
    runner = Mock(return_value=SimpleNamespace(stdout="{}"))
    monkeypatch.setattr("subprocess.run", runner)
    namespace = {"__name__": "__main__"}
    for source in cells():
        exec(compile(source, "notebook", "exec"), namespace)
    argv = runner.call_args.args[0]
    assert argv[1:4] == ["-m", "local_translation", "check-data"]
    assert runner.call_args.kwargs["check"] is True


def test_notebook_missing_check_path(monkeypatch):
    monkeypatch.setenv("NOTEBOOK_CHECK_DATA", "1")
    monkeypatch.delenv("PARALLEL_CSV", raising=False)
    namespace = {"__name__": "__main__"}
    with pytest.raises(ValueError):
        for source in cells():
            exec(compile(source, "notebook", "exec"), namespace)


def test_notebook_explicit_training(monkeypatch, tmp_path):
    monkeypatch.delenv("NOTEBOOK_CHECK_DATA", raising=False)
    monkeypatch.setenv("NOTEBOOK_RUN_TRAINING", "1")
    input_path = tmp_path / "local-input"
    input_path.mkdir()
    output = tmp_path / "new-output"
    monkeypatch.setenv("PARALLEL_CSV", str(input_path))
    monkeypatch.setenv("TRANSLATION_OUTPUT", str(output))
    monkeypatch.setenv("TRANSLATION_BASE_MODEL", str(input_path))
    runner = Mock(return_value=SimpleNamespace(stdout="{}"))
    monkeypatch.setattr("subprocess.run", runner)
    namespace = {"__name__": "__main__"}
    for source in cells():
        exec(compile(source, "notebook", "exec"), namespace)
    argv = runner.call_args.args[0]
    assert "train" in argv and "--epochs" in argv
    assert runner.call_args.kwargs["check"] is True
    output.mkdir()
    runner.reset_mock()
    with pytest.raises(ValueError):
        for source in cells():
            exec(compile(source, "notebook", "exec"), namespace)
    runner.assert_not_called()
