import os
import sys
import subprocess
from cloudify import ctx
from cloudify.state import ctx_parameters as inputs

CONFIG_FILE_NAME = 'scripts/configure.conf'

def prepare():

    confFile=ctx.get_resource(CONFIG_FILE_NAME)

    ctx.logger.info('prop2: {0}'.format(inputs['host_string']))
    ctx.logger.info('prop3: {0}'.format(inputs['user']))
    ctx.logger.info('prop4: {0}'.format(inputs['password']))
    ctx.logger.info('Folder: {0}'.format(confFile))

def install_pyfg():

    ctx.logger.info('Installing pyFG module')
    pip_fpath = os.path.join(sys.prefix, 'bin', 'pip')
    cmd = [pip_fpath, 'install', 'pyFG']
    exit_code = subprocess.call(cmd)
    ctx.logger.info('Install exit code: {0}'.format(exit_code))

def main():

    ctx.logger.info('Start Main')

    prepare()

    confFile=ctx.get_resource(CONFIG_FILE_NAME)
    fortinet_host=inputs['host_string']
    fortinet_user=inputs['user']
    fortinet_pass=inputs['password']
    fortinet_vdom='root'

    install_pyfg()

    d = FortiOS(fortinet_host, username=fortinet_user, password=fortinet_pass)

    d.open()
    ctx.logger.info('Executing Command: {0}'.format(confFile))
    d.execute_command(confFile)
    d.close()
    #print d.running_config.to_text()

if __name__ == '__main__':
    main()
