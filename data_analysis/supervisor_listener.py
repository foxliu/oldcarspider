#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import subprocess


def write_stdout(s):
    # only eventlistener protocol messages may be sent to stdout
    sys.stdout.write(s)
    sys.stdout.flush()


def write_stderr(s):
    sys.stderr.write(s)
    sys.stderr.flush()


def main():
    script_path = '/etc/supervisor.sequence.d/'
    log_file = '/var/log/supervisor.listener.log'
    while 1:
        # transition from ACKNOWLEDGED to READY
        write_stdout('READY\n')

        # read header line and print it to stderr
        line = sys.stdin.readline()

        # read event payload and print it to stderr
        headers = dict([x.split(':') for x in line.split()])
        # get server:supervisor  and eventname: PROCESS_STATE_STARTING
        if headers['server'] == 'supervisor' and headers['eventname'] == 'SUPERVISOR_STATE_CHANGE_RUNNING':
            files = os.listdir(script_path)
            files.sort()
            for f in files:
                script_path = os.path.join(script_path, f)
                os.chmod(script_path, 0755)
                p = subprocess.Popen(script_path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                out_put = p.communicate()
                with open(log_file, 'a+') as f:
                    f.write(out_put[0])

        # transition from READY to ACKNOWLEDGED
        write_stdout('RESULT 2\nOK')


if __name__ == '__main__':
    main()
