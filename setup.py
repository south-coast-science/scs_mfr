#!/usr/bin/env python3

"""
Created on 4 Sep 2020
Updated 23 Mar 2021

@author: Jade Page (jade.page@southcoastscience.com)

https://packaging.python.org/tutorials/packaging-projects/
https://packaging.python.org/guides/single-sourcing-package-version/
"""

import codecs
import os

from setuptools import setup, find_packages


# --------------------------------------------------------------------------------------------------------------------

def read(rel_path):
    here = str(os.path.abspath(os.path.dirname(__file__)))
    with codecs.open(os.path.join(here, rel_path)) as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            return line.split("'")[1]
    else:
        raise RuntimeError("Unable to find version string.")


# --------------------------------------------------------------------------------------------------------------------

with open('requirements.txt') as req_txt:
    required = [line for line in req_txt.read().splitlines() if line]


setup(
    name='scs_mfr',
    version=get_version("src/scs_mfr/__init__.py"),
    description='High-level scripts and command-line applications for South Coast Science '
                'environmental monitor manufacturing, test and calibration.',
    author='South Coast Science',
    author_email='contact@southcoastscience.com',
    url='https://github.com/south-coast-science/scs_mfr',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: POSIX',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    scripts=[
        'src/scs_mfr/afe_baseline.py',
        'src/scs_mfr/afe_calib.py',
        'src/scs_mfr/airnow_site_conf.py',
        'src/scs_mfr/aws_client_auth.py',
        'src/scs_mfr/aws_deployment.py',
        'src/scs_mfr/aws_group_cloner.py',
        'src/scs_mfr/aws_group_deployment.py',
        'src/scs_mfr/aws_group_setup.py',
        'src/scs_mfr/aws_identity.py',
        'src/scs_mfr/aws_project.py',
        'src/scs_mfr/configuration.py',
        'src/scs_mfr/csv_logger_conf.py',
        'src/scs_mfr/csv_reader.py',
        'src/scs_mfr/csv_writer.py',
        'src/scs_mfr/dfe_id.py',
        'src/scs_mfr/dfe_test.py',
        'src/scs_mfr/display_conf.py',
        'src/scs_mfr/eeprom_read.py',
        'src/scs_mfr/eeprom_write.py',
        'src/scs_mfr/fuel_gauge_calib.py',
        'src/scs_mfr/gas_baseline.py',
        'src/scs_mfr/gas_model_conf.py',
        'src/scs_mfr/gauge_conf.py',
        'src/scs_mfr/git_pull.py',
        'src/scs_mfr/gps_conf.py',
        'src/scs_mfr/host_id.py',
        'src/scs_mfr/interface_conf.py',
        'src/scs_mfr/modem.py',
        'src/scs_mfr/mpl115a2_calib.py',
        'src/scs_mfr/mpl115a2_conf.py',
        'src/scs_mfr/mqtt_conf.py',
        'src/scs_mfr/ndir_conf.py',
        'src/scs_mfr/opc_cleaning_interval.py',
        'src/scs_mfr/opc_conf.py',
        'src/scs_mfr/opc_firmware_conf.py',
        'src/scs_mfr/opc_version.py',
        'src/scs_mfr/pmx_model_conf.py',
        'src/scs_mfr/psu_conf.py',
        'src/scs_mfr/pt1000_calib.py',
        'src/scs_mfr/rtc.py',
        'src/scs_mfr/scd30_conf.py',
        'src/scs_mfr/schedule.py',
        'src/scs_mfr/shared_secret.py',
        'src/scs_mfr/sht_conf.py',
        'src/scs_mfr/system_id.py',
        'src/scs_mfr/timezone.py'
    ],
    install_requires=required,
    platforms=['any'],
    python_requires=">=3.3"
)
