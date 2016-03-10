import os
import sys
import subprocess

from cloudify import ctx

PORT = 80


def run_server():
    webserver_cmd = [sys.executable, '-m', 'SimpleHTTPServer', str(PORT)]
    if not IS_WIN:
        webserver_cmd.insert(0, 'nohup')

    ctx.logger.info('Running WebServer locally on port: {0}'.format(PORT))
    # emulating /dev/null
    with open(os.devnull, 'wb') as dn:
        process = subprocess.Popen(webserver_cmd, stdout=dn, stderr=dn)
    return process.pid


def set_pid(pid):
    ctx.logger.info('Setting `pid` runtime property: {0}'.format(pid))
    # We can set runtime information in our context object which
    # can later be read somewhere in the context of the instance.
    # For instance, we want to save the `pid` here so that when we
    # run `uninstall.py`, we can destroy the process.
    ctx.instance.runtime_properties['pid'] = pid


pid = run_server()
#set_pid(pid)
#Status