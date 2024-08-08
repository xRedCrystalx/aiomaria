from __future__ import annotations
import sys, asyncio
sys.dont_write_bytecode = True
from typing import Sequence, Literal, Self, override, Any, TYPE_CHECKING

from mariadb.cursors import (
    PARAMSTYLE_QMARK, PARAMSTYLE_FORMAT, PARAMSTYLE_PYFORMAT,
    ROWS_ALL, ROWS_EOF,
    RESULT_TUPLE, RESULT_NAMEDTUPLE, RESULT_DICTIONARY,
    SQL_NONE, SQL_INSERT, SQL_UPDATE, SQL_REPLACE, SQL_DELETE, SQL_CALL, SQL_DO, SQL_SELECT, SQL_OTHER,
    Cursor as Crs
)

if TYPE_CHECKING:
    from .connections import Connection

class Cursor(Crs):
    def __init__(self, connection: Connection, **kwargs) -> None:
        """MariaDB Connector/Python Cursor Object"""

        self.loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
        super().__init__(connection, **kwargs)

        # removing sync context manager and iter
        #delattr(self, "__enter__")
        #delattr(self, "__exit__")
        #delattr(self, "__iter__")

    @override
    async def callproc(self, sp: str, data: Sequence[Any] = None) -> None:
        if not data:
            data: list = []
        return await self.loop.run_in_executor(None, super().callproc, sp, data)

    @override
    async def nextset(self) -> None: 
        return await self.loop.run_in_executor(None, super().nextset)

    @override
    async def execute(self, statement: str, data: Sequence = None, buffered = None) -> None:
        return await self.loop.run_in_executor(None, super().execute, statement, data, buffered)
    
    # TODO: l
    @override
    async def executemany(self, statement: str, parameters: Sequence[str]):
        return await self.loop.run_in_executor(None, super().executemany, statement, parameters)

    @override
    async def close(self) -> None:
        return await self.loop.run_in_executor(None, super().close)

    @override
    async def fetchone(self) -> Sequence[Any] | None:
        return await self.loop.run_in_executor(None, super().fetchone)

    @override
    async def fetchmany(self, size: int = 0) -> Sequence[Sequence[Any]]:
        return await self.loop.run_in_executor(None, super().fetchmany, size)

    @override
    async def fetchall(self)-> Sequence[Sequence[Any]]:
        return await self.loop.run_in_executor(None, super().fetchall)
    
    @override
    async def scroll(self, value: int, mode: Literal["relative", "absolute"] = "relative") -> None:
        return await self.loop.run_in_executor(None, super().scroll, value, mode)
    
    @override
    async def setinputsizes(self, size: int) -> None:
        return

    @override
    async def setoutputsize(self, size: int) -> None:
        return

    async def __aenter__(self) -> Self:
        """Returns a copy of the cursor."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Closes cursor."""
        await self.close()

    @property
    def rowcount(self) -> int:
        return super().rowcount

    @property
    def sp_outparams(self) -> bool:
        return super().sp_outparams

    @property
    def lastrowid(self) -> int | None:
        return super().lastrowid
    
    @property
    def connection(self) -> Connection:
        return super().connection


"""
def _substitute_parameters
def _check_execute_params
def _parse_execute
def _fetch_row
def __iter__

await .callproc -> [.execute]
await .execute -> ._execute_text, ._readresponse, ._execute_binary, ._bulk, ._check_text_types, ._parse_execute
await .executemany -> ._clear_result, [.execute], ._parse_execute, ._execute_bulk
await .fetchone -> ._fetch_row
await .scroll -> ._seek


# general
self._connection: Connection
self._paramstyle: int
self._command: int

# counts/size
self._rowcount: int
self._rownumber: int
self.rowcount: int
self.rownumber: int
self.field_count: int
self.paramcount: int
self.arraysize: int

#  constants
self.is_text: bool
self.closed: bool
self._bulk: bool
self._text: bool
self._dictionary: bool
self._named_tuple: bool
self._force_binary: bool
self.buffered: bool
self._prepared: bool
self._reprepare: bool

# type
self._resulttype: int
self._cursor_type: int

# statements
self.statement: str
self._prev_stmt: str
self._transformed_statement: str 

# have to figure out
self._paramlist: list
self._keys: list
self._data: dict

self._description: None       
self._parseinfo: None
"""