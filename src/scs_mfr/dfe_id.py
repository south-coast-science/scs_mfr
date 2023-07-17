#!/usr/bin/env python3

"""
Created on 26 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The dfe_id utility is used to read the vendor, product ID and product UUID fields from the EEPROM on a
South Coast Science digital front-end (DFE) board.

DFE boards conform to Raspberry Pi HAT and BeagleBone Cape standards, as appropriate, and have differing fields, as
required by the respective standards.

SYNOPSIS
dfe_id.py

EXAMPLES
./dfe_id.py

DOCUMENT EXAMPLE
{"vendor": null, "product": null, "product_id": null, "product_ver": null, "uuid": null}

SEE ALSO
scs_mfr/eeprom_read
scs_mfr/eeprom_write

BUGS
The utility is not currently functional on BeagleBone systems.
"""

from scs_core.data.json import JSONify

from scs_dfe.interface.interface_id import InterfaceID


# TODO: fix dfe_id.py
# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ------------------------------------------------------------------------------------------------------------
    # resources...

    product_id = InterfaceID()

    # ------------------------------------------------------------------------------------------------------------
    # run...

    jstr = JSONify.dumps(product_id)
    print(jstr)
