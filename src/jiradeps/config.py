# Copyright 2018,2022 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory
import configparser
import logging
from importlib import resources
from pathlib import Path
from typing import Optional


CONFIG_FILENAME = ".jiradepsrc"

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
        log.info(f'loaded config from  "{path}"')
    else:
        log.info(f'no config file "{path}" was found')
    return found_config


def create_default_config(path: Path):
    try:
        path.write_text(resources.read_text(__package__, "default.jiradepsrc"))
    except FileExistsError:
        log.error(f'config file "{path}" already exists')
    else:
        log.info(f'created config file "{path}"')
