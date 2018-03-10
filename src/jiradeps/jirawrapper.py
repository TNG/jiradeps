# Copyright 2018 TNG Technology Consulting GmbH, Unterföhring, Germany
# Licensed under the Apache License, Version 2.0 - see LICENSE.md in project root directory

import logging
import re
import configparser
from typing import List, Set, Optional

from jira import JIRA, Issue

from .config import get_config

log = logging.getLogger(__name__)

SPRINT_ID_REGEX = re.compile(r'name=Sprint (\w+),')


def _get_customfields() -> configparser.SectionProxy:
    config = get_config()
    return config['customfields']


def _fields_to_load() -> List[str]:
    fields = ['key', 'summary', 'issuelinks', 'status', 'labels']
    customfields = _get_customfields()
    if 'sprint' in customfields:
        fields.append(customfields['sprint'])
    if 'team' in customfields:
        fields.append(customfields['team'])
    if 'storypoints' in customfields:
        fields.append(customfields['storypoints'])
    return fields


def get_jira_session(user, password, server) -> JIRA:
    log.info('initializing JIRA connection...')
    jira = JIRA(options={'server': server},
                basic_auth=(user, password),
                validate=True)
    log.info('initialized JIRA')
    return jira


def load_epics(epic_params: List[str], session: JIRA) -> List[Issue]:
    epics = []
    key_prefix = get_config()['jql']['epicprefix']
    for epic_param in epic_params:
        if epic_param.startswith(key_prefix):
            epics.append(_load_epic_by_key(epic_param, session))
        else:
            epics += _load_epics_by_config_query(epic_param, session)
    return epics


def _load_epics_by_config_query(epic_param: str, session: JIRA)-> List[Issue]:
    query = get_config()['jql'].get('query')
    if not query:
        log.warning('no custom epic query is configured, '
                    f'cannot search for epic parameter {epic_param}')
        return []
    epics = session.search_issues(query.format(epic_param),
                                  fields=','.join(_fields_to_load()),
                                  maxResults=1000)
    log.info(f'found {len(epics)} epics for query parameter {epic_param}')
    return epics


def _load_epic_by_key(epic_key: str, session: JIRA) -> List[Issue]:
    query = f'key in ({epic_key}) AND issuetype = Epic'
    epics = session.search_issues(query,
                                  fields=','.join(_fields_to_load()),
                                  maxResults=1000)
    if len(epics) != 1:
        log.warning(f'found {len(epics)} epics for key {epic_key}')
    else:
        log.info(f'found 1 epic for key {epic_key}')
    return epics[0]


def load_epic_stories(epic: Issue, session: JIRA) -> List[Issue]:
    query = 'type = Story AND "Epic Link" = {}'.format(epic.key)
    predicate = get_config()['jql'].get('predicate')
    if predicate:
        query = f'{query} AND ({predicate})'
        log.debug(f'using story query with custom predicate: {query}')
    stories = session.search_issues(query,
                                    fields=','.join(_fields_to_load()),
                                    maxResults=1000)
    return stories


def get_sprints(issue: Issue) -> Optional[Set[str]]:
    sprint_field = _get_customfields().get('sprint')
    if not sprint_field:
        return None
    return {SPRINT_ID_REGEX.search(sprint_raw).group(1)
            for sprint_raw in getattr(issue.fields, sprint_field) or []}


def get_story_points(issue: Issue) -> Optional[float]:
    story_points_field = _get_customfields().get('storypoints')
    if not story_points_field:
        return None
    return getattr(issue.fields, story_points_field) or 0.0


def get_team(issue: Issue) -> Optional[str]:
    team_field = _get_customfields().get('team')
    if not team_field:
        return None
    team = getattr(issue.fields, team_field)
    if team:
        return team.value
    else:
        return None


def get_blocked_keys(issue: Issue) -> List[str]:
    links = issue.fields.issuelinks
    return [link.outwardIssue.id for link in links
            if str(link.type) == 'Blocks' and hasattr(link, 'outwardIssue')]


def get_related_keys(issue: Issue) -> List[str]:
    links = issue.fields.issuelinks
    outward_keys = [link.outwardIssue.key for link in links
                    if str(link.type) == 'Relates'
                    and hasattr(link, 'outwardIssue')]
    inward_keys = [link.inwardIssue.key for link in links
                   if str(link.type) == 'Relates'
                   and hasattr(link, 'inwardIssue')]
    return outward_keys + inward_keys
