"""
Created on 14 Jul 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.sys.command import Command
from scs_core.sys.logging import Logging

from scs_host.sync.flag import Flag


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
        self.__scs_configuration_completed = Flag('scs-configuration-completed')
        self.__root_setup_completed = Flag('root-setup-completed')

        self.__clu = Command(verbose, on_abort=self.on_abort)

        self.__logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------
    # flags...

    def on_abort(self):
        self.__scs_configuration_completed.lower_flag()
        self.__root_setup_completed.lower_flag()


    def raise_root_setup_completed(self):
        self.__root_setup_completed.raise_flag()


    def wait_for_scs_configuration_completed(self):
        self.__scs_configuration_completed.wait_for_raised()


    def lower_scs_configuration_completed(self):
        self.__scs_configuration_completed.lower_flag()


    # ----------------------------------------------------------------------------------------------------------------
    # Stage 1...

    def stop(self):
        self.__logger.info("Stop...")

        self.__clu.s(['systemctl', 'stop', 'scs_*'], no_verbose=True)


    def prep_sd(self):
        self.__logger.info("SD card...")

        self.__clu.s(['prep-sd', '-f'], no_verbose=True)


    # ----------------------------------------------------------------------------------------------------------------
    # Stage 2...

    def identity(self):
        self.__logger.info("AWS identity...")

        self.__clu.s(['aws_identity', '-s'])


    def setup(self):
        self.__logger.info("AWS setup...")

        self.__clu.s(['aws_group_setup', '-f', '-i', 4, '-s'])

        self.__clu.s(['rm', '-f', '/usr/local/etc/scs_machine_uncommissioned'], no_verbose=True, abort_on_fail=False)
        self.__clu.s(['systemctl', 'enable', 'scs_*'], no_verbose=True, abort_on_fail=False)
        self.__clu.s(['systemctl', 'disable', 'scs_mqtt_client.service'], no_verbose=True, abort_on_fail=False)
        self.__clu.s(['rm', '-f', 'scs_mqtt_client.service'], no_verbose=True, abort_on_fail=False)
        self.__clu.s(['systemctl', 'start', 'scs_greengrass.service'], no_verbose=True)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ProvisionRoot:{scs_configuration_completed:%s, root_setup_completed:%s, clu:%s}" % \
            (self.__scs_configuration_completed, self.__root_setup_completed, self.__clu)
