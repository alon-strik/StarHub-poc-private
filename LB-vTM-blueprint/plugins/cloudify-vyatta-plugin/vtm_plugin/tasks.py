# coding=utf-8
## vTM Brocade load balancer

from cloudify.decorators import operation
from cloudify.state import ctx_parameters as inputs
import re
import urllib
import requests
requests.packages.urllib3.disable_warnings()  


@operation
def port_config(ctx, **kwargs):
    ctx.logger.info('Start port config task....')
    command = []
    port_idx = 4

    vtm_host_ip = get_host_ip(ctx)
    ctx.logger.info('vtm_host_ip: {0}'.format(vtm_host_ip))

    for relationship in ctx.instance.relationships:
        ctx.logger.info('RELATIONSHIP type : {0}'.format(relationship.type))

        if 'connected_to' in relationship.type:
            target_ip = relationship.target.instance.runtime_properties['fixed_ip_address']
            ctx.logger.info('TARGET IP target_ip : {0}'.format(target_ip))
            cmd = 'set interfaces dataplane dp0s' + port_idx + ' description ' + relationship.target.node.name
            command.append(cmd)
            cmd = 'set interfaces dataplane dp0s' + port_idx + ' address ' + target_ip + '/24'
            command.append(cmd)
            port_idx = +1

        exec_command(ctx, command, vtm_host_ip)


@operation
def port_local_config(ctx, **kwargs):
    ctx.logger.info('Start local port config task....')
    command = []
    port_idx = 1

    vtm_host_ip = get_host_ip(ctx)
    ctx.logger.info('vtm_host_ip: {0}'.format(vtm_host_ip))

    for relationship in ctx.instance.relationships:
        ctx.logger.info('RELATIONSHIP type : {0}'.format(relationship.type))

        if 'connected_to' in relationship.type:
            target_ip = relationship.target.instance.runtime_properties['fixed_ip_address']
            ctx.logger.info('TARGET IP target_ip : {0}'.format(target_ip))
            cmd = 'set interfaces dataplane dp0s' + port_idx + ' description ' + relationship.target.node.name
            command.append(cmd)
            cmd = 'set interfaces dataplane dp0s' + port_idx + ' address ' + target_ip + '/24'
            command.append(cmd)
            port_idx = +1

        exec_command(ctx, command, vtm_host_ip)


@operation
def route_policy_config(ctx, **kwargs):
    ctx.logger.info('Start route policy task....')
    command = []

    vtm_host_ip = get_host_ip(ctx)
    ctx.logger.info('vtm_host_ip: {0}'.format(vtm_host_ip))

    # for relationship in ctx.instance.relationships:
    #     ctx.logger.info('RELATIONSHIP type : {0}'.format(relationship.type))
    #
    #     if 'connected_to' in relationship.type:
    #         target_ip = relationship.target.instance.runtime_properties['fixed_ip_address']
    #         ctx.logger.info('TARGET IP target_ip : {0}'.format(target_ip))
    #         cmd = 'set interfaces dataplane dp0s' + port_idx + ' description ' + relationship.target.node.name
    #         command.append(cmd)
    #         cmd = 'set interfaces dataplane dp0s' + port_idx + ' address ' + target_ip + '/24'
    #         command.append(cmd)
    #         port_idx = +1


    ### need to add ploicy here ....

    exec_command(ctx, command, vtm_host_ip)


#
# 1) Creating a Test Pool
# URI : https://10.88.88.42:9070/api/tm/3.5/config/active/pools/Test-Pool
#
# 2) Changing the load balancing alogrithm to Least Connections
# URI : https://10.88.88.42:9070/api/tm/3.5/config/active/pools/Test-Pool
#
# 3) Create a session persistence class
# URI : https://10.88.88.42:9070/api/tm/2.0/config/active/persistence/Persistence
#
# 4) Assigning a session persistence class to “Test-Pool”
# URI : https://10.88.88.42:9070/api/tm/3.5/config/active/pools/Test-Pool
#
# 5) Creating a Traffic IP Group named Test-TIP
# URI : https://10.88.88.42:9070/api/tm/2.0/config/active/traffic_ip_groups/Test-TIP
#
# 6) Creating a Virtual Server “Test-VS”, the virtual server is associated with  traffic IP “Test-IP” and server pool “Test-Pool”
# URI : https://10.88.88.42:9070/api/tm/2.0/config/active/virtual_servers/Test-VS
#

class vtmControl(object):
    """
    Provides methods to modify vTM configurations.
    """

    def __init__(self, urlBase, user, passwd, ctx):

        self.urlBase = urlBase
