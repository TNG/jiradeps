# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory
import configparser
import os
from unittest.mock import MagicMock

import pytest
from click.testing import CliRunner

import jiradeps.main as main


@pytest.fixture()
def config(mocker):
    test_config = configparser.ConfigParser()
    test_config.read_dict(
        {
            "server": {"url": "test.com", "username": "testuser"},
            "jql": {"epicprefix": "ABC", "query": ""},
            "customfields": {},
        }
    )
    mocker.patch("jiradeps.main._load_or_create_config", return_value=True)
    mocker.patch("jiradeps.jirawrapper.get_config", return_value=test_config)
    mocker.patch("jiradeps.main.get_config", return_value=test_config)
    return test_config


@pytest.fixture
def click_runner():
    runner = CliRunner()
    with runner.isolated_filesystem():
        yield runner


@pytest.mark.usefixtures("config")
def test_cli(click_runner, mocker, epics, stories):
    mocker.patch(
        "jiradeps.main.get_jira_session", return_value=MagicMock(search_issues=MagicMock(side_effect=[epics, stories]))
    )

    result = click_runner.invoke(main.cli, ["-f", "test", "-p", "test", "-g", "ABC-123"], catch_exceptions=False)
    assert result.exit_code == 0
    assert "loaded 1 epics" in result.output
    assert "loaded 2 stories" in result.output

    assert os.path.isfile("test.gv.svg")
    with open("test.gv.svg") as output_file:
        file_content = output_file.read()
    assert "ABC&#45;10" in file_content
    assert "ABC&#45;11" in file_content
    assert "ABC&#45;12" in file_content
