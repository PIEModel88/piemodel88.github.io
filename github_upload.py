#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 15 00:33:43 2021

@author: ivamn
"""
#pip install PyGithub
from github import Github
#from github import InputGitTreeElement
import base64
import os, sys
# g = Github("tokenH")
# repo = g.get_user().get_repo("piemodel88.github.io")
# all_files = []
# contents = repo.get_contents("")
# while contents:
#     file_content = contents.pop(0)
#     if file_content.type == "dir":
#         contents.extend(repo.get_contents(file_content.path))
#     else:
#         file = file_content
#         all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))

# with open(str(sys.argv[1]+sys.argv[2]), 'r') as file:
#     content = file.read()

    
# # Upload to github
# git_prefix = 'page/'
# git_file = git_prefix + str(sys.argv[2])
# if git_file in all_files:
#     contents = repo.get_contents(git_file)
#     repo.update_file(contents.path, "committing files", content, contents.sha, branch="main")
#     print(git_file + ' UPDATED')
# else:
#     repo.create_file(git_file, "committing files", content, branch="main")
#     print(git_file + ' CREATED')
    
    
    
from github_contents import GithubContents

# For repo simonw/disaster-data:
github = GithubContents(
    "Piemodel88",
    "piemodel88.github.io",
    token='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',
    branch="main"
)



with open(str(sys.argv[1]+sys.argv[2]), 'rb') as file:
    content = file.read()


content_sha, commit_sha = github.write(
    'page/' + sys.argv[2],
    content,
    commit_message='written by test',
    committer={"name": "Test", "email": "test"},
 )
