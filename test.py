import sys, asyncio
sys.dont_write_bytecode = True
import aiomaria

async def main() -> None:
    credentials = dict(host="localhost", port=3306, user="root", password="root")

    async with aiomaria.Connection(**credentials) as con:
        print(con.server_info)


    conn: aiomaria.Connection = await aiomaria.connect()
    print(conn.server_info)
    await conn.close()

asyncio.run(main())
