#!/usr/bin/env python

from logging import getLogger
from github import Github
from os.path import join, exists
from subprocess import call

BACKUP_PATH = 'github'

log = getLogger('backup.github')

log.info('[GitHub backup]')

g = Github("", "")

for repo in g.get_user().get_repos():
    repo_name = repo.get_name()
    log.info('Backing up %s' % repo_name)

    repo_backup_path = join(BACKUP_PATH, repo_name + '.git')
    log.debug('Backing up to %s' % repo_backup_path)

    repo_url = repo.git_url()
    log.debug('Backing up from %s' % repo_url)

    if exists(repo_backup_path):
        log.debug('Backed up in the past, updating mirror')

        result = call(['git', 'remote', 'update'])

        if result == 0:
            log.info('Updated %s' % repoo_name)
        else:
            log.error('Failed to update %s' % repo_name)
    else:
        log.debug('Not backed up repo before, cloning')

        result = call(['git', 'clone', '--mirror', repo_name, repo_backup_path])

        if result == 0:
            log.info('Cloned %s' % repo_name)
        else:
            log.error('Failed to clone %s' % repo_name)
