import sys
import pytest
from typing import List
from unittest import mock

from things3cli import main


def run_cli(thigs3cli_args: List[str]):
    with mock.patch.object(sys, "argv", ["things3cli"] + thigs3cli_args):
        return main.cli()


def test_version(capsys):
    mock_exit = mock.Mock(side_effect=ValueError("raised in test to exit early"))
    with mock.patch.object(sys, "exit", mock_exit), pytest.raises(
        ValueError, match="raised in test to exit early"
    ):
        assert not run_cli(["--version"])
    captured = capsys.readouterr()
    mock_exit.assert_called_with(0)
    assert main.__version__ in captured.out.strip()


def test_help_text(capsys):
    mock_exit = mock.Mock(side_effect=ValueError("raised in test to exit early"))
    with mock.patch.object(sys, "exit", mock_exit), pytest.raises(
        ValueError, match="raised in test to exit early"
    ):
        assert not run_cli(["--help"])
    captured = capsys.readouterr()
    print(captured)
    assert "usage: things3cli" in captured.out
