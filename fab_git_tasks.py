from fabric_helper import *

@task
def git_commit(msg):
    local('git config --global user.email "{0}"'.format('varma.rakesh@gmail.com'))
    local('git config --global user.name "{0}"'.format('varma.rakesh'))
    local('git add .')
    local('git commit -m {0}'.format(msg))

@task
def git_commit_push(msg):
    local('git config --global user.email "{0}"'.format('varma.rakesh@gmail.com'))
    local('git config --global user.name "{0}"'.format('varma.rakesh'))
    local('git add .')
    local('git add config.ini')
    #local('git rm --cached config.ini')
    local('git commit -m "{0}"'.format(msg))
    local('git remote set-url origin git@github.com:varmarakesh/aws-hadoop.git')
    local('git push origin master')
    local('git status')
    local('git log --oneline')
