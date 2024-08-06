from __future__ import annotations
import sys, asyncio, socket
sys.dont_write_bytecode = True
from functools import partial
from typing import Sequence, Self, override, Any

from mariadb.connections import (
    _DEFAULT_CHARSET, _DEFAULT_COLLATION, _MAX_TPC_XID_SIZE,
    Connection as Con
)

from .cursors import Cursor

class Connection(Con):
    """
    MariaDB async Connector/Python Connection Object

    Handles the connection to a MariaDB or MySQL database server.
    It encapsulates a database session.

    Connections are created using the method `await aiomaria.connect()`
    """
    
    def __init__(self, **kwargs) -> None:
        self.warnings: bool
        self.loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
        super().__init__(**kwargs)

        # removing sync context manager
        #del self.__enter__
        #del self.__exit__

    @override
    async def cursor(self, cursorclass = Cursor, **kwargs) -> Cursor[Self]:
        return await self.loop.run_in_executor(None, partial(super().cursor, cursorclass=cursorclass, **kwargs))
    
    @override
    async def close(self) -> None:
        return await self.loop.run_in_executor(None, super().close)
    
    @override
    async def commit(self) -> None:
        return await self.loop.run_in_executor(None, super().commit)
    
    @override
    async def rollback(self) -> None:
        return await self.loop.run_in_executor(None, super().rollback)
    
    @override
    async def kill(self, id: int) -> None:
        return await self.loop.run_in_executor(None, super().kill, id)

    @override
    async def begin(self) -> None:
        return await self.loop.run_in_executor(None, super().begin)
    
    @override
    async def select_db(self) -> None:
        return await self.loop.run_in_executor(None, super().select_db)

    # TODO: s
    @override
    async def get_server_version(self) -> tuple[int, int, Any]:
        version = await self.loop.run_in_executor(None, super().get_server_version)
        print(version)
        return version
    
    @override
    async def show_warnings(self) -> None | Sequence[Sequence[Any]]:
        self._check_closed()
        if (not self.warnings):
            return None

        cursor: Cursor = await self.cursor()
        await cursor.execute("SHOW WARNINGS")
        ret: Sequence[Sequence[Any]] = await cursor.fetchall()
        del cursor
        return ret
    
    @override
    async def tpc_begin(self, xid: "Connection.xid") -> None:
        return await self.loop.run_in_executor(None, super().tpc_begin, xid)
    
    @override
    async def tpc_commit(self, xid: "Connection.xid" = None) -> None:
        return await self.loop.run_in_executor(None, super().tpc_commit, xid)
    
    @override
    async def tpc_prepare(self) -> None:
        return await self.loop.run_in_executor(None, super().tpc_prepare)
    
    @override
    async def tpc_rollback(self, xid: "Connection.xid" = None) -> None:
        return await self.loop.run_in_executor(None, super().tpc_rollback, xid)

    @override
    async def tpc_recover(self) -> None:
        self._check_closed()
        cursor: Cursor = await self.cursor()
        await cursor.execute("XA RECOVER")
        result: Sequence[Sequence[Any]] = await cursor.fetchall()
        del cursor
        return result

    async def __aenter__(self) -> Self:
        """Returns a copy of the connection."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Closes connection."""
        self._check_closed()
        await self.close()

    # TODO: type
    @property
    def database(self) -> str:
        return super().database
    
    @property
    def user(self) -> str:
        return super().user
    
    @property
    def character_set(self) -> str:
        return super().character_set
    
    # TODO: type
    @property
    def client_capabilities(self) -> bool | int:
        return super().client_capabilities
    
    # TODO: type
    @property
    def server_capabilities(self) -> bool | int:
        return super().server_capabilities
    
    #TODO: type
    @property
    def extended_server_capabilities(self) -> bool | int:
        return super().extended_server_capabilities
    
    @property
    def server_port(self) -> int:
        return super().server_port
    
    # TODO: type
    @property
    def unix_socket(self) -> str:
        return super().unix_socket
    
    @property
    def server_name(self) -> str:
        return super().server_name
    
    @property
    def collation(self) -> str:
        return super().collation
    
    @property
    def server_info(self) -> str:
        return super().server_info
    
    # TODO: type
    @property
    def tls_cipher(self) -> str:
        return super().tls_cipher
    
    # TODO: type
    @property
    def tls_version(self) -> int:
        return super().tls_version
    
    # TODO: type
    @property
    def server_status(self) -> int | bool | str:
        return super().server_status
    
    @property
    def server_version(self) -> int:
        return super().server_version
    
    @property
    def server_version_info(self) -> tuple[int, int, int | float]:
        return super().server_version_info
    
    @property
    def autocommit(self) -> bool:
        return super().autocommit

    @autocommit.setter
    def autocommit(self, mode: int) -> None:
        self._check_closed()
        if bool(mode) == self.autocommit:
            return
        try:
            self._execute_command("SET AUTOCOMMIT=%s" % int(mode))
            self._read_response()
        except Exception:
            raise

    @property
    def socket(self) -> socket.socket:
        return super().socket
    
    @property
    def open(self) -> bool:
        return super().open
    
    # TODO: type
    @property
    def thread_id(self) -> int | str:
        return super().thread_id