#!/usr/bin/env python

from logging import getLogger
from pybitbucket.auth import BasicAuthenticator
from pybitbucket.bitbucket import Client
from pybitbucket.repository import Repository
from os import environ
from os.path import join, exists
from subprocess import call
from logging.config import fileConfig

BACKUP_PATH = 'bitbucket'

fileConfig('logging.ini')
log = getLogger()

log.info('[BitBucket backup]')

b = Client(BasicAuthenticator(
    environ['BITBUCKET_USERNAME'], environ['BITBUCKET_PASSWORD'], 'pybitbucket@mailinator.com'
))

user = b.get_username()
log.debug('Backing up for %s' % user)

for repo in Repository.find_repositories_by_owner_and_role(owner=user, client=b):
    repo_name = repo.name
    log.info('Backing up %s' % repo_name)

    repo_backup_path = join(BACKUP_PATH, repo_name + '.git')
    log.debug('Backing up to %s' % repo_backup_path)

    if exists(repo_backup_path):
        log.debug('Backed up in the past, updating mirror')

        result = call(['git', 'remote', 'update'])

        if result == 0:
            log.info('Updated %s' % repo_name)
        else:
            log.error('Failed to update %s' % repo_name)
    else:
        log.debug('Not backed up repo before, cloning')

        repo_url = 'git@bitbucket.org:%s/%s' % (user, repo_name)
        log.debug('Repo URL is %s' % repo_url)

        result = call(['git', 'clone', '--mirror', repo_url, repo_backup_path], env=environ)

        if result == 0:
            log.info('Cloned %s' % repo_name)
        else:
            log.error('Failed to clone %s' % repo_name)
