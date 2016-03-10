import os
import sys
import subprocess
from cloudify import ctx
from fabric.api import run, env

CONFIG_FILE_NAME = 'scripts/configure.conf'

def prepare():

    confFile=ctx.get_resource(CONFIG_FILE_NAME)

    ctx.logger.info('prop1: {0}'.format(env.host_string))
    ctx.logger.info('prop2: {0}'.format(env.user))
    ctx.logger.info('prop3: {0}'.format(env.password))
    ctx.logger.info('Config: {0}'.format(confFile))

def execute_cmd():

    ctx.logger.info('Start Main')

    prepare()

    confFile=ctx.get_resource(CONFIG_FILE_NAME)
    fortinet_host=env.host_string
    fortinet_user=env.user
    fortinet_pass=env.password
    fortinet_vdom='root'
    running = confFile

    ctx.logger.info('Connect to Fortinet: {0}'.format(fortinet_host))
    env.hosts = [fortinet_host]

    ctx.logger.info('execute command')
    run(confFile)

    ctx.logger.info('Done')


