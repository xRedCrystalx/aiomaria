"""
aiomaria
"""

from __future__ import annotations
import sys
sys.dont_write_bytecode = True

import mariadb.connections
import mariadb.connectionpool
import mariadb.cursors

import mariadb.release_info as maria_info
from mariadb import (
    client_version, 
    client_version_info,
    _CONNECTION_POOLS
)
_CONNECTION_POOLS: dict[str, ConnectionPool]

__version__: str = "1.0.0"
__version_info__: tuple[int, ...] = (1, 0, 0)
__author__: str = "xRedCrystalx"

from .connections import Connection
from .cursors import Cursor
from .field import fieldinfo
from .dbapi20 import *
from .connectionpool import ConnectionPool

# monkeypatching 
mariadb.Connection = mariadb.connections.Connection = Connection
mariadb.ConnectionPool = mariadb.connectionpool.ConnectionPool = ConnectionPool
mariadb.Cursor = mariadb.cursors.Cursor = Cursor

# NOTE: this function is blocking due to creation of `Connection`, which requires to be in a thread with running asyncio loop.
async def connect(connectionclass=Connection, **kwargs) -> Connection:
    return mariadb.connect(connectionclass=connectionclass, **kwargs)
