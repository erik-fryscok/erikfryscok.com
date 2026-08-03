"""Tests for CLI commands."""

from pathlib import Path

from click.testing import CliRunner

from agent_eval.cli import main


def test_validate_fails_when_jobs_dir_missing_env():
    runner = CliRunner()
    result = runner.invoke(main, ["validate"])
    assert result.exit_code == 1
    assert "ERIKFRYSCOK_HARBOR_JOBS_DIR not set" in result.output


def test_validate_fails_when_jobs_dir_missing(tmp_path, monkeypatch):
    monkeypatch.setenv("ERIKFRYSCOK_HARBOR_JOBS_DIR", str(tmp_path / "does-not-exist"))
    runner = CliRunner()
    result = runner.invoke(main, ["validate"])
    assert result.exit_code == 1
    assert "does not exist" in result.output


def test_validate_rejects_in_repo_path(tmp_path, monkeypatch):
    repo_local = Path.cwd() / "local-jobs"
    repo_local.mkdir(exist_ok=True)
    monkeypatch.setenv("ERIKFRYSCOK_HARBOR_JOBS_DIR", str(repo_local))
    runner = CliRunner()
    result = runner.invoke(main, ["validate"])
    assert result.exit_code == 1
    assert "must be outside repository" in result.output


def test_validate_succeeds_for_external_path(tmp_path, monkeypatch):
    monkeypatch.setenv("ERIKFRYSCOK_HARBOR_JOBS_DIR", str(tmp_path))
    runner = CliRunner()
    result = runner.invoke(main, ["validate"])
    assert result.exit_code == 0
    assert "Configuration valid" in result.output


def test_preflight_fails_when_docker_unavailable(monkeypatch):
    def raise_file_not_found(*_args, **_kwargs):
        raise FileNotFoundError

    import subprocess

    monkeypatch.setattr(subprocess, "run", raise_file_not_found)
    runner = CliRunner()
    result = runner.invoke(main, ["preflight"])
    assert result.exit_code == 1
    assert "Docker not available" in result.output


def test_preflight_succeeds_with_lm_studio(monkeypatch):
    class DummyResponse:
        status_code = 200

    class DummyRequests:
        @staticmethod
        def get(_url, timeout):
            assert timeout == 5
            return DummyResponse()

    import subprocess
    import sys

    monkeypatch.setattr(subprocess, "run", lambda *_args, **_kwargs: None)
    monkeypatch.setenv("LM_STUDIO_ENDPOINT", "http://localhost:1234/v1")
    monkeypatch.setitem(sys.modules, "requests", DummyRequests)

    runner = CliRunner()
    result = runner.invoke(main, ["preflight"])
    assert result.exit_code == 0
    assert "Docker available" in result.output
    assert "LM Studio available" in result.output


def test_stub_commands_render_expected_output(tmp_path):
    runner = CliRunner()

    assert runner.invoke(main, ["oracle", "--suite", "smoke"]).exit_code == 0
    assert runner.invoke(main, ["run", "--suite", "smoke", "--profile", "baseline"]).exit_code == 0

    exp_file = tmp_path / "exp.yaml"
    exp_file.write_text("name: test\n")
    assert runner.invoke(main, ["matrix", "--experiment", str(exp_file)]).exit_code == 0

    assert runner.invoke(main, ["compare", "--baseline", "b1", "--candidate", "c1"]).exit_code == 0
    assert runner.invoke(main, ["sanitize-report", "--experiment", "exp-1"]).exit_code == 0
