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

# Configuration is loaded at import time. Do not touch this

from nfq.logwrapper.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text


class Daemon(Base):
    __tablename__ = 'daemons'

    id = Column(Integer, primary_key=True)
    ip = Column(String)
    uuid = Column(String)
    when = Column(DateTime)
    port = Column(Integer)
    active = Column(Boolean)

    def to_dict(self):
        return {
            'ip': self.ip,
            'uuid': self.uuid,
            'when': self.when.isoformat(),
            'port': self.port,
            'active': self.active
        }


class Process(Base):
    __tablename__ = 'processes'

    id = Column(Integer, primary_key=True)
    process = Column(Integer)
    wrapped = Column(Integer)
    when = Column(DateTime)
    host = Column(String)
    label = Column(String)
    source = Column(String)
    command = Column(String)
    running = Column(Boolean)

    def to_dict(self):
        return {
            'process': self.process,
            'wrapped': self.wrapped,
            'host': self.host,
            'when': self.when.isoformat(),
            'label': self.label,
            'source': self.source,
            'command': self.command
        }


class Configuration(Base):
    __tablename__ = 'configurations'

    id = Column(Integer, primary_key=True)
    when = Column(DateTime)
    config = Column(Text)

    def to_dict(self):
        return {
            'when': self.when.isoformat(),
            'config': self.config
        }
