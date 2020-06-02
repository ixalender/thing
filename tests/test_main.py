import sys
import pytest
from typing import List
from unittest import mock

from thing import main
from thing.commands.list import ListSubCommand


def run_cli(thing_args: List[str]):
    with mock.patch.object(sys, "argv", ["thing"] + thing_args):
        return main.cli()


def test_version(capsys):
    mock_exit = mock.Mock(
        side_effect=ValueError("raised in test to exit early"))
    with mock.patch.object(sys, "exit", mock_exit), pytest.raises(
        ValueError, match="raised in test to exit early"
    ):
        assert not run_cli(["--version"])
    captured = capsys.readouterr()
    mock_exit.assert_called_with(0)
    assert main.__version__ in captured.out.strip()


def test_help_text(capsys):
    mock_exit = mock.Mock(
        side_effect=ValueError("raised in test to exit early"))
    with mock.patch.object(sys, "exit", mock_exit), pytest.raises(
        ValueError, match="raised in test to exit early"
    ):
        assert not run_cli(["--help"])
    captured = capsys.readouterr()
    assert "usage: thing" in captured.out


def test_list_text(capsys):
    run_cli(["list"])
    captured = capsys.readouterr()
    types = ', '.join(list(map(lambda i: i.value, iter(ListSubCommand))))
    assert f"You should add the type of task you want to list, like: {types}" in captured.out
