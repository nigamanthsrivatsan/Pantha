import aiosqlite

async def create_db(file, args):
    async with aiosqlite.connect(f"./data/{file}.db") as connection:
        async with connection.cursor() as cursor:
            await connection.execute(f"CREATE TABLE IF NOT EXISTS {args};")

