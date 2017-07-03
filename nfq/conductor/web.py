# NFQ Logwrapper. A tool for centralizing and visualizing logs.
# Copyright (C) 2017 Guillem Borrell Nogueras
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
import logging
from tornado import web, template, httpclient
from nfq.logwrapper.db import session
from nfq.conductor.db import Daemon

root_path = os.path.abspath(os.path.join(os.path.realpath(__file__), os.path.pardir))
loader = template.Loader(os.path.join(root_path, 'templates'))


def get_from_daemon(ip, port, call):
    http_client = httpclient.HTTPClient()
    try:
        response = http_client.fetch("http://{}:{}/{}".format(
            ip, port, call
        ))
        rval = response.body.decode()
    except httpclient.HTTPError as e:
        # HTTPError is raised for non-200 responses; the response
        # can be found in e.response.
        rval = 'NA'
    except Exception as e:
        # Other errors are possible, such as IOError.
        rval = 'NA'

    http_client.close()
    return rval


class DaemonsHandler(web.RequestHandler):
    def get(self):
        daemons = session.query(Daemon).filter(Daemon.active)
        checked_daemons = list()

        for daemon in daemons:
            key = get_from_daemon(daemon.ip, daemon.port, '')

            if key == daemon.uuid:
                checked_daemons.append(daemon)
            else:
                logging.info('Daemon {} is inactive'.format(daemon.uuid))
                daemon.active = False

        session.commit()

        self.write(
            loader.load("daemons.html").generate(daemons=checked_daemons)
        )


class DaemonHandler(web.RequestHandler):
    def get(self, uuid):
        daemon = session.query(Daemon).filter(Daemon.uuid == uuid).one_or_none()
        self.write(
            loader.load("daemon.html").generate(daemon=daemon,
                                                cpu_count=get_from_daemon(
                                                    daemon.ip,
                                                    daemon.port,
                                                    'cpu_count'))
        )
