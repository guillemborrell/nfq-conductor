# NFQ Conductor. A tool for centralizing and visualizing logs.
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

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import zmq
import datetime
import psutil
import logging

from tornado.options import define, options
from uuid import uuid4

UUID = str(uuid4())

define("port", default=8999, help="run on the given port", type=int)
define("interface", default='lo', help="network interface for collector connection", type=str)
define("collector", default='tcp://127.0.0.1:5555', help="Collector socket address", type=str)
define("uuid", default=UUID, help="Unique ID for the daemon", type=str)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(options.uuid)


class CpuCountHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(str(psutil.cpu_count()))


def run():
    tornado.options.parse_command_line()

    # Fetch network information
    ip = psutil.net_if_addrs()[options.interface][0].address

    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.connect(options.collector)

    socket.send_json({
        'source': options.uuid,
        'when': datetime.datetime.now().isoformat(),
        'message': '^^^^{{"ip": "{}", "port": {}, "uuid": "{}" }}'.format(
            ip, options.port, options.uuid
        )
    })

    socket.close()
    context.destroy()
    logging.info('Sent configuration message')
    logging.info('{{"ip": "{}", "port": {}, "uuid": "{}" }}'.format(
            ip, options.port, options.uuid
        ))

    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/cpu_count", CpuCountHandler)
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    run()
