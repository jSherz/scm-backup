#!/usr/bin/env python

from logging import getLogger
from github import Github
from os import environ
from os.path import join, exists
from subprocess import call
from logging.config import fileConfig

BACKUP_PATH = 'github'

fileConfig('logging.ini')
log = getLogger()

log.info('[GitHub backup]')

g = Github(environ['GITHUB_ACCESS_TOKEN'])

user = g.get_user()
username = user.login
log.debug('Backing up for %s' % username)

for repo in user.get_repos():
    repo_name = repo.name
    log.info('Backing up %s' % repo_name)

    repo_backup_path = join(BACKUP_PATH, repo_name + '.git')
    log.debug('Backing up to %s' % repo_backup_path)

    repo_url = repo.git_url
    log.debug('Backing up from %s' % repo_url)

    if exists(repo_backup_path):
        log.debug('Backed up in the past, updating mirror')

        result = call(['git', 'remote', 'update'])

        if result == 0:
            log.info('Updated %s' % repo_name)
        else:
            log.error('Failed to update %s' % repo_name)
    else:
        log.debug('Not backed up repo before, cloning')

        repo_url = 'git@github.com:%s/%s.git' % (username, repo_name)
        log.debug('Repo URL is %s' % repo_url)

        result = call(['git', 'clone', '--mirror', repo_url, repo_backup_path], env=environ)

        if result == 0:
            log.info('Cloned %s' % repo_name)
        else:
            log.error('Failed to clone %s' % repo_name)
