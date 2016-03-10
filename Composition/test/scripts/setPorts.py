from fabric.api import run, put
from cloudify import ctx

def setPorts(fw_ip, lb_ip,host_ip):
    ctx.logger.info('set fw ports : fw ip  {0}, lb ip {1}, on host : {2}'.format(fw_ip, lb_ip, host_ip))

    command = \
        'config system interface\n' \
        '  edit port2\n' \
        '    set mode static\n' \
        '    set allowaccess ping http https\n' \
        '    set alias out\n' \
        '    set ip %s 255.255.255.0\n' \
        '  next\n' \
        'end' % (lb_ip)

    ctx.logger.info('executing command {0}'.format(command))

    run(command)


    command = \
        'config system interface\n' \
        '  edit port3\n' \
        '    set mode static\n' \
        '    set allowaccess ping http https\n' \
        '    set alias out\n' \
        '    set ip %s 255.255.255.248\n' \
        '  next\n' \
        'end' % (fw_ip)

    ctx.logger.info('executing command {0}'.format(command))

    run(command)
