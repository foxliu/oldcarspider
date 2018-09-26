#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def create_repo():
    repo_file = '/etc/yum.repos.d/salt.repo'
    content = """
[saltstack for rhel6]
name=saltstack packages
baseurl=http://172.29.25.37/saltstack/rhel6/x86_64/latest
        http://172.29.25.38/saltstack/rhel6/x86_64/latest
enabled=1
gpgcheck=1
gpgkey=http://172.29.25.37/saltstack/rhel6/x86_64/latest/SALTSTACK-GPG-KEY.pub
       http://172.29.25.38/saltstack/rhel6/x86_64/latest/SALTSTACK-GPG-KEY.pub

"""
    with open(repo_file, 'a+') as f:
        f.write(content)
