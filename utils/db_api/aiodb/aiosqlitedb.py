import aiosqlite

 

class AioSqliteDb():
    def connection(func):
        async def wrapper(self, *args, **kwargs):
            kwargs["connect"] = await aiosqlite.connect("{}.db".format(self.name))
            kwargs["cursor"] = await kwargs["connect"].cursor()
            result= await func(self, *args, **kwargs)
            await kwargs["connect"].close()
            return result
        return wrapper

    name = "hello"
    async def run(self, name):
        self.name = name

    @connection
    async def __response(self, response, connect = None, cursor = None):
        await cursor.execute(response)
        

    async def create(self, name, cols):
        response = '''
            CREATE TABLE {name}
            (id INTEGER PRIMARY KEY AUTOINCREMENT, {args})
        '''.format(name=name, args= ", ".join(cols))

        await self.__response(response)

    
    async def delete(self, name):
        response = '''
            DROP TABLE {name}
        '''.format(name = name)

        await self.__response(response)


import asyncio

async def main():
    db = AioSqliteDb()
    await db.run("hello")
    await db.delete("asd")

if __name__ =="__main__":
    asyncio.run(main())
    