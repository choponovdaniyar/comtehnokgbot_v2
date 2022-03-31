import pandas
import asyncio

from loguru import logger

from .webscraper import WebScraper 
import re

class Builder:
    table = None
    ws = WebScraper()
    tables = dict()
    links = [tuple([None, None]), tuple([None, None]), tuple([None, None])]
    async def build_table(self):
        logger.info("builder [start]")

        map = await self.ws.get_soup(url="https://comtehno.kg/timetable/", name="map")
        btns = map.find_all("a", class_="elementor-button-link")
        ids = list()

        for btn in btns:
            if "расписание" not in btn.text.lower():
                continue
            id = re.search(r"\d+", btn.text).group()
            url = btn.attrs["href"]
            ids.append(tuple([int(id),url]))
        
        if self.links != ids: 
            self.links = ids
            logger.info("builder [start building]")
            for id in ids:
                soup = await self.ws.get_soup(url=id[1])
                soup = str(soup.find("table"))
                it = 1
                for table in (await self.html_to_tables(soup)):
                    self.tables["{}{}".format(id[0],it)] = table
                    it += 1
        logger.info("builder [finish]")

    async def html_to_dict(self,html):
        pd = pandas.read_html(html)[0]
        dict_ = pd.to_dict()
        return dict_

    async def dict_to_noSql(self, dict_):
        result = dict()
        prefix = 'Unnamed: '
        width = len(dict_)
        height = len(dict_["{}{}".format(prefix,0)])
        table = list()
        for x in range(height): 
            
            in_table = bool("nan" not in str(list(dict_["{}{}".format(prefix,1)].values())[x]))
            if not in_table:
                if len(table):
                    break
                continue
            table += [list()]
            for y in range(1, width):
                table[-1] += [str(list(dict_["{}{}".format(prefix,y)].values())[x])]
                lesson = table[-1][y-1] if table[-1][y-1] != "nan" else None
                group = table[0][y-1].lower()
                day = table[-1][0].lower() 
        
                if len(table) - 1:
                    if y - 1 == 1:
                        time = table[-1][1].replace(" ","")
                        if len(time[5:]) > 0:
                            time = "-".join([time[:5], time[5:]])

                    if group not in ["ауд.", "время"]:
                        if result.get(group) == None:
                            result[group] = dict() 
                        if result[group].get(day) == None:
                            result[group][day] = dict()
                        if result[group][day].get(time) == None:
                            result[group][day][time] = list()
                        result[group][day][time] += [ lesson ]
        return result

    async def noSql_to_sql(self, dict_):
        table_1 = list()
        table_2 = list()

        for group in dict_:
            for day in dict_[group]:
                for time in dict_[group][day]:
                    lesson_1 = dict_[group][day][time][0]
                    lesson_2 = dict_[group][day][time][-1]
                    table_1 += [ (group, day, time, lesson_1) ]
                    table_2 += [ (group, day, time, lesson_2) ]
        return table_1, table_2

    async def html_to_tables(self,html):
        dict_ = await self.html_to_dict(html)
        result = await self.dict_to_noSql(dict_)
        return await self.noSql_to_sql(result)


async def timer():
    it = 0
    while True:
        await asyncio.sleep(1)
        it += 1
        logger.info("timer [{}]".format(it))
 
        
async def start():
    funcs = [timer()]
    await asyncio.gather(*funcs)
    


if __name__ == "__main__":
    asyncio.run(start())
    

