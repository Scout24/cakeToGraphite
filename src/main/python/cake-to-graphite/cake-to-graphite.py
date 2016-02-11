#!/usr/bin/env python

import sys
import time

import yamlreader
from gatherData import gather_data

from pushToGraphite import push_data
from succubus import Daemon
from logging.handlers import WatchedFileHandler
import logging


class StatusCakeGraphiteLink(Daemon):
    def run(self):
        try:
            config = yamlreader.yaml_load('/etc/cake.conf.d/')

            handler = WatchedFileHandler('/tmp/succubus.log')
            self.logger = logging.getLogger()
            self.logger.addHandler(handler)
            while True:
                for test_name, test_id in config['tests'].iteritems():
                    self.logger.warn('{0}: fetching data for {1}:{2}'.format(
                            time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()), test_name, test_id))
                    data_dict = gather_data(config['apikey'], config['username'], test_id)
                    push_data(data_dict, test_name, config['graphitehost'])
                time.sleep(600)
        except Exception:
            self.logger.exception('strange stuff')


def main():
    daemon = StatusCakeGraphiteLink(pid_file='succubus.pid')
    sys.exit(daemon.action())


if __name__ == '__main__':
    main()
