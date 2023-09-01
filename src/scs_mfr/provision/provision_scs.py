"""
Created on 14 Jul 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import spidev

from scs_core.sys.command import Command
from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class ProvisionSCS(object):
    """
    classdocs
    """

    SPIDEV_VERSION = '3.6.1.dev1'

    MFR = '/home/scs/SCS/scs_mfr/src/scs_mfr/'
    DEV = '/home/scs/SCS/scs_dev/src/scs_dev/'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, verbose=False):
        """
        Constructor
        """
        self.__clu = Command(verbose)
        self.__logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------
    # Stage 1...

    def os_info(self):
        self.__logger.info("OS info...")

        self.__clu.s(['uname', '-r'], no_verbose=True)          # equivalent to platform.uname().release


    def upgrade_pips(self):
        self.__logger.info("Upgrade pips...")

        self.__clu.s(['pip', 'install', '--upgrade', 'pip'], no_verbose=True)
        self.__clu.s(['pip', 'install', '--upgrade', 'requests'], no_verbose=True)

        if spidev.__version__ != self.SPIDEV_VERSION:
            self.__clu.s(['pip', 'uninstall', '-y', 'spidev', '&&',
                          'pip', 'install', 'git+https://github.com/tim-seoss/py-spidev.git@' + self.SPIDEV_VERSION],
                         no_verbose=True)


    def upgrade_scs(self):
        self.__logger.info("Upgrade scs...")

        self.__clu.s([self.MFR + 'git_pull.py', '-p', '-t', 60])


    def include_gases(self, afe_serial, dsi_serial, dsi_calibration_date, scd30):
        self.__logger.info("Include gases...")

        if afe_serial or dsi_serial:
            self.__clu.s([self.MFR + 'afe_baseline.py', '-z'])
            self.__clu.s([self.MFR + 'gas_baseline.py', '-d'])
            self.__clu.s([self.MFR + 'vcal_baseline.py', '-d'])

        if scd30:
            self.__clu.s([self.MFR + 'scd30_baseline.py', '-d'])

        if afe_serial:
            self.__clu.s([self.MFR + 'afe_calib.py', '-a', afe_serial])

        if dsi_serial:
            self.__clu.s([self.MFR + 'afe_calib.py', '-s', dsi_serial, dsi_calibration_date])

        if scd30:
            self.__clu.s([self.MFR + 'scd30_conf.py', '-i', 5, '-t', 0.0])


    def remove_gases(self):
        self.__logger.info("Remove gases...")

        self.__clu.s([self.MFR + 'afe_calib.py', '-d'])
        self.__clu.s([self.MFR + 'afe_baseline.py', '-d'])
        self.__clu.s([self.MFR + 'gas_baseline.py', '-d'])
        self.__clu.s([self.MFR + 'vcal_baseline.py', '-d'])
        self.__clu.s([self.MFR + 'scd30_baseline.py', '-d'])
        self.__clu.s([self.MFR + 'gas_model_conf.py', '-d'])
        self.__clu.s([self.MFR + 'schedule.py', '-r', 'scs-gases'])


    def include_pressure(self):
        self.__logger.info("Barometric pressure...")

        self.__clu.s([self.MFR + 'pressure_conf.py', '-m', 'ICP'])


    def psu_model(self, model):
        self.__logger.info("PSU...")

        self.__clu.s([self.MFR + 'psu_conf.py', '-p', model])


    def timezone(self, timezone):
        self.__logger.info("Timezone...")

        self.__clu.s([self.MFR + 'timezone.py', '-s', timezone])


    def system_id(self, invoice_number):
        self.__logger.info("System ID...")

        self.__clu.s([self.MFR + 'system_id.py', '-a'])
        self.__clu.s([self.MFR + 'shared_secret.py', '-g', '-i'])
        self.__clu.s([self.MFR + 'cognito_device_credentials.py', '-a', invoice_number])


    def aws_project(self, org, group, location):
        self.__logger.info("AWS project...")

        self.__clu.s([self.MFR + 'aws_project.py', '-s', org, group, location])


    # ----------------------------------------------------------------------------------------------------------------
    # Stage 2...

    def aws_deployment(self):
        self.__logger.info("AWS deployment...")

        self.__clu.s([self.MFR + 'aws_deployment.py', '-w', '-i', 4])


    def test(self):
        self.__logger.info("Test...")

        self.__clu.s([self.DEV + 'status_sampler.py', '-i', 12, '-c', 1])
        self.__clu.s([self.DEV + 'climate_sampler.py'])
        self.__clu.s([self.DEV + 'particulates_sampler.py'])
        self.__clu.s([self.DEV + 'gases_sampler.py'])
        self.__clu.s([self.DEV + 'psu_monitor.py'])


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ProvisionSCS:{clu:%s}" % self.__clu
