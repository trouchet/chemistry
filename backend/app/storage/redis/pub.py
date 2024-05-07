import asyncio

from chemistry.core.config import settings
from .constants import STOPWORD

async def publish(task: asyncio.Task, channel: str, msg: str):
    pub = settings.REDIS

    if not task.done() and pub:
        await pub.publish(channel, msg)
    if (msg == STOPWORD) and pub:
        await pub.publish(channel, STOPWORD)
