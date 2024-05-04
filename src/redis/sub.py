import asyncio
from typing import Callable

import async_timeout
from aioredis.client import PubSub

from src.core.config import settings

STOPWORD = "STOP"


async def sub_reader(client: PubSub, callback: Callable):
    while client.listen():
        try:
            async with async_timeout.timeout(1):
                message = await client.get_message(ignore_subscribe_messages=True)
                if message is not None:
                    if message["data"] == "get_board_data":
                        await callback()
                    if message["data"] == STOPWORD:
                        break
                await asyncio.sleep(0.01)
        except asyncio.TimeoutError:
            pass
        except asyncio.CancelledError:
            break
        except Exception:
            break


async def subscribe_and_read(channel: str, callback: Callable):
    redis = settings.REDIS
    if redis:
        psub = redis.pubsub()

        async with psub as client:
            await client.subscribe(channel)
            await sub_reader(client, callback)
            await client.unsubscribe(channel)

        await psub.close()
    else:
        raise Exception("No redis instance")
