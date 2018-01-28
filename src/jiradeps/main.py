# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

"""
Visualize the dependencies in one or more epics.
"""

import getpass
import sys
import os
import logging
import tempfile

import keyring
import click
import click_log

from jiradeps import (get_jira_session, load_epic_stories,
                      load_epics, create_issue_digraph,
                      add_longest_ancestor_distance, remove_unconnected_nodes,
                      visualize_with_graphviz,
                      CONFIG_FILENAME, load_config, get_config,
                      create_default_config)

log = logging.getLogger(__name__)
click_log.basic_config()


@click.command()
@click.argument('EPIC_PARAMS', nargs=-1, required=True)
@click.option('--configfile', '-c',
              default=os.path.join(os.getcwd(), CONFIG_FILENAME),
              help='Config file to be used '
                   f'(defaults to CWD/{CONFIG_FILENAME})')
@click.option('--password', '-p', help='Jira password')
# output
@click.option('--file-name', '-f',
              help='Name for output file (without file extension).')
@click.option('--file-type', '-t', default='svg',
              help='Type of output file (e.g., svg or png).')
@click.option('--open-file', '-o', is_flag=True,
              help='Automatically open the output file with '
                   'default application.')
# graph options
@click.option('--hide-unconnected', '-u', is_flag=True,
              help='Hide stories that have no blocking dependencies.')
@click.option('--align-sprints', '-a', is_flag=True,
              help='Enforce that stories from same sprint '
                   'are at the same height.')
@click.option('--group-epics', '-g', is_flag=True,
              help='Create a subgraph for each epic.')
@click.option('--show-status', '-s', is_flag=True,
              help='Show the issue status and team assignment.')
@click_log.simple_verbosity_option(default='INFO')
def cli(epic_params, configfile, password,
        file_name, file_type, open_file,
        hide_unconnected, align_sprints, group_epics, show_status):
    """
    EPIC_PARAMS can be JIRA issue keys (matching the prefix specified in the
    config file), or will otherwise be loaded using the query from the
    config file.
    """
    _load_or_create_config(configfile)
    config = get_config()
    server_config = config['server']
    user = server_config['username']
    if not password:
        password = _get_password(user, 'jiradeps')
    session = get_jira_session(user, password, server_config['url'])

    epics = load_epics(epic_params, session)
    log.info(f'loaded {len(epics)} epics')
    epic_stories = {}
    n_stories = 0
    for epic in epics:
        if epic.key in epic_stories:
            log.warning(f'epic {epic.key} was loaded multiple times')
            continue
        stories = load_epic_stories(epic, session)
        epic_stories[epic.key] = stories
        n_stories += len(stories)
        log.info(f'loaded {len(stories)} stories for epic {epic.key}')
    if n_stories == 0:
        log.error('found no stories, creating no graph')
        sys.exit(1)

    nx_graph = create_issue_digraph(epic_stories)
    if hide_unconnected:
        removed_issues = remove_unconnected_nodes(nx_graph)
        log_issues(
            'removed {} unconnected issues:'.format(len(removed_issues)),
            removed_issues)
    add_longest_ancestor_distance(nx_graph)

    if not file_name:
        file_name = os.path.join(tempfile.mkdtemp(prefix='jiradeps_'),
                                 'jiradeps')
    if align_sprints and not config['customfields'].get('sprint'):
        log.error('Sprint alignment option requires that the customfield '
                  'is configured.')
    output_path = visualize_with_graphviz(nx_graph, epics,
                                          file_type=file_type,
                                          file_name=file_name,
                                          group_epics=group_epics,
                                          align_sprints=align_sprints,
                                          show_status=show_status)
    log.info('rendered graph as {}'.format(os.path.abspath(output_path)))
    if open_file:
        click.launch(output_path)


def _load_or_create_config(config_path):
    found_config = load_config(config_path)
    if not found_config:
        create_config = click.confirm(
            f'Do you want to create a new config file at {config_path} '
            '(a config file is mandatory)?')
        if create_config:
            create_default_config(config_path)
            click.echo(click.style(
                f'Please adapt the config file {config_path} and start again.',
                bold=True))
        else:
            click.echo(click.style(
                f'Please create a config file and start again.',
                bold=True))
        sys.exit(1)


def _get_password(user, service_name):
    password = keyring.get_password(service_name, user)
    if password is None:
        password = getpass.getpass(
            'Password for {} (will be stored in keyring): '.format(user))
        keyring.set_password(service_name, user, password)
    return password


def log_issues(headline, issues):
    log.info('\n'.join([headline]
                       + ['    {} - {}'.format(issue.key, issue.fields.summary)
                          for issue in issues]))
