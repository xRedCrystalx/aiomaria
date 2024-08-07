# aiomaria

Asynchronous wrapper for MariaDB library (mariadb-connector-python) written in python.

> [!IMPORTANT]
> This library is still under early development. For any bugs, please create an issue [here](https://github.com/xRedCrystalx/aiomaria/issues/new).

## Example

### Basic connection

```py
import aiomaria, asyncio

credentials = {
    "host": "localhost",
    "port": 3306,
    "user": "user",
    "password": "password",
    "database": "database"
}

async def main() -> None:
    con: aiomaria.Connection = await aiomaria.connect(**credentials)
    print(con.server_info)
    await con.close()

asyncio.run(main())
```

### Connection pool

```py
# `pool_name` param will trigger pool creation
pool: aiomaria.Connection = await aiomaria.connect(**credentials, pool_name="test")
```

> [!NOTE]
> `.connect()` will always return `aiomaria.Connection`. Pool can be accessed from the `aiomaria._CONNECTION_POOLS` dictionary with its name.

### With async context manager

```py
async with aiomaria.Connection(**credentials) as con:
    print(con.server_info)

# or

async with aiomaria.ConnectionPool(**credentials, pool_name="test") as pool:
    con: aiomaria.Connection = await pool.get_connection()
    print(con.server_info)
```

> [!CAUTION]
> Due to how wrapper works, `mariadb` library will no longer work once the `aiomaria` is imported. This is due to monkeypatching at runtime and will hopefully be resolved in the future.

## Installation

```cmd
pip install aiomaria
```

For operating systems other than MS Windows, some binaries are required. See [MariaDB connector installation](https://mariadb.com/docs/server/connect/programming-languages/python/install/).

## Licence

MIT License
