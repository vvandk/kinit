#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2022/11/3 17:23
# @File           : count.py
# @IDE            : PyCharm
# @desc           : 计数


from redis.asyncio.client import Redis


class Count:
    """
    计数
    """

    def __init__(self, rd: Redis, key):
        self.rd = rd
        self.key = key

    async def add(self, ex: int = None) -> int:
        await self.rd.set(self.key, await self.get_count() + 1, ex=ex)
        return await self.get_count()

    async def subtract(self, ex: int = None) -> int:
        await self.rd.set(self.key, await self.get_count() - 1, ex=ex)
        return await self.get_count()

    async def get_count(self) -> int:
        number = await self.rd.get(self.key)
        if number:
            return int(number)
        return 0

    async def reset(self) -> None:
        await self.rd.set(self.key, 0)

    async def delete(self) -> None:
        await self.rd.delete(self.key)
