import asyncio

from src.core.config import settings

STOPWORD = "STOP"


async def publish(task: asyncio.Task, channel: str, msg: str):
    pub = settings.REDIS

    if not task.done() and pub:
        await pub.publish(channel, msg)
    if (msg == STOPWORD) and pub:
        await pub.publish(channel, STOPWORD)
