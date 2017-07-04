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
import json
import logging
from tornado import web, template, httpclient
from nfq.logwrapper.db import session
from nfq.conductor.db import Daemon, Process
from operator import attrgetter

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


def post_job(ip, port, body):
    http_client = httpclient.HTTPClient()
    logging.info('Sending job')
    response = http_client.fetch(
        "http://{}:{}/send_process".format(ip, port),
        method='POST',
        body=body)

    return response.body


def kill_job(ip, port, pid):
    http_client = httpclient.HTTPClient()
    logging.info('Sending job')
    response = http_client.fetch(
        "http://{}:{}/kill/{}".format(ip, port, pid))

    return response.body


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

        daemon_info = list()
        for daemon in checked_daemons:
            usage_str = get_from_daemon(daemon.ip, daemon.port, 'usage')
            cpu_usage = json.loads(usage_str)
            daemon_info.append((daemon, cpu_usage))

        self.write(
            loader.load("daemons.html").generate(daemons=daemon_info)
        )


class DaemonHandler(web.RequestHandler):
    def get(self, uuid):
        daemon = session.query(Daemon).filter(Daemon.uuid == uuid).one_or_none()
        processes = [s for s in session.query(
            Process).filter(
            Process.host == uuid).order_by(
            Process.when
        )]
        processes = [p for p in reversed(sorted(processes,
                                                key=attrgetter('running')))]

        for proc in processes:
            if proc.running:
                # Check if the wrapped process is running
                running = get_from_daemon(
                    daemon.ip,
                    daemon.port,
                    'is_running/{}'.format(proc.process))
                if running == 'False':
                    logging.info('Proccess {} stopped'.format(proc.label))
                    proc.running = False

        session.commit()

        self.write(
            loader.load("daemon.html").generate(daemon=daemon,
                                                processes=processes,
                                                cpu_count=get_from_daemon(
                                                    daemon.ip,
                                                    daemon.port,
                                                    'cpu_count'))
        )

    def post(self, *args, **kwargs):
        if self.get_argument('command', default=None):
            logging.info('Posting job {}'.format(self.get_argument('command')))
            response = post_job(self.get_argument('ip'),
                                self.get_argument('port'),
                                self.get_argument('command'))

        elif self.get_argument('pid', default=None):
            logging.info('Killing pid {}'.format(self.get_argument('pid')))
            response = kill_job(self.get_argument('ip'),
                                self.get_argument('port'),
                                self.get_argument('pid'))

        self.write(response)
