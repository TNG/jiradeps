# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

from unittest.mock import MagicMock
import configparser

from pytest import fixture
from click.testing import CliRunner

import jiradeps.main as main


@fixture
def config():
    test_config = configparser.ConfigParser()
    test_config.read_dict({
        'server': {
            'url': 'test.com',
            'username': 'testuser'
        },
        'jql': {
            'keyprefix': 'ABC',
            'query': ''
        },
        'customfields': {
        }
    })
    return test_config


def test_cli(mocker, config, epics, stories):
    mocker.patch('jiradeps.main._load_or_create_config', return_value=True)
    mocker.patch('jiradeps.jirawrapper.get_config',
                 return_value=config)
    mocker.patch('jiradeps.main.get_config',
                 return_value=config)

    mocker.patch('jiradeps.main.get_jira_session', return_value=MagicMock(
        search_issues=MagicMock(side_effect=[epics, stories])))

    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(main.cli,
                               ['--password', 'test', '-g', 'ABC-123'],
                               catch_exceptions=False)
        # the output file can be gathered from the log if needed:
        # print('\n' + result.output.split()[-1])
    assert result.exit_code == 0
    assert 'loaded 1 epics' in result.output
    assert 'loaded 2 stories' in result.output
    assert 'rendered graph as' in result.output
