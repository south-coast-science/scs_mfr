"""
Created on 14 Jul 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aws.greengrass.v1.aws_group_version import AWSGroupVersion

from scs_mfr.provision.provision import Provision

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

class ProvisionRoot(Provision):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, verbose=False):
        """
        Constructor
        """
        super().__init__(verbose=verbose)


    # ----------------------------------------------------------------------------------------------------------------
    # flags...

    def on_abort(self):
        self._scs_configuration_completed.lower_flag()
        self._root_setup_completed.lower_flag()


    def raise_root_setup_completed(self):
        self._root_setup_completed.raise_flag()


    def wait_for_scs_configuration_completed(self):
        self._scs_configuration_completed.wait_for_raised()


    def lower_scs_configuration_completed(self):
        self._scs_configuration_completed.lower_flag()


    def wait_for_scs_deployment_completed(self):
        self._scs_deployment_completed.wait_for_raised()


    def lower_scs_deployment_completed(self):
        self._scs_deployment_completed.lower_flag()


    # ----------------------------------------------------------------------------------------------------------------
    # Stage 1...

    def stop(self):
        self._logger.info("Stop...")

        self._clu.s(['systemctl', 'stop', 'scs_*'], no_verbose=True)


    def prep_sd(self):
        self._logger.info("SD card...")

        self._clu.s(['prep-sd', '-f'], no_verbose=True)


    # ----------------------------------------------------------------------------------------------------------------
    # Stage 2...

    def identity(self):
        self._logger.info("AWS identity...")

        self._clu.s(['aws_identity', '-s'])


    def setup(self):
        self._logger.info("AWS setup...")

        self._clu.s(['aws_group_setup', '-f', '-i', 4, '-s'])

        # noinspection SpellCheckingInspection
        self._clu.s(['rm', '-f', '/usr/local/etc/scs_machine_uncommissioned'], no_verbose=True, abort_on_fail=False)
        self._clu.s(['systemctl', 'enable', 'scs_*'], no_verbose=True, abort_on_fail=False)
        self._clu.s(['systemctl', 'disable', 'scs_mqtt_client.service'], no_verbose=True, abort_on_fail=False)
        self._clu.s(['rm', '-f', 'scs_mqtt_client.service'], no_verbose=True, abort_on_fail=False)
        self._clu.s(['systemctl', 'start', 'scs_greengrass.service'], no_verbose=True)


    def set_greengrass_log_level(self, log_level):
        self._logger.info("Greengrass log level...")

        group_version = AWSGroupVersion.load(Host)

        group_version.greengrass_log_level = log_level
        group_version.lambda_log_level = log_level
        group_version.save(Host)

        self._logger.info("level: %s" % log_level)
