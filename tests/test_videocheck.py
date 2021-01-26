#!/usr/bin/env python

"""Tests for `videocheck` package."""

import pytest

from click.testing import CliRunner

from videocheck import cli
import pandas as pd
from pathlib import Path


def test_cli():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)

    assert "1/2 faulty videos detected 🚨" in result.output
    assert "OVER ✅" in str(result.output)
    assert result.exit_code == 0

    Path("videochecked.csv").unlink()


def test_cli_args():
    """Test the CLI arguments."""
    runner = CliRunner()
    result = runner.invoke(
        cli.main,
        "-o tests/out.csv -t 2 -e mp4,avi".split(" ")
    )

    print(result.output)
    assert "1/2 faulty videos detected 🚨" in result.output
    assert "OVER ✅" in str(result.output)
    assert result.exit_code == 0

    csv = pd.read_csv("tests/out.csv", index_col=0)
    assert csv.shape == (2, 2)
    assert csv.errors.dropna().shape[0] == 1

    Path("tests/out.csv").unlink()
