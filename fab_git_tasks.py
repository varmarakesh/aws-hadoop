from fabric_helper import *

git_email = 'varma.rakesh@gmail.com'
git_usr = 'varma.rakesh'
git_repo_url ='git@github.com:varmarakesh/aws-hadoop.git'


@task
def git_commit(msg):
    """
    fab git_initialize:msg='your commit message'
    run fab git_commit for commit to your local repo. it is a good practice to commit regularly.
    """
    local('git config --global user.email "{0}"'.format(git_email))
    local('git config --global user.name "{0}"'.format(git_usr))
    local('git add .')
    local('git commit -m "{0}"'.format(msg))

@task
def git_commit_push(msg):
    """
    fab git_commit_push
    This commits as well as pushes to the remote repo. To not prompt for the password add your machine ssh-key to the github settings.
    """
    git_commit(msg)
    local('git remote set-url origin {0}'.format(git_repo_url))
    local('git push origin master')
    local('git status')
    local('git log --oneline')