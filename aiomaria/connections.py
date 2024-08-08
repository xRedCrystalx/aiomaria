from __future__ import annotations
import sys, asyncio, socket
sys.dont_write_bytecode = True
from typing import Self, Literal, override, Any

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
    """
    
    def __init__(self, **kwargs) -> None:
        self.warnings: bool
        self.loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
        super().__init__(**kwargs)

        # removing sync context manager
        #del self.__enter__
        #del self.__exit__

    # NOTE: this function is blocking due to creation of `Cursor`, which requires to be in a thread with running asyncio loop.
    @override
    async def cursor(self, cursorclass = Cursor, **kwargs) -> Cursor:
        return super().cursor(cursorclass, **kwargs)
    
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

    @override
    async def get_server_version(self) -> tuple[int, int, int]:
        return await self.loop.run_in_executor(None, super().get_server_version)
    
    @override
    async def show_warnings(self) -> None | list[tuple[Any]]:
        return self.loop.run_in_executor(None, super().show_warnings)
    
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
        return await self.loop.run_in_executor(None, super().tpc_recover)

    async def __aenter__(self) -> Self:
        """Returns a copy of the connection."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Closes connection."""
        self._check_closed()
        await self.close()

    @property
    def database(self) -> str:
        return super().database
    
    @property
    def user(self) -> str:
        return super().user
    
    @property
    def character_set(self) -> str:
        return super().character_set
    
    @property
    def client_capabilities(self) -> int:
        return super().client_capabilities
    
    @property
    def server_capabilities(self) -> int:
        return super().server_capabilities
    
    @property
    def extended_server_capabilities(self) -> int:
        return super().extended_server_capabilities
    
    @property
    def server_port(self) -> int:
        return super().server_port
    
    @property
    def unix_socket(self) -> str | Literal[""]:
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
    
    @property
    def tls_cipher(self) -> str | Literal[""]:
        return super().tls_cipher
    
    # TODO: type - Not supported on my end
    @property
    def tls_version(self) -> int:
        return super().tls_version
    
    @property
    def server_status(self) -> int:
        return super().server_status
    
    @property
    def server_version(self) -> int:
        return super().server_version
    
    @property
    def server_version_info(self) -> tuple[int, int, int]:
        return super().server_version_info
    
    @property
    def autocommit(self) -> bool:
        return super().autocommit

    @autocommit.setter
    def autocommit(self, mode: int) -> None:
        """
        self._check_closed()
        if bool(mode) == self.autocommit:
            return
        try:
            self._execute_command("SET AUTOCOMMIT=%s" % int(mode))
            self._read_response()
        except Exception:
            raise        
        """
        super().autocommit(mode)

    @property
    def socket(self) -> socket.socket:
        return super().socket
    
    @property
    def open(self) -> bool:
        return super().open
    
    @property
    def thread_id(self) -> int:
        return super().thread_id