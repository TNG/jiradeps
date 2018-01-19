# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

import configparser
import logging
from typing import Optional


CONFIG_FILENAME = '.jiradepsrc'

DEFAULT_CONFIG = '''
[server]
url: https://example.local/jira
username: test

[jql]
# prefix used to identify issue keys
keyprefix: ABC

# optional query to load epics if the key prefix doesn't match
# (query is run for each specified epic identifier)
query: (customID ~ {0} OR labels in ({0})) AND issuetype = Epic 

# optional predicate for loading the stories in epics 
predicate: labels NOT IN ("NoDev") OR labels is EMPTY

[customfields]
## optionally specify the following custom fields for your JIRA instance
## (the id values for your JIRA instance can for example be seen in the
## issue query autocomplete, or ask your friendly JIRA admin)
# sprint: customfield_10123
# team: customfield_12111
# storypoints: customfield_12345
'''.strip()

_config_inst: Optional[configparser.ConfigParser] = None

log = logging.getLogger(__name__)


def get_config() -> configparser.ConfigParser:
    """Returns an empty config or the one last loaded with `load_config`.

    The empty config is especially useful for testing.
    """
    global _config_inst
    if not _config_inst:
        _config_inst = configparser.ConfigParser()
    return _config_inst


def load_config(path) -> bool:
    global _config_inst
    _config_inst = configparser.ConfigParser()
    found_config = bool(_config_inst.read(path))
    if found_config:
        log.info('loaded config from  "{}"'.format(path))
    else:
        log.info('no config file "{}" was found'.format(path))
    return found_config


def create_default_config(path):
    try:
        with open(path, 'x', encoding='UTF-8') as config_file:
            config_file.write(DEFAULT_CONFIG)
    except FileExistsError:
        log.error('config file "{}" already exists'.format(path))
    else:
        log.info('created config file "{}"'.format(path))
