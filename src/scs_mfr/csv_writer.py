#!/usr/bin/env python3

"""
Created on 19 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_mfr

DESCRIPTION
The csv_writer utility is used to convert from JSON format to comma-separated value (CSV) format.

The path into the JSON document is used to name the column in the header row: dictionary fields are separated
from their container by a period ('.') character, and array members are separated by a colon (':') character.

The --quote-all flag forces quote ('"') characters around all cell values. This is useful when long numeric
codes such as IMEI numbers are included in the data, such codes should not be interpreted as floats by
spreadsheet applications. The default behaviour is to quote only where necessary.

default mode:

All the leaf nodes of the first JSON document are included in the CSV. If subsequent JSON documents in the input stream
contain fields that were not in this first document, these extra fields are ignored. If subsequent JSON documents
do not contain a field that is in the header, then this field is given the null value.

header-scan mode:

All input documents are scanned in order to build an inclusive hearer row. Any documents that do not contain a header
fields are given a null value for that field. Any values bound to paths that become internal nodes are discarded.
Warning: the header-scan mode requires memory proportional to the size of its input.

SYNOPSIS
csv_writer.py [{ -a | -x | -s }] [-q] [-e] [-v] [FILENAME]

EXAMPLES
socket_receiver.py | csv_writer.py temp.csv -e

DOCUMENT EXAMPLE - INPUT
{"tag": "scs-ap1-6", "rec": "2018-04-04T14:50:27.641+00:00", "val": {"hmd": 59.6, "tmp": 23.8}}

DOCUMENT EXAMPLE - OUTPUT
tag,rec,val.hmd,val.tmp
scs-ap1-6,2018-04-04T14:50:38.394+00:00,59.7,23.8

SEE ALSO
scs_analysis/csv_logger
scs_analysis/csv_reader

RESOURCES
https://jsonlines.org
"""

import sys

from scs_core.csv.csv_writer import CSVWriter

from scs_mfr.cmd.cmd_csv_writer import CmdCSVWriter


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    writer = None

    document_count = 0
    processed_count = 0

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdCSVWriter()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("csv_writer: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        writer = CSVWriter(filename=cmd.filename, append=cmd.append, exclude_header=cmd.exclude_header,
                           header_scan=cmd.header_scan, quote_all=cmd.quote_all)

        if cmd.verbose:
            print("csv_writer: %s" % writer, file=sys.stderr)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        for line in sys.stdin:
            jstr = line.strip()

            document_count += 1

            if not writer.write(jstr):
                continue

            # echo...
            if cmd.echo:
                print(jstr)
                sys.stdout.flush()

            processed_count += 1


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        print(file=sys.stderr)

    finally:
        if writer is not None:
            writer.close()

        if cmd.verbose:
            print("csv_writer: documents: %d processed: %d" % (document_count, processed_count), file=sys.stderr)
