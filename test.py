import unittest
from app.db import area
from app.main import read_name ,read_id ,create_item ,delete_item , inter_area , read_prop
import asyncio
item = area(name='satellogic_8', date = '2022-01-01', area ='POLYGON((0 0,1 0,1 1,0 1,0 0))' , properties = {'name':'satellogic','crop':'wheat'})
name_str = 'satellogic_1'
name_str_del = 'satellogic_8'
pol = 'POLYGON((0 0,1 0,1 1,0 1,0 0))'
prop = {"name": "satellogic_2","crop":"wheat"}

print('RUNNING TEST')
class Testing(unittest.IsolatedAsyncioTestCase):
    async def test_name(self):
        res = await read_name(name_str)
        self.assertIsNotNone(res)

    async def test_create_item(self):
        res = await create_item(item)
        self.assertIsNotNone(res)

    async def test_delete_item(self):
        res = await delete_item(name_str_del)
        self.assertIsNotNone(res)

    async def test_inter_area(self):
        res = await inter_area(pol)
        self.assertIsNotNone(res)

    async def test_read_prop(self):
        res = await read_prop(prop)
        self.assertIsNotNone(res)


if __name__ == '__main__':
    unittest.main()
