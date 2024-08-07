"""
Created on 28 Nov 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from abc import ABC, abstractmethod

from scs_core.sys.command import Command
from scs_core.sys.logging import Logging

from scs_host.sync.flag import Flag
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

class Provision(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, verbose=False):
        """
        Constructor
        """
        self._scs_configuration_completed = Flag('scs-configuration-completed')
        self._root_setup_completed = Flag('root-setup-completed')
        self._scs_deployment_completed = Flag('scs-deployment-completed')

        self._clu = Command(verbose=verbose, on_abort=self.on_abort)

        self._logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------
    # flags...

    @abstractmethod
    def on_abort(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------
    # Check...

    def os_check(self):
        self._logger.info("OS info...")

        current = Host.os_release()
        self._logger.info("current = %s" % current)

        if not Host.has_acceptable_os_release():
            self._logger.error('unacceptable OS release.')
            self._clu.abort(1)


    def kernel_check(self):
        self._logger.info("Kernel info...")

        current = Host.kernel_release()
        self._logger.info("current = %s" % current)

        if not Host.has_acceptable_kernel_release():
            self._logger.error('unacceptable kernel release.')
            self._clu.abort(1)


    def greengrass_check(self):
        self._logger.info("Greengrass info...")

        current = Host.greengrass_version()
        required = Host.minimum_required_greengrass_version()

        self._logger.info("current = %s required >= %s" % (current.as_json(), required.as_json()))

        if current < required:
            self._logger.error('unacceptable greengrass version.')
            self._clu.abort(1)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        name = self.__class__.__name__
        return name + ":{scs_configuration_completed:%s, root_setup_completed:%s, scs_deployment_completed: %s, " \
                      "clu:%s}" % \
            (self._scs_configuration_completed, self._root_setup_completed, self._scs_deployment_completed,
             self._clu)
