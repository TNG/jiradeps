# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

from unittest.mock import MagicMock

from pytest import fixture


@fixture
def epics():
    return [
        MagicMock(id='1', key='ABC-10',
                  fields=MagicMock(summary='Epic'))
    ]


@fixture
def stories():
    link = MagicMock(type='Blocks', outwardIssue=MagicMock(id='3'))
    return [
        MagicMock(id='2', key='ABC-11',
                  fields=MagicMock(
                      summary='Story 1',
                      issuelinks=[link]
                  )),
        MagicMock(id='3', key='ABC-12',
                  fields=MagicMock(summary='Story 2'))
    ]