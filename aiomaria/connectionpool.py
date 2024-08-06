from __future__ import annotations
import sys, asyncio
sys.dont_write_bytecode = True
from functools import partial
from typing import override, TYPE_CHECKING

from mariadb.connectionpool import (
    MAX_POOL_SIZE, ConnectionPool as ConP
)

if TYPE_CHECKING:
    from .connections import Connection

class ConnectionPool(ConP):
    def __init__(self, pool_name: str, pool_size: int = 5, pool_reset_connection: bool = True) -> None:
        """
        Creates a connection pool class

        - `pool_name` - Name of connection pool
        - `pool_size` - Size of pool. If not specified default value of 5 will be used. Maximum allowed number is 64.
        - `pool_reset_connection` -  Will reset the connection before returning it to the pool. 
        """
        self.loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
        super().__init__(pool_name, pool_size, pool_reset_connection)

    @override
    async def add_connection(self, connection=None) -> Connection | None:
        return await self.loop.run_in_executor(None, super().add_connection, connection)
    
    @override
    async def get_connection(self) -> Connection:
        return await self.loop.run_in_executor(None, super().get_connection)
    
    @override
    async def set_config(self, **kwargs) -> None:
        return await self.loop.run_in_executor(None, partial(super().set_config, **kwargs))
    
    @override
    async def close(self) -> None:
        return await self.loop.run_in_executor(None, super().close)
    
    @property
    def pool_name(self) -> str:
        return super().pool_name
    
    @property
    def pool_size(self) -> int:
        return super().pool_size
    
    @property
    def max_size(self) -> int:
        return super().max_size
    
    @property
    def connection_count(self) -> int:
        return super().connection_count
    
    @property
    def pool_reset_connection(self) -> bool:
        return super().pool_reset_connection

    
"""
_replace_connection -> [.add_connection], connection.close
get_connection -> _replace_connection
_close_connection -> connection.reset, connection.rollback, ._replace_connection
close -> connection.close
"""