# configuration API
        self.urlConfBase = urlBase + 'api/tm'
        self.user = user
        self.passwd = passwd

    def getOpId(self, urlOpId, ctx):
        """
        Get the operation id, which is substring of the Location header in HTTP response.
        """

        rop = requests.post(urlOpId, auth=(self.user, self.passwd), verify=False)  # Request to get operation id
        return rop.headers['Location'].split('/')[2]  # Get Location header

    def getConfId(self, ctx):
        """
        Get the configuration id, which is substring of the Location header in HTTP response.
        """

        rconf = requests.post(self.urlConfBase, auth=(self.user, self.passwd), verify=False)
        return rconf.headers['Location'].split('/')[2]

    def deleteConfId(self, confId, ctx):
        """
        Delete existing vtm configuration session
        """

        urlConfDelete = self.urlConfBase + '/' + confId
        rdel = requests.delete(urlConfDelete, auth=(self.user, self.passwd), verify=False)
        return rdel.status_code

    def commandOperational(self, opCommands, ctx):
        """
        Call vtm operational mode commands from opCommands list.
        """
        for line in opCommands:
            urlOpCommand = self.urlOpBase + '/' + '/'.join(line.split(None))
            ropResult = requests.get(self.urlOpBase + '/' + self.getOpId(urlOpCommand),
                                     auth=(self.user, self.passwd),
                                     verify=False)  # Request to get the results

            ctx.logger.info('$ : {0}'.format(line))
            ctx.logger.info('{0}'.format(ropResult.text))

    def createEncodedUrl(self, confId, string, ctx):
        """
        URLencode every configuration words and form proper URL for REST API requests.
        :param confId: Configuration session ID
        :param string: One line vtm configuration commands and parameters
        :return: Encoded URL for vtm REST API
        """

        encodedWord = []
        for word in string.split():
            encodedWord.append(urllib.quote(word, safe=""))  # Encode each words, then make a list of words

        encodedUrl = self.urlConfBase + '/' + confId + '/' + '/'.join(' '.join(encodedWord).split(None))
        return encodedUrl

    def editConfig(self, config, ctx):
        """
        Read configurations from a LIST and send requests to vtm via REST API,
        then actually modify vtm configuration and commit configuration changes.
        """

        # Set configurations
        confId = self.getConfId()  # Get configuration ID

        for line in config:
            if not (re.compile("^#").match(line)
                    or re.compile("^$").match(line)):  # Skip line matches with "^#" or "^$"
                urlConfPut = self.createEncodedUrl(confId, line)
                rconf = requests.put(urlConfPut,
                                     auth=(self.user, self.passwd),
                                     verify=False)  # Request for configuration commands

                print("%s : %s" % (urlConfPut, rconf.status_code))

        # Commit configurations
        self.commitConfig(confId)

        # Save configurations
        self.saveConfig(confId)

        # Delete conf-id and return HTTP status code
        return self.deleteConfId(confId)

    def commitConfig(self, confId, ctx):
        """
        Commit configuration changes
        """

        urlConfCommit = self.urlConfBase + '/' + confId + '/commit'
        rconf = requests.post(urlConfCommit, auth=(self.user, self.passwd), verify=False)  # Request for commit
        ctx.logger.info('{0}  :  {1}'.format(urlConfCommit, rconf.status_code))
        return rconf.status_code

    def saveConfig(self, confId, ctx):
        """
         Save changes
        """
        urlConfSave = self.urlConfBase + '/' + confId + '/save'
        rconf = requests.post(urlConfSave, auth=(self.user, self.passwd), verify=False)  # Request for save
        ctx.logger.info('{0}  :  {1}'.format(urlConfSave, rconf.status_code))
        return rconf.status_code


def exec_command(ctx, command, vtm_host_ip):

    ctx.logger.info('Open connection to host {0} '.format(vtm_host_ip))

    vtm_username = 'admin'
    vtm_password = 'admin'
    urlBase = 'https://' + vtm_host_ip + ':9070/'

    vy = vtmControl(ctx, urlBase, vtm_username, vtm_password)

    vy.editConfig(command)

    #vy.commandOperationalList(['show interfaces'])


def get_host_ip(ctx):
    for relationship in ctx.instance.relationships:
        if 'contained_in' in relationship.type:
            return relationship.target.instance.runtime_properties['ip']


def get_host_id(ctx):
    ctx.instance._get_node_instance_if_needed()
    return ctx.instance._node_instance.host_id
