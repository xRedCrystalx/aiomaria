import sys, asyncio
sys.dont_write_bytecode = True
from typing import Sequence, override, Any

from mariadb.field import (
    field_types, field_flags, 
    fieldinfo as fi
)

field_types: dict[int, str]
field_flags: dict[int, str]

class fieldinfo(fi):
    def __init__(self) -> None:
        self.loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()

    @override
    async def type(self, description: Sequence[Any]) -> str | None:
        print(description)
        return await self.loop.run_in_executor(None, super().type, description)
         
    @override
    async def flag(self, description) -> str:
        print(description)
        return await self.loop.run_in_executor(None, super().flag, description)
    
# TODO: check datatype in runtime