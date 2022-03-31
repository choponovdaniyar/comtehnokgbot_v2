from aiosqlitedb import AioSqliteDb

class aiotable(AioSqliteDb):
    query = None #запросы
#C
    async def create(self):
        pass
    
    async def save(self): #создание или обновление
        pass
#R
    async def get(self):
        pass

    async def get_or_create(self): # получить или создать
        pass

    async def all(self):
        pass

    async def filter(self):
        pass

    async def exclude(self):    
        pass

#U
    async def update(self): # обновление данных
        pass
 
    async def update_or_create(self): # обновить или создать
        pass

#D
    async def delete(self): # обновление данных
        pass

    

    

   


if __name__ == "__main__":
    pass