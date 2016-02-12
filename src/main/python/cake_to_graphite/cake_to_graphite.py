import logging
import sys
import time
from logging.handlers import WatchedFileHandler

import yamlreader
from succubus import Daemon
from gather_data import gather_data
from push_to_graphite import push_data


class StatusCakeGraphiteLink(Daemon):
    def run(self):

        handler = WatchedFileHandler('/tmp/cake.log')
        self.logger = logging.getLogger()
        self.logger.addHandler(handler)
        try:
            config = yamlreader.yaml_load('/etc/cake.conf.d/')
            self.logger.exception(config)
            while True:
                for test_name, test_id in config['tests'].iteritems():
                    self.logger.info('{0}: fetching data for {1}:{2}'.format(
                            time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()), test_name, test_id))
                    data_dict = gather_data(config['apikey'], config['username'], test_id)
                    push_data(data_dict, test_name, config['graphitehost'])
                time.sleep(600)
        except Exception:
            self.logger.exception('succubus doing some strange stuff')


def main():
    daemon = StatusCakeGraphiteLink(pid_file='succubus.pid')
    sys.exit(daemon.action())


if __name__ == '__main__':
    main()
