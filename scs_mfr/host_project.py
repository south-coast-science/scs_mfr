#!/usr/bin/env python3

"""
Created on 18 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

workflow:
  1: ./scs_mfr/system_id.py
  2: ./scs_mfr/api_auth.py
  3: ./scs_mfr/host_device.py
> 4: ./scs_mfr/host_project.py

Requires APIAuth and SystemID documents.
Creates Project document.

command line example:
./scs_mfr/host_project.py -v -s field-trial 2 -g 28
"""

import sys

from scs_core.data.json import JSONify
from scs_core.osio.client.api_auth import APIAuth
from scs_core.osio.config.project import Project
from scs_core.osio.data.topic import Topic
from scs_core.osio.data.topic_info import TopicInfo
from scs_core.osio.manager.topic_manager import TopicManager
from scs_core.sys.system_id import SystemID

from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_host_project import CmdHostProject


# TODO: check if the project / topics already exist - if so do update, rather than create

# TODO: schema_id must be derived from afe_calib.json using OSIO mapping class

# --------------------------------------------------------------------------------------------------------------------

class TopicCreator(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, topic_manager):
        """
        Constructor
        """
        self.__topic_manager = topic_manager


    # ----------------------------------------------------------------------------------------------------------------

    def construct_topic(self, path, name, description, schema_id):
        # topic = self.__topic_manager.find(path)

        # if topic:
        #     print("Warning: topic already exists: %s")
        #     TODO: update topic with field params
            # return

        # success = self.__topic_manager.create()

        info = TopicInfo(TopicInfo.FORMAT_JSON, None, None, None)     # for the v2 API, schema_id goes in Topic
        topic = Topic(path, name, description, True, True, info, schema_id)

        print(topic)

        try:
            success = self.__topic_manager.create(topic)
        except RuntimeError:
            success = False

        return success


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "TopicCreator:{topic_manager:%s}" % self.__topic_manager


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdHostProject()

    if cmd.verbose:
        print(cmd, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # APIAuth...
    auth = APIAuth.load_from_host(Host)

    if auth is None:
        print("APIAuth not available.", file=sys.stderr)
        exit()

    # SystemID...
    system_id = SystemID.load_from_host(Host)

    if system_id is None:
        print("SystemID not available.", file=sys.stderr)
        exit()

    if cmd.verbose:
        print(system_id, file=sys.stderr)

    # manager...
    manager = TopicManager(HTTPClient(), auth.api_key)

    creator = TopicCreator(manager)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        project = Project.construct(auth.org_id, cmd.group, cmd.location_id)

        print(JSONify.dumps(project))

        creator.construct_topic(project.climate_topic_path(), Project.CLIMATE_NAME,
                                Project.CLIMATE_DESCRIPTION, Project.CLIMATE_SCHEMA)

        creator.construct_topic(project.gases_topic_path(), Project.GASES_NAME,
                                Project.GASES_DESCRIPTION, cmd.gases_schema_id)

        creator.construct_topic(project.particulates_topic_path(), Project.PARTICULATES_NAME,
                                Project.PARTICULATES_DESCRIPTION, Project.PARTICULATES_SCHEMA)

        creator.construct_topic(project.status_topic_path(system_id), Project.STATUS_NAME,
                                Project.STATUS_DESCRIPTION, Project.STATUS_SCHEMA)

        creator.construct_topic(project.control_topic_path(system_id), Project.CONTROL_NAME,
                                Project.CONTROL_DESCRIPTION, Project.CONTROL_SCHEMA)

        project.save(Host)      # TODO: only save if successful


    else:
        project = Project.load_from_host(Host)
        print(JSONify.dumps(project))

    if cmd.verbose:
        print("-", file=sys.stderr)
        print("climate_topic:      %s" % project.climate_topic_path(), file=sys.stderr)
        print("gases_topic:        %s" % project.gases_topic_path(), file=sys.stderr)
        print("particulates_topic: %s" % project.particulates_topic_path(), file=sys.stderr)

        print("status_topic:       %s" % project.status_topic_path(system_id), file=sys.stderr)
        print("control_topic:      %s" % project.control_topic_path(system_id), file=sys.stderr)