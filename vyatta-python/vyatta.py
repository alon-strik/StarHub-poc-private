#!/usr/bin/env python

import re
import urllib
import requests

requests.packages.urllib3.disable_warnings()  # Surpress "InsecureRequestWarning" warning
import logging

# logging.warning('Watch out!') # will print a message to the console


VYUSER = "vyatta"
VYPASSWD = "vyatta"
URLBASE = "https://192.168.122.23/"


class VyattaControl(object):
    """
    Provides methods to show and modify Vyatta status and configurations.
    """

    def __init__(self, urlBase, user, passwd):

        self.urlBase = urlBase
        self.urlConfBase = urlBase + 'rest/conf'
        self.urlOpBase = urlBase + 'rest/op'
        self.user = user
        self.passwd = passwd

    def getOpId(self, urlOpId):
        """
        Get the operation id, which is substring of the Location header in HTTP response.

        :param urlOpPost:
        :return:
        """

        rop = requests.post(urlOpId, auth=(self.user, self.passwd), verify=False)  # Request to get operation id
        return rop.headers['Location'].split('/')[2]  # Get Location header

    def getConfId(self):
        """
        Get the configuration id, which is substring of the Location header in HTTP response.
        :return:
        """

        rconf = requests.post(self.urlConfBase, auth=(self.user, self.passwd), verify=False)
        logging.warning('>> conf-id: {0}'.format(rconf.headers['Location'].split('/')[2]))
        return rconf.headers['Location'].split('/')[2]

    def deleteConfId(self, confId):
        """
        Delete existing Vyatta configuration session
        """

        urlConfDelete = self.urlConfBase + '/' + confId
        rdel = requests.delete(urlConfDelete, auth=(self.user, self.passwd), verify=False)
        return rdel.status_code

    def commandOperational(self, opCommandFileName):
        """
        Call Vyatta operational mode commands from opCommandFileName file.
        :param opCommandFileName: Input file for Vyatta operational mode commands
        :return:
        """

        with open(opCommandFileName) as opCommandFile:
            for line in opCommandFile:
                urlOpCommand = self.urlOpBase + '/' + '/'.join(line.split(None))
                ropResult = requests.get(self.urlOpBase + '/' + self.getOpId(urlOpCommand),
                                         auth=(self.user, self.passwd),
                                         verify=False)  # Request to get the results
                print('$ ' + line)
                print(ropResult.text)

    def commandOperationalList(self, opCommands):
        """
        Call Vyatta operational mode commands from opCommands list.
        """
        for line in opCommands:
            urlOpCommand = self.urlOpBase + '/' + '/'.join(line.split(None))
            ropResult = requests.get(self.urlOpBase + '/' + self.getOpId(urlOpCommand),
                                     auth=(self.user, self.passwd),
                                     verify=False)  # Request to get the results
            print('$ ' + line)
            print(ropResult.text)
            return ropResult




    def createEncodedUrl(self, confId, string):
        """
        URLencode every configuration words and form proper URL for REST API requests.
        :param confId: Configuration session ID
        :param string: One line Vyatta configuration commands and parameters
        :return: Encoded URL for Vyatta REST API
        """

        encodedWord = []
        for word in string.split():
            encodedWord.append(urllib.quote(word, safe=""))  # Encode each words, then make a list of words

        encodedUrl = self.urlConfBase + '/' + confId + '/' + '/'.join(' '.join(encodedWord).split(None))
        return encodedUrl

    def editConfig(self, confFileName):
        """
        Read configurations from a file and send requests to Vyatta via REST API,
        then actually modify Vyatta configuration and commit configuration changes.
        """

        # Set configurations
        with open(confFileName) as confFile:

            confId = self.getConfId()  # Get configuration ID

            for line in confFile:
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

    def editConfigList(self, config):
        """
        Read configurations from a LIST and send requests to Vyatta via REST API,
        then actually modify Vyatta configuration and commit configuration changes.
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

    def commitConfig(self, confId):
        """
        Commit configuration changes
        """

        urlConfCommit = self.urlConfBase + '/' + confId + '/commit'
        rconf = requests.post(urlConfCommit, auth=(self.user, self.passwd), verify=False)  # Request for commit
        print("%s : %s" % (urlConfCommit, rconf.status_code))
        return rconf.status_code

    def saveConfig(self, confId):
        """
         Save changes
        """
        urlConfCommit = self.urlConfBase + '/' + confId + '/save'
        rconf = requests.post(urlConfCommit, auth=(self.user, self.passwd), verify=False)  # Request for save
        print("%s : %s" % (urlConfCommit, rconf.status_code))
        return rconf.status_code


if __name__ == "__main__":

    user = VYUSER
    passwd = VYPASSWD
    urlBase = URLBASE

    vy = VyattaControl(urlBase, user, passwd)

#    vy.editConfigList(['set interfaces dataplane dp0s4 address 172.10.1.1/24',
#                       'set interfaces dataplane dp0s7 address 10.1.1.1/24'])

#    vy.editConfigList(['delete interfaces dataplane dp0s4',
#                       'delete interfaces dataplane dp0s7'])

    resp = vy.commandOperationalList(['show interfaces'])

    print "------------------"
    interfaces = []
    for interface in resp:
        if 'dp0s' in interface:
            interfaces.append(interface)
    print interfaces

#ip addr | grep dp0s | grep : | awk  '{print $2}' | cut -d':' -f 1