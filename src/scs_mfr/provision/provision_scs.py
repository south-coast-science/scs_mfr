"""
Created on 14 Jul 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import spidev

from scs_core.model.gas.gas_model_conf import GasModelConf
from scs_core.model.pmx.pmx_model_conf import PMxModelConf

from scs_host.sys.host import Host

from scs_mfr.provision.provision import Provision


# --------------------------------------------------------------------------------------------------------------------

class ProvisionSCS(Provision):
    """
    classdocs
    """

    SPIDEV_VERSION = '3.6.1.dev1'

    MFR = '~/SCS/scs_mfr/src/scs_mfr/'
    DEV = '~/SCS/scs_dev/src/scs_dev/'

    __MODEL_MAPS = {'scs-bbe-': 'uE.1', 'scs-cube-': 'oE.1'}      # oE.1 or oM.2

    __GAS_PIPE = 'pipes/lambda-gas-model.uds'
    __GAS_MODEL_INTERFACE = 'vE'

    __PMX_PIPE = 'pipes/lambda-pmx-model.uds'
    __PMX_MODEL_INTERFACE = 's2'

    __CLIMATE_INTERVAL = 60                         # seconds


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def default_model_map(cls):
        return cls.__MODEL_MAPS[Host.hostname_prefix()]


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, model_map=None, verbose=False):
        """
        Constructor
        """
        super().__init__(verbose=verbose)

        self._model_map = self.default_model_map() if model_map is None else model_map


    # ----------------------------------------------------------------------------------------------------------------
    # flags...

    def on_abort(self):
        self._scs_configuration_completed.lower_flag()
        self._root_setup_completed.lower_flag()


    def raise_scs_configuration_completed(self):
        self._scs_configuration_completed.raise_flag()


    def wait_for_root_setup_completed(self):
        self._root_setup_completed.wait_for_raised()


    def lower_root_setup_completed(self):
        self._root_setup_completed.lower_flag()


    # ----------------------------------------------------------------------------------------------------------------
    # Stage 1...

    def upgrade_pips(self):
        self._logger.info("Upgrade pips...")

        self._clu.s(['pip', 'install', '--upgrade', 'pip'], no_verbose=True)
        self._clu.s(['pip', 'install', '--upgrade', 'requests'], no_verbose=True)

        if spidev.__version__ != self.SPIDEV_VERSION:
            self._clu.s(['pip', 'uninstall', '-y', 'spidev', '&&',
                         'pip', 'install', 'git+https://github.com/tim-seoss/py-spidev.git@v' + self.SPIDEV_VERSION],
                        no_verbose=True)


    def upgrade_scs(self):
        self._logger.info("Upgrade scs...")

        self._clu.s([self.MFR + 'git_pull.py', '-p', '-t', 60])


    def include_gases(self, afe_serial, dsi_serial, dsi_calibration_date, scd30):
        self._logger.info("Include gases...")

        self._clu.s([self.MFR + 'schedule.py', '-s', 'scs-gases', 10, 1])

        if afe_serial or dsi_serial:
            self._clu.s([self.MFR + 'afe_baseline.py', '-z'])
            self._clu.s([self.MFR + 'gas_baseline.py', '-d'])
            self._clu.s([self.MFR + 'vcal_baseline.py', '-d'])

        if scd30:
            self._clu.s([self.MFR + 'scd30_baseline.py', '-d'])

        if afe_serial:
            self._clu.s([self.MFR + 'afe_calib.py', '-a', afe_serial])
            self._clu.s([self.MFR + 'gas_model_conf.py', '-u', self.__GAS_PIPE, '-i', self.__GAS_MODEL_INTERFACE,
                         '-m', self._model_map])

        if dsi_serial:
            self._clu.s([self.MFR + 'afe_calib.py', '-s', dsi_serial, dsi_calibration_date])
            self._clu.s([self.MFR + 'gas_model_conf.py', '-u', self.__GAS_PIPE, '-i', self.__GAS_MODEL_INTERFACE,
                         '-m', self._model_map])

        if scd30:
            self._clu.s([self.MFR + 'scd30_conf.py', '-i', 5, '-t', 0.0])


    def remove_gases(self):
        self._logger.info("Remove gases...")

        self._clu.s([self.MFR + 'schedule.py', '-r', 'scs-gases'])

        self._clu.s([self.MFR + 'afe_calib.py', '-d'])
        self._clu.s([self.MFR + 'afe_baseline.py', '-d'])
        self._clu.s([self.MFR + 'gas_baseline.py', '-d'])
        self._clu.s([self.MFR + 'vcal_baseline.py', '-d'])
        self._clu.s([self.MFR + 'scd30_baseline.py', '-d'])
        self._clu.s([self.MFR + 'gas_model_conf.py', '-d'])


    def update_models(self, electrochems_are_being_set):
        self._logger.info("Updating models...")

        # GasModelConf...
        if GasModelConf.load(Host) is not None and not electrochems_are_being_set:
            self._clu.s([self.MFR + 'gas_model_conf.py', '-u', self.__GAS_PIPE, '-i', self.__GAS_MODEL_INTERFACE,
                         '-m', self._model_map])

        # PMxModelConf...
        if PMxModelConf.load(Host) is not None:
            self._clu.s([self.MFR + 'pmx_model_conf.py', '-u', self.__PMX_PIPE, '-i', self.__PMX_MODEL_INTERFACE,
                         '-m', self._model_map])


    def set_schedule(self):
        self._logger.info("Set schedule...")

        self._clu.s([self.MFR + 'schedule.py', '-s', 'scs-climate', self.__CLIMATE_INTERVAL, 1])


    def include_pressure(self):
        self._logger.info("Barometric pressure...")

        self._clu.s([self.MFR + 'pressure_conf.py', '-m', 'ICP'])


    def psu_model(self, model):
        self._logger.info("PSU...")

        self._clu.s([self.MFR + 'psu_conf.py', '-p', model])


    def timezone(self, timezone):
        self._logger.info("Timezone...")

        self._clu.s([self.MFR + 'timezone.py', '-s', timezone])


    def system_id(self):
        self._logger.info("System ID...")

        self._clu.s([self.MFR + 'system_id.py', '-a'])


    def aws_project(self, org, group, location, force):
        self._logger.info("AWS project...")

        self._clu.s([self.MFR + 'aws_project.py', '-s', org, group, location, '-f' if force else None])


    # ----------------------------------------------------------------------------------------------------------------
    # Stage 2...

    def aws_deployment(self):
        self._logger.info("AWS deployment...")

        self._clu.s([self.MFR + 'aws_deployment.py', '-w', '-i', 4])


    def cognito_identity(self, invoice_number):
        self._logger.info("Cognito identity...")

        self._clu.s([self.MFR + 'shared_secret.py', '-g', '-i'])
        self._clu.s([self.MFR + 'cognito_device_credentials.py', '-a', invoice_number])


    def test(self):
        self._logger.info("Test...")

        self._clu.s([self.DEV + 'status_sampler.py', '-i', 10, '-c', 2], abort_on_fail=False)
        self._clu.s([self.DEV + 'climate_sampler.py'], abort_on_fail=False)
        self._clu.s([self.DEV + 'particulates_sampler.py'], abort_on_fail=False)
        self._clu.s([self.DEV + 'gases_sampler.py'], abort_on_fail=False)
        self._clu.s([self.DEV + 'psu_monitor.py'], abort_on_fail=False)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ProvisionSCS:{model_map:%s, scs_configuration_completed:%s, root_setup_completed:%s, clu:%s}" % \
            (self._model_map, self._scs_configuration_completed, self._root_setup_completed, self._clu)
