#!/usr/bin/env python3

"""
Created on 19 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The csv_writer utility is used to convert from JSON format to comma-separated value (CSV) format.

The path into the JSON document is used to name the column in the header row, with JSON nodes separated by a period
('.') character.

All the leaf nodes of the first JSON document are included in the CSV. If subsequent JSON documents in the input stream
contain fields that were not in this first document, these extra fields are ignored.

SYNOPSIS
csv_writer.py [-c] [-a] [-e] [-v] [FILENAME]

EXAMPLES
./socket_receiver.py | ./csv_writer.py temp.csv -e

DOCUMENT EXAMPLE - INPUT
{"tag": "scs-ap1-6", "rec": "2018-04-04T14:50:27.641+00:00", "val": {"hmd": 59.6, "tmp": 23.8}}

DOCUMENT EXAMPLE - OUTPUT
tag,rec,val.hmd,val.tmp
scs-ap1-6,2018-04-04T14:50:38.394+00:00,59.7,23.8

SEE ALSO
scs_mfr/csv_reader
"""

import sys

from scs_core.csv.csv_writer import CSVWriter

from scs_mfr.cmd.cmd_csv_writer import CmdCSVWriter


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    cmd = None
    csv = None

    try:
        # ------------------------------------------------------------------------------------------------------------
        # cmd...

        cmd = CmdCSVWriter()

        if cmd.verbose:
            print(cmd, file=sys.stderr)


        # ------------------------------------------------------------------------------------------------------------
        # resources...

        csv = CSVWriter(cmd.filename, cmd.cache, cmd.append)

        if cmd.verbose:
            print(csv, file=sys.stderr)
            sys.stderr.flush()


        # ------------------------------------------------------------------------------------------------------------
        # run...

        for line in sys.stdin:
            datum = line.strip()

            if datum is None:
                break

            csv.write(datum)

            # echo...
            if cmd.echo:
                print(datum)
                sys.stdout.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("csv_writer: KeyboardInterrupt", file=sys.stderr)

    finally:
        if csv is not None:
            csv.close()
