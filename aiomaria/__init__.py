"""
aiomaria
"""

from __future__ import annotations
import sys, typing, asyncio
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

_CONNECTION_POOLS: dict[str, ConnectionPool]

async def connect(connectionclass=Connection, **kwargs) -> Connection:
    """
    Creates a MariaDB Connection object.

    By default the standard connectionclass `mariadb.connections.Connection`
    will be created.
    
    Parameter connectionclass specifies a subclass of
    mariadb.Connection object. If not specified default will be used.

    Connection parameters are provided as a set of keyword arguments:
    - `host`
        
        The host name or IP address of the database server.
        If MariaDB Connector/Python was built with MariaDB Connector/C 3.3
        it is also possible to provide a comma separated list of hosts for
        simple fail over in case of one or more hosts are not available.
    - `user, username`

        The username used to authenticate with the database server
    - `password, passwd`

        The password of the given user
    - `database, db`

        Database (schema) name to use when connecting with the database
        server
    - `unix_socket`

        The location of the unix socket file to use instead of using an IP
        port to connect. If socket authentication is enabled, this can also
        be used in place of a password.
    - `port`

        port number of the database server. If not specified the default
        value of `3306` will be used.
    - `connect_timeout`

        connect timeout in seconds
    - `read_timeout`

        read timeout in seconds
    - `write_timeout`

        write timeout in seconds
    - `local_infile`

        Enables or disables the use of LOAD DATA LOCAL INFILE statements.
    - `compress=False`

        Uses the compressed protocol for client server communication. If
        the server doesn't support compressed protocol, the default
        protocol will be used.
    - `init_command`

        Command(s) which will be executed when connecting and reconnecting
        to the database server
    - `default_file`

        Read options from the specified option file. If the file is an
        empty string, default configuration file(s) will be used
    - `default_group`

        Read options from the specified group
    - `plugin_dir`

        Directory which contains MariaDB client plugins.
    - `reconnect`

        Enables or disables automatic reconnect. (mariadb connector version 1.1.4 +)
    - `ssl_key`

        Defines a path to a private key file to use for TLS. This option
        requires that you use the absolute path, not a relative path. The
        specified key must be in PEM format
    - `ssl_cert`

        Defines a path to the X509 certificate file to use for TLS.
        This option requires that you use the absolute path, not a relative
        path. The X609 certificate must be in PEM format.

    - `ssl_ca`

        Defines a path to a PEM file that should contain one or more X509
        certificates for trusted Certificate Authorities (CAs) to use for
        TLS.  This option requires that you use the absolute path, not a
        relative path.

    - `ssl_capath`
        Defines a path to a directory that contains one or more PEM files
        that contains one X509 certificate for a trusted Certificate
        Authority (CA)

    - `ssl_cipher`

        Defines a list of permitted cipher suites to use for TLS
    - `ssl_crlpath`

        Defines a path to a PEM file that should contain one or more
        revoked X509 certificates to use for TLS. This option requires
        that you use the absolute path, not a relative path.
    - `ssl_verify_cert`

        Enables server certificate verification.
    - `ssl`

        The connection must use TLS security or it will fail.
    - `tls_version`

        A comma-separated list (without whitespaces) of TLS versions.
        Valid versions are TLSv1.0, TLSv1.1,TLSv1.2 and TLSv1.3.
        (mariadb connector version 1.1.7+)
    - `autocommit=False`

        Specifies the autocommit settings.
        True will enable autocommit, False will disable it (default).
    - `converter`

        Specifies a conversion dictionary, where keys are FIELD_TYPE
        values and values are conversion functions
    """
    if kwargs:
        if "pool_name" in kwargs:
            if not kwargs["pool_name"] in mariadb._CONNECTION_POOLS:
                pool: ConnectionPool = ConnectionPool(**kwargs)
            else:
                pool: ConnectionPool = _CONNECTION_POOLS[kwargs["pool_name"]]
            return await pool.get_connection()

    connection = connectionclass(**kwargs)
    if not isinstance(connection, Connection):
        raise mariadb.ProgrammingError(f"{connection} is not an instance of mariadb.Connection")
    return connection