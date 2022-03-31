import aiohttp
import asyncio

from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class WebScraper:
    soup = dict()


    async def get_headers(self):
        return {
            "user-agent": UserAgent().random
        }


    async def get_soup(self,url, name=None):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get(url, headers=await self.get_headers()) as response:
                name = name if name != None else response.url
                return BeautifulSoup(await response.text(encoding="utf-8"), "lxml")

        
    
if __name__ == "__main__":
    ws = WebScraper()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ws.main())