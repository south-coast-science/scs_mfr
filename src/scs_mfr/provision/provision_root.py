"""
Created on 14 Jul 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.sys.command import Command
from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class ProvisionRoot(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, verbose=False):
        """
        Constructor
        """
        self.__clu = Command(verbose)
        self.__logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------
    # stage 1...

    def stop(self):
        self.__logger.info("stop...")

        self.__clu.s(['systemctl', 'stop', 'scs_*'], no_verbose=True)


    def prep_sd(self):
        self.__logger.info("prep-sd...")

        self.__clu.s(['prep-sd', '-f'], no_verbose=True)


    # ----------------------------------------------------------------------------------------------------------------
    # stage 2...

    def identity(self):
        self.__logger.info("identity...")

        self.__clu.s(['aws_identity', '-s'])


    def setup(self):
        self.__logger.info("setup...")

        self.__clu.s(['aws_group_setup', '-f', '-i', 4, '-s'])

        self.__clu.s(['rm', '-f', '/usr/local/etc/scs_machine_uncommissioned'], no_verbose=True)
        self.__clu.s(['systemctl', 'enable', 'scs_*'], no_verbose=True)
        self.__clu.s(['systemctl', 'disable', 'scs_mqtt_client.service'], no_verbose=True)
        self.__clu.s(['rm', '-f', 'scs_mqtt_client.service'], no_verbose=True)
        self.__clu.s(['systemctl', 'start', 'scs_greengrass.service'], no_verbose=True)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ProvisionRoot:{clu:%s}" % self.__clu